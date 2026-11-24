"""نقطهٔ شروع برنامه؛ اجرای برنامه از تابع main آغاز می‌شود."""

import tkinter as tk

from auth_window import LuxuryAuthApp
from database import init_db


def main():
    init_db()                     # جدول‌ها و حساب مدیر نمونه را آماده کن.
    root = tk.Tk()                 # پنجرهٔ اصلی Tkinter را بساز.
    LuxuryAuthApp(root)            # رابط برنامه را به همین پنجره وصل کن.
    root.mainloop()                # پنجره را باز نگه دار و منتظر رویدادهای کاربر بمان.


if __name__ == "__main__":
    main()                         # این خط فقط هنگام اجرای مستقیم main.py انجام می‌شود.
