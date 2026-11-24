"""صفحه ورود و بررسی اطلاعات حساب."""

import tkinter as tk

from database import authenticate_user
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
    """چیدمان صفحه ورود را می‌سازد."""
    # app راه دسترسی این صفحه به پنجره، رنگ‌ها و فیلدهای برنامه است.
    body = form_body(app)
    header(app, body, "ورود امن به فروشگاه", "خوش برگشتی", "وارد حساب خودت شو و ادامه بده.")
    status(app, body)
    app.login_user_entry = add_field(app, body, "نام کاربری", "نام کاربری‌ات را وارد کن", "◉", pady=13)
    app.login_pass_entry = add_field(app, body, "رمز عبور", "رمز عبور حساب", "⌑", password=True, pady=6)

    # این دو پیوند کاربر را به صفحه‌های دیگر می‌برند.
    links = tk.Frame(body, bg=app.COLORS["paper"])
    links.pack(fill="x", pady=(0, 17))
    link(app, links, "فراموشی رمز عبور؟", lambda: app.show_view("forgot"), anchor="e")
    link(app, links, "حساب ندارید؟ ثبت‌نام", lambda: app.show_view("register"), anchor="w")
    # command تابعی است که فقط پس از کلیک اجرا می‌شود.
    button(app, body, "ورود به حساب  ←", lambda: submit(app))
    tk.Label(
        body,
        text="ورود به حساب شما با اطلاعات ثبت‌شده انجام می‌شود",
        bg=app.COLORS["paper"],
        fg="#9a8d98",
        font=("Vazirmatn", 9),
    ).pack(pady=(4, 0))
    app.login_pass_entry.bind("<Return>", lambda _event: submit(app))
    app.login_user_entry.focus_set()


def submit(app):
    """اطلاعات ورود را بررسی می‌کند و نتیجه را نشان می‌دهد."""
    # اول متن ورودی‌ها را می‌خوانیم؛ بعد تابع دیتابیس حساب را بررسی می‌کند.
    username = value(app.login_user_entry).strip()
    password = value(app.login_pass_entry)
    if not username or not password:
        show_status(app, "نام کاربری و رمز عبور را وارد کن.")
        return
    user = authenticate_user(username, password)
    if not user:
        show_status(app, "نام کاربری یا رمز عبور درست نیست.")
        return
    app.current_user = user
    show_status(app, "ورود موفق بود؛ در حال آماده‌سازی حساب…", error=False)
    app.root.after(450, lambda: app.on_login_success(user))
