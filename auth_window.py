"""مدیریت پنجره و جابه‌جایی بین صفحه‌های ورود، ثبت‌نام و بازیابی رمز."""

import ctypes
import os
import tkinter as tk
from tkinter import messagebox

from database import init_db
from screens import forgot_password, login, register
from ui_assets import draw_vertical_gradient


APP_DIR = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(APP_DIR, "fonts")


def _enable_windows_dpi():
    """تنظیم وضوح نمایش و بارگذاری قلم‌های همراه برنامه در ویندوز."""
    try:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    try:
        for filename in ("Vazirmatn.ttf", "Estedad.ttf"):
            path = os.path.join(FONT_DIR, filename)
            if os.path.exists(path):
                ctypes.windll.gdi32.AddFontResourceW(path)
    except Exception:
        pass


_enable_windows_dpi()


class LuxuryAuthApp:
    """پنجره را می‌سازد و صفحهٔ فعال را مدیریت می‌کند."""

    # رنگ‌های اصلی رابط؛ برای تغییر رنگ کلی، مقدارهای این بخش را ویرایش کن.
    COLORS = {
        "page": "#f4f1f3",
        "paper": "#ffffff",
        "ink": "#302532",
        "muted": "#827681",
        "line": "#e9e2e8",
        "field": "#fcfafb",
        "plum": "#56334f",
        "plum_dark": "#33243a",
        "plum_mid": "#704766",
        "rose": "#e7b8d1",
        "gold": "#dfc28f",
        "success": "#25754f",
        "success_bg": "#eff8f2",
        "danger": "#a43d55",
        "danger_bg": "#fff2f4",
        "focus": "#a45e86",
    }

    def __init__(self, root):
        # root همان پنجره‌ای است که در main.py با tk.Tk() ساخته شد.
        self.root = root
        self.root.title("دیجی‌استایل | ورود به حساب")
        self.root.geometry("1160x790")
        self.root.minsize(980, 700)
        self.root.configure(bg=self.COLORS["page"])
        self.root.option_add("*Font", ("Vazirmatn", 10))

        self.current_user = None
        self.current_view = "login"
        self._build_shell()
        self.show_view("login")
        self.root.bind("<Escape>", self._escape_to_login)

    def _build_shell(self):
        """قاب اصلی، فرم سفید و پنل برند را می‌چیند."""
        stage = tk.Frame(self.root, bg=self.COLORS["page"])
        stage.pack(fill="both", expand=True, padx=30, pady=28)

        self.card = tk.Frame(
            stage,
            bg=self.COLORS["paper"],
            highlightbackground="#e7dfe6",
            highlightthickness=1,
        )
        self.card.pack(fill="both", expand=True)
        self.card.grid_rowconfigure(0, weight=1)
        self.card.grid_columnconfigure(0, weight=1)
        self.card.grid_columnconfigure(1, minsize=370, weight=0)

        self.form_container = tk.Frame(self.card, bg=self.COLORS["paper"])
        self.form_container.grid(row=0, column=0, sticky="nsew")

        self.story_canvas = tk.Canvas(
            self.card,
            width=370,
            bg=self.COLORS["plum_dark"],
            highlightthickness=0,
            bd=0,
        )
        self.story_canvas.grid(row=0, column=1, sticky="nsew")
        self.story_canvas.bind("<Configure>", self._draw_story)

    def _draw_story(self, event=None):
        """نقش‌ونگار و نوشته‌های پنل سمت راست را روی Canvas می‌کشد."""
        canvas = self.story_canvas
        width = max(1, canvas.winfo_width())
        height = max(1, canvas.winfo_height())
        if width < 100 or height < 100:
            return
        canvas.delete("all")
        draw_vertical_gradient(canvas, width, height, "#684363", "#30243a", steps=150)

        # دایره‌های تزئینی و حلقه‌های نورانی پنل برند.
        canvas.create_oval(width - 260, 78, width + 95, 433, outline="#86607c", width=1)
        canvas.create_oval(width - 218, 120, width + 55, 393, outline="#754e70", width=1)
        canvas.create_oval(width - 173, 165, width + 10, 348, outline="#8c6682", width=1)
        canvas.create_oval(width - 138, 200, width - 25, 313, fill="#563a57", outline="#ad7f9d", width=1)
        canvas.create_text(width - 82, 257, text="✦", fill=self.COLORS["gold"], font=("Segoe UI Symbol", 35))
        canvas.create_oval(38, 145, 46, 153, fill="#edc5dc", outline="")
        canvas.create_oval(width - 67, 108, width - 61, 114, fill="#dfc28f", outline="")
        canvas.create_text(width - 38, 42, text="دیجی‌استایل", anchor="e", fill="#ffffff", font=("Vazirmatn", 17, "bold"))
        canvas.create_text(width - 180, 42, text="✦", fill=self.COLORS["gold"], font=("Segoe UI Symbol", 14, "bold"))

        right = width - 38
        canvas.create_text(right, height * 0.59, text="انتخابی برای", anchor="e", fill="#e4cddd", font=("Vazirmatn", 12, "bold"))
        canvas.create_text(right, height * 0.59 + 39, text="لحظه‌های ماندگار", anchor="e", fill="#ffffff", font=("Vazirmatn", 23, "bold"))
        canvas.create_text(right, height * 0.59 + 77, text="از اینجا آغاز می‌شود", anchor="e", fill="#ffffff", font=("Vazirmatn", 17))

        description = "کالای دلخواهت را پیدا کن؛\nبا خیال راحت و تجربه‌ای ساده."
        canvas.create_text(
            right,
            height * 0.59 + 131,
            text=description,
            anchor="ne",
            justify="right",
            fill="#d8c8d5",
            font=("Vazirmatn", 10),
            spacing=7,
        )
        canvas.create_line(38, height - 72, width - 38, height - 72, fill="#765973", width=1)
        canvas.create_text(right, height - 46, text="خریدی امن  ·  انتخابی مطمئن", anchor="e", fill="#eadde8", font=("Vazirmatn", 9))

    def _escape_to_login(self, event=None):
        """با Escape از صفحه فرعی به صفحه ورود برمی‌گردد."""
        if self.current_view != "login":
            self.show_view("login")

    def _clear_form(self):
        """محتوای صفحه قبلی را پاک می‌کند تا صفحه بعدی جا بگیرد."""
        for widget in self.form_container.winfo_children():
            widget.destroy()

    def show_view(self, view_name):
        """یکی از صفحه‌های ورود، ثبت‌نام یا بازیابی رمز را نشان می‌دهد."""
        self.current_view = view_name
        self._clear_form()
        # هر شرط، نام صفحه را به تابع ساخت همان صفحه وصل می‌کند.
        # برای اضافه‌کردن صفحه، یک elif دیگر به همین الگو اضافه کن.
        if view_name == "login":
            login.build(self)
        elif view_name == "forgot":
            forgot_password.build(self)
        elif view_name == "register":
            register.build(self)

    def on_login_success(self, user):
        """پس از ورود موفق، نقش حساب را به کاربر نشان می‌دهد."""
        role = "مدیر فروشگاه" if user["role"] == "admin" else "کاربر فروشگاه"
        messagebox.showinfo("ورود موفق", f"خوش آمدی، {user['full_name']}!\nنقش حساب: {role}", parent=self.root)


if __name__ == "__main__":
    init_db()
    app_root = tk.Tk()
    app = LuxuryAuthApp(app_root)
    app_root.mainloop()
