"""صفحه ساخت حساب کاربری جدید."""

import tkinter as tk

from database import register_user
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
    """چیدمان فرم ثبت‌نام و پرسش امنیتی را می‌سازد."""
    # هر add_field یک عنوان و فیلد ورودی می‌سازد؛ ظاهر مشترک در ui_components.py است.
    body = form_body(app)
    header(app, body, "شروع یک تجربه تازه", "حساب خودت را بساز", "چند مورد کوتاه را تکمیل کن تا آماده خرید شوی.")
    status(app, body)
    app.reg_fn_entry = add_field(app, body, "نام و نام خانوادگی", "مثال: علیرضا رضایی", "◉", pady=6)
    app.reg_user_entry = add_field(app, body, "نام کاربری", "یک نام کاربری انتخاب کن", "⌑", pady=6)
    app.reg_pass_entry = add_field(app, body, "رمز عبور", "حداقل ۴ نویسه", "✧", password=True, pady=6)

    # پرسش امنیتی از فهرست انتخاب می‌شود تا گزینه‌ها یکسان باشند.
    question_group = tk.Frame(body, bg=app.COLORS["paper"])
    question_group.pack(fill="x", pady=(0, 6))
    tk.Label(
        question_group,
        text="پرسش امنیتی برای بازیابی رمز",
        bg=app.COLORS["paper"],
        fg=app.COLORS["ink"],
        font=("Vazirmatn", 10, "bold"),
        anchor="e",
    ).pack(fill="x", pady=(0, 3))
    questions = (
        "نام اولین مدرسه شما چیست؟",
        "نام اولین حیوان خانگی شما چیست؟",
        "شهر محل تولد شما کجاست؟",
        "رنگ مورد علاقه شما چیست؟",
    )
    # StringVar مقدار انتخاب‌شده از فهرست را نگه می‌دارد تا submit آن را بخواند.
    app.reg_sq_var = tk.StringVar(value=questions[0])
    app.reg_sq_menu = tk.OptionMenu(question_group, app.reg_sq_var, *questions)
    app.reg_sq_menu.configure(
        bg=app.COLORS["field"],
        activebackground="#f3e9f0",
        fg=app.COLORS["ink"],
        activeforeground=app.COLORS["ink"],
        bd=0,
        highlightthickness=1,
        highlightbackground=app.COLORS["line"],
        anchor="e",
        justify="right",
        font=("Vazirmatn", 9),
        height=1,
    )
    app.reg_sq_menu.pack(fill="x", ipady=5)
    app.reg_sq_menu["menu"].configure(
        bg=app.COLORS["paper"],
        fg=app.COLORS["ink"],
        activebackground="#f3e9f0",
        font=("Vazirmatn", 9),
    )

    app.reg_ans_entry = add_field(app, body, "پاسخ پرسش امنیتی", "پاسخی که بعداً یادت می‌ماند", "◇", pady=5)
    # این دکمه تابع submit را اجرا می‌کند؛ تابع پایین فایل فرم را ذخیره می‌کند.
    button(app, body, "ساخت حساب کاربری  ←", lambda: submit(app))
    link(app, body, "حساب کاربری داری؟  ورود", lambda: app.show_view("login"), anchor="e")
    app.reg_ans_entry.bind("<Return>", lambda _event: submit(app))
    app.reg_fn_entry.focus_set()


def submit(app):
    """اطلاعات فرم را به پایگاه داده می‌فرستد و نتیجه را نشان می‌دهد."""
    # مقادیر فرم را جمع می‌کنیم و به تابع ثبت‌نام در database.py می‌فرستیم.
    full_name = value(app.reg_fn_entry).strip()
    username = value(app.reg_user_entry).strip()
    password = value(app.reg_pass_entry)
    answer = value(app.reg_ans_entry).strip()
    success, text = register_user(username, password, full_name, app.reg_sq_var.get().strip(), answer)
    show_status(app, text, error=not success)
    if success:
        app.root.after(1200, lambda: app.show_view("login"))
