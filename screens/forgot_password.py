"""صفحه بازیابی رمز با پرسش امنیتی."""

import tkinter as tk

from database import get_user_security_question, reset_user_password
from ui_components import (
    add_field,
    button,
    form_body,
    header,
    link,
    show_status,
    status,
    value,
)


def build(app):
    """چیدمان صفحه بازیابی رمز را می‌سازد."""
    # این فیلدها پاسخ امنیتی و رمز تازه را می‌گیرند.
    body = form_body(app)
    header(app, body, "بازیابی دسترسی", "رمزت را دوباره تنظیم کن", "برای تأیید حساب، پاسخ پرسش امنیتی را وارد کن.")
    status(app, body)
    app.forgot_user_entry = add_field(app, body, "نام کاربری", "نام کاربری حساب", "◉", pady=8)
    # پس از خروج از فیلد نام کاربری، پرسش امنیتی را از دیتابیس می‌خوانیم.
    app.forgot_user_entry.bind("<FocusOut>", lambda _event: on_username_blur(app))

    app.sq_label = tk.Label(
        body,
        text="پس از واردکردن نام کاربری، پرسش امنیتی نمایش داده می‌شود.",
        bg="#faf6f9",
        fg=app.COLORS["plum_mid"],
        font=("Vazirmatn", 9),
        anchor="e",
        justify="right",
        wraplength=520,
        padx=11,
        pady=8,
    )
    app.sq_label.pack(fill="x", pady=(0, 9))
    app.forgot_ans_entry = add_field(app, body, "پاسخ پرسش امنیتی", "پاسخ ثبت‌شده را وارد کن", "⌑", pady=8)
    app.forgot_new_pass_entry = add_field(app, body, "رمز عبور جدید", "حداقل ۴ نویسه", "✧", password=True, pady=4)
    # با هر بار رهاکردن کلید، نوار قدرت رمز را تازه می‌کنیم.
    app.forgot_new_pass_entry.bind("<KeyRelease>", lambda _event: update_password_strength(app))

    # سه نوار کوچک قدرت رمز را نمایش می‌دهند؛ تابع پایین رنگشان را عوض می‌کند.
    meter = tk.Frame(body, bg=app.COLORS["paper"])
    meter.pack(fill="x", pady=(0, 7))
    app.strength_label = tk.Label(meter, text="", bg=app.COLORS["paper"], fg=app.COLORS["muted"], font=("Vazirmatn", 9))
    app.strength_label.pack(side="right", padx=(0, 8))
    app.strength_bars = []
    for _ in range(3):
        bar = tk.Frame(meter, bg="#e7dfe5", width=48, height=5)
        bar.pack(side="right", padx=(0, 4))
        bar.pack_propagate(False)
        app.strength_bars.append(bar)

    button(app, body, "ذخیره رمز جدید  ←", lambda: submit(app))
    link(app, body, "←  بازگشت به صفحه ورود", lambda: app.show_view("login"), anchor="e")
    app.forgot_new_pass_entry.bind("<Return>", lambda _event: submit(app))
    app.forgot_user_entry.focus_set()


def on_username_blur(app):
    """با خروج از فیلد نام کاربری، پرسش امنیتی حساب را پیدا می‌کند."""
    username = value(app.forgot_user_entry).strip()
    if not username:
        return
    question = get_user_security_question(username)
    if question:
        app.sq_label.configure(text=f"پرسش امنیتی حساب:  {question}", fg=app.COLORS["plum"])
    else:
        app.sq_label.configure(text="حسابی با این نام کاربری پیدا نشد.", fg=app.COLORS["danger"])


def update_password_strength(app):
    """نوار قدرت رمز را هنگام تایپ به‌روز می‌کند."""
    length = len(value(app.forgot_new_pass_entry))
    if length == 0:
        level, label, color = 0, "حداقل ۴ نویسه", app.COLORS["muted"]
    elif length < 5:
        level, label, color = 1, "ضعیف", "#c94f5b"
    elif length < 8:
        level, label, color = 2, "متوسط", "#bd8741"
    else:
        level, label, color = 3, "قوی", app.COLORS["success"]
    app.strength_label.configure(text=label, fg=color)
    for index, bar in enumerate(app.strength_bars):
        bar.configure(bg=color if index < level else "#e7dfe5")


def submit(app):
    """رمز تازه را پس از بررسی پاسخ امنیتی در پایگاه داده ذخیره می‌کند."""
    # reset_user_password بررسی پاسخ و ذخیرهٔ رمز را در database.py انجام می‌دهد.
    username = value(app.forgot_user_entry).strip()
    answer = value(app.forgot_ans_entry).strip()
    password = value(app.forgot_new_pass_entry)
    if not username or not answer or not password:
        show_status(app, "همه فیلدها را کامل کن.")
        return
    success, text = reset_user_password(username, answer, password)
    show_status(app, text, error=not success)
    if success:
        app.root.after(1200, lambda: app.show_view("login"))
