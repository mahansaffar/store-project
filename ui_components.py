"""اجزای مشترک صفحه‌ها؛ ظاهر فیلد، دکمه و پیام‌ها از اینجا تنظیم می‌شود."""

import tkinter as tk


def form_body(app):
    """قاب سفید و فاصله‌های داخلی هر فرم را می‌سازد."""
    body = tk.Frame(app.form_container, bg=app.COLORS["paper"])
    body.pack(fill="both", expand=True, padx=48, pady=(32, 26))
    return body


def header(app, parent, badge, title, subtitle):
    """نشان کوچک، عنوان و توضیح بالای هر صفحه را می‌سازد."""
    badge_box = tk.Frame(parent, bg="#faf4f8", highlightbackground="#eee1e9", highlightthickness=1)
    badge_box.pack(anchor="e", pady=(0, 11))
    tk.Label(
        badge_box,
        text=f"✦  {badge}",
        bg="#faf4f8",
        fg=app.COLORS["plum_mid"],
        font=("Vazirmatn", 9, "bold"),
        padx=12,
        pady=4,
    ).pack()
    tk.Label(
        parent,
        text=title,
        bg=app.COLORS["paper"],
        fg=app.COLORS["ink"],
        font=("Vazirmatn", 22, "bold"),
        anchor="e",
    ).pack(fill="x", anchor="e")
    tk.Label(
        parent,
        text=subtitle,
        bg=app.COLORS["paper"],
        fg=app.COLORS["muted"],
        font=("Vazirmatn", 10),
        anchor="e",
    ).pack(fill="x", anchor="e", pady=(2, 15))


def add_field(app, parent, label, hint="", icon="◇", password=False, pady=7):
    """یک عنوان و ورودی هم‌شکل با بقیه فرم‌ها می‌سازد."""
    group = tk.Frame(parent, bg=app.COLORS["paper"])
    # pack یعنی ویجت را داخل قاب بگذار؛ fill="x" عرض قاب را پر می‌کند.
    group.pack(fill="x", pady=(0, pady))
    tk.Label(
        group,
        text=label,
        bg=app.COLORS["paper"],
        fg=app.COLORS["ink"],
        font=("Vazirmatn", 10, "bold"),
        anchor="e",
    ).pack(fill="x", pady=(0, 3))

    shell = tk.Frame(
        group,
        bg=app.COLORS["field"],
        height=42,
        highlightbackground=app.COLORS["line"],
        highlightcolor=app.COLORS["focus"],
        highlightthickness=1,
    )
    shell.pack(fill="x")
    shell.pack_propagate(False)
    icon_label = tk.Label(
        shell,
        text=icon,
        bg=app.COLORS["field"],
        fg="#987b91",
        font=("Segoe UI Symbol", 12),
        width=3,
    )
    icon_label.pack(side="right", fill="y", padx=(4, 7))

    entry = tk.Entry(
        shell,
        bd=0,
        relief="flat",
        bg=app.COLORS["field"],
        fg=app.COLORS["ink"],
        insertbackground=app.COLORS["plum"],
        selectbackground="#dec5d6",
        selectforeground=app.COLORS["ink"],
        font=("Vazirmatn", 10),
        justify="right",
        show="●" if password else "",
    )
    entry._hint = hint
    # این علامت‌ها اطلاعات کمکی همین ورودی‌اند: متن راهنما، رمز بودن و وضعیت نمایش رمز.
    # نام‌هایی که با _ شروع می‌شوند، جزئیات داخلی این جزء هستند.
    entry._placeholder_active = False
    entry._password = password
    entry._revealed = False
    if password:
        eye = tk.Button(
            shell,
            text="◉",
            command=lambda e=entry: toggle_password(app, e),
            bg=app.COLORS["field"],
            activebackground=app.COLORS["field"],
            fg="#8a7385",
            activeforeground=app.COLORS["plum"],
            bd=0,
            relief="flat",
            cursor="hand2",
            font=("Segoe UI Symbol", 11),
            padx=8,
        )
        eye.pack(side="left")
    entry.pack(side="left", fill="both", expand=True, padx=(12, 2), pady=2)

    # bind یک رویداد Tkinter را به تابع وصل می‌کند؛ اینجا کلیک یا Tab وارد فیلد می‌شود.
    def on_focus_in(_event):
        shell.configure(highlightbackground=app.COLORS["focus"])
        if entry._placeholder_active:
            entry.delete(0, "end")
            entry._placeholder_active = False
            if entry._revealed:
                entry.configure(fg=app.COLORS["ink"], show="")
            elif entry._password:
                entry.configure(fg=app.COLORS["ink"], show="●")
            else:
                entry.configure(fg=app.COLORS["ink"], show="")

    # وقتی کاربر فیلد را ترک می‌کند، اگر خالی باشد متن راهنما دوباره نمایش داده می‌شود.
    def on_focus_out(_event):
        shell.configure(highlightbackground=app.COLORS["line"])
        if not entry.get() and entry._hint:
            entry.configure(show="", fg="#a69aa4")
            entry.insert(0, entry._hint)
            entry._placeholder_active = True

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)
    if hint:
        entry.configure(show="", fg="#a69aa4")
        entry.insert(0, hint)
        entry._placeholder_active = True
    return entry


def value(entry):
    """متن واقعی ورودی را می‌دهد و متن راهنما را نادیده می‌گیرد."""
    # متن خاکستری فقط راهنماست و نباید به‌عنوان نام کاربری یا رمز ذخیره شود.
    if getattr(entry, "_placeholder_active", False):
        return ""
    return entry.get()


def toggle_password(app, entry):
    """نمایش یا پنهان‌کردن رمز داخل همان فیلد."""
    entry._revealed = not entry._revealed
    if not entry._placeholder_active:
        entry.configure(show="" if entry._revealed else "●")


def button(app, parent, text, command, secondary=False):
    """دکمه اصلی یا دکمه کم‌رنگ‌تر با واکنش هنگام رفتن ماوس روی آن."""
    bg = "#f8f2f6" if secondary else app.COLORS["plum"]
    hover = "#efe2eb" if secondary else app.COLORS["plum_mid"]
    fg = app.COLORS["plum"] if secondary else "#ffffff"
    button_widget = tk.Button(
        parent,
        text=text,
        command=command,
        bg=bg,
        activebackground=hover,
        fg=fg,
        activeforeground=fg,
        disabledforeground="#bdb4bb",
        bd=0,
        relief="flat",
        cursor="hand2",
        font=("Vazirmatn", 11, "bold"),
        height=2 if not secondary else 1,
        highlightthickness=0,
    )
    button_widget.pack(fill="x", pady=(3, 9) if not secondary else (0, 0))
    # lambda اجرای تغییر رنگ را تا لحظهٔ ورود ماوس به دکمه عقب می‌اندازد.
    button_widget.bind("<Enter>", lambda _event: button_widget.configure(bg=hover))
    button_widget.bind("<Leave>", lambda _event: button_widget.configure(bg=bg))
    return button_widget


def link(app, parent, text, command, anchor="e"):
    """پیوند متنی قابل کلیک، مثل «فراموشی رمز عبور؟»."""
    label = tk.Label(
        parent,
        text=text,
        bg=app.COLORS["paper"],
        fg=app.COLORS["plum_mid"],
        font=("Vazirmatn", 9, "bold"),
        cursor="hand2",
    )
    label.pack(side="right" if anchor == "e" else "left")
    label.bind("<Button-1>", lambda _event: command())
    label.bind("<Enter>", lambda _event: label.configure(fg=app.COLORS["focus"]))
    label.bind("<Leave>", lambda _event: label.configure(fg=app.COLORS["plum_mid"]))
    return label


def status(app, parent):
    """جای پیام موفقیت یا خطا را بالای فیلدها نگه می‌دارد."""
    app.status_label = tk.Label(
        parent,
        text="",
        bg=app.COLORS["paper"],
        fg=app.COLORS["danger"],
        font=("Vazirmatn", 9),
        anchor="e",
        justify="right",
        wraplength=520,
        height=1,
    )
    app.status_label.pack(fill="x", pady=(0, 5))


def show_status(app, text, error=True):
    """پیام صفحه را با رنگ خطا یا موفقیت نشان می‌دهد."""
    app.status_label.configure(
        text=f"{('!  ' if error else '✓  ')}{text}",
        fg=app.COLORS["danger"] if error else app.COLORS["success"],
        bg=app.COLORS["danger_bg"] if error else app.COLORS["success_bg"],
        padx=10,
        pady=5,
    )
