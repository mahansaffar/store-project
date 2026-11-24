"""توابع دیتابیس SQLite؛ صفحه‌های رابط فقط این توابع را صدا می‌زنند."""

import os
import hashlib
import sqlite3

# این فایل کنار database.py ساخته می‌شود، نه در مسیر اجرای ترمینال.
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "store.db")

def hash_password(password: str) -> str:
    """رمز را به متن هش‌شده تبدیل می‌کند تا خود رمز در جدول ذخیره نشود."""
    # برای یادگیری ساده نگه داشته شده؛ جزئیات محدودیتش در README آمده است.
    salt = "digi_luxury_salt_2026"
    return hashlib.sha256((password + salt).encode('utf-8')).hexdigest()


def get_db():
    """اتصال تازه به دیتابیس می‌دهد؛ هر تابع پس از کار باید آن را ببندد."""
    conn = sqlite3.connect(DB_PATH)
    # با این تنظیم، نتیجه را می‌توان با نام ستون خواند: row["username"]
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """جدول‌های لازم را بساز و اگر لازم بود حساب مدیر نمونه را اضافه کن."""
    conn = get_db()
    cursor = conn.cursor()

    # cursor.execute دستور SQL را اجرا می‌کند. IF NOT EXISTS جلوی ساخت دوباره را می‌گیرد.
    # جدول کاربران: اطلاعات ورود و پرسش امنیتی هر حساب.
    # هر ستون یک ویژگی از حساب کاربر است؛ id را SQLite خودکار زیاد می‌کند.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        full_name TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'user', -- 'admin' or 'user'
        security_question TEXT NOT NULL,
        security_answer TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # جدول دسته‌ها، مثل پوشاک یا کالای دیجیتال.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        icon TEXT DEFAULT '🛍️',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # جدول کالاها؛ category_id مشخص می‌کند هر کالا در کدام دسته است.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER NOT NULL,
        unique_code TEXT UNIQUE NOT NULL,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        stock INTEGER DEFAULT 10,
        description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (category_id) REFERENCES categories (id) ON DELETE CASCADE
    )
    """)

    # جدول سفارش‌ها؛ user_id سفارش را به حساب خریدار وصل می‌کند.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_code TEXT UNIQUE NOT NULL,
        total_price INTEGER NOT NULL,
        status TEXT DEFAULT 'ثبت شده',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    """)

    # هر سفارش چند ردیف کالا دارد؛ این جدول ردیف‌های فاکتور را نگه می‌دارد.
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        product_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        unit_price INTEGER NOT NULL,
        total_price INTEGER NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id)
    )
    """)

    # ابتدا می‌پرسیم مدیر نمونه وجود دارد یا نه تا هر بار یک مدیر جدید نسازیم.
    cursor.execute("SELECT id FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        admin_pass_hash = hash_password("admin123")
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, security_question, security_answer)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (
            "admin",
            admin_pass_hash,
            "مدیر کل سیستم",
            "admin",
            "نام سیستم فروشگاهی شما چیست؟",
            "دیجی استایل"
        ))
        print("Default admin created: username='admin', password='admin123'")

    conn.commit()  # تغییرهای ساخت جدول و مدیر را روی دیسک ذخیره می‌کند.
    conn.close()   # اتصال دیتابیس را پس از پایان کار می‌بندد.


def authenticate_user(username, password):
    """اگر نام کاربری و رمز درست باشند، اطلاعات حساب را برمی‌گرداند؛ وگرنه None."""
    conn = get_db()
    cursor = conn.cursor()
    # علامت سؤال جای مقدار ورودی است؛ مقدار را داخل متن SQL نچسبان.
    cursor.execute("SELECT * FROM users WHERE username = ?", (username.strip(),))
    # fetchone یک ردیف می‌دهد؛ اگر نام پیدا نشود، نتیجه None است.
    user = cursor.fetchone()
    conn.close()
    # هم نام کاربری و هم هش رمز باید با اطلاعات ذخیره‌شده برابر باشند.
    if user and user["password_hash"] == hash_password(password):
        # Row شبیه دیکشنری است؛ تبدیلش می‌کنیم تا لایهٔ رابط راحت استفاده کند.
        return dict(user)
    return None


def register_user(username, password, full_name, security_question, security_answer):
    """کاربر عادی را می‌سازد و (موفقیت، پیام برای نمایش) برمی‌گرداند."""
    username = username.strip()
    # بررسی سادهٔ ورودی‌ها پیش از بازکردن اتصال دیتابیس.
    if not username or not password or not full_name:
        return False, "لطفاً تمامی فیلدهای ستاره‌دار را تکمیل کنید."
    
    if len(password) < 4:
        return False, "رمز عبور باید حداقل ۴ کاراکتر باشد."

    conn = get_db()
    cursor = conn.cursor()
    # اگر درج اطلاعات به خطا بخورد، except اتصال را می‌بندد و پیام می‌دهد.
    try:
        # نام کاربری باید یکتا باشد؛ اگر پیدا شد، ادامهٔ ثبت‌نام را متوقف می‌کنیم.
        cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
        if cursor.fetchone():
            conn.close()
            return False, "این نام کاربری قبلاً در سیستم ثبت شده است."

        pwd_hash = hash_password(password)
        # هر ? با یک مقدار از tuple پایین جایگزین می‌شود.
        cursor.execute("""
        INSERT INTO users (username, password_hash, full_name, role, security_question, security_answer)
        VALUES (?, ?, ?, 'user', ?, ?)
        """, (username, pwd_hash, full_name.strip(), security_question.strip(), security_answer.strip().lower()))
        conn.commit()  # INSERT را ذخیره کن.
        conn.close()   # کار تمام شد؛ اتصال را ببند.
        return True, "حساب کاربری شما با موفقیت ایجاد گردید."
    except Exception as e:
        conn.close()  # حتی اگر ثبت‌نام خطا داد، اتصال را باز نگه ندار.
        return False, f"خطا در ثبت‌نام: {str(e)}"


def get_user_security_question(username):
    """پرسش امنیتی حساب را می‌دهد؛ اگر کاربر نباشد، None برمی‌گرداند."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT security_question FROM users WHERE username = ?", (username.strip(),))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row["security_question"]
    return None


def reset_user_password(username, security_answer, new_password):
    """پاسخ امنیتی را می‌سنجد و در صورت درستی، هش رمز را عوض می‌کند."""
    username = username.strip()
    security_answer = security_answer.strip().lower()
    
    if len(new_password) < 4:
        return False, "رمز عبور جدید باید حداقل ۴ کاراکتر باشد."

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT security_answer FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return False, "کاربری با این مشخصات یافت نشد."

    stored_answer = row["security_answer"].strip().lower()
    if stored_answer != security_answer:
        conn.close()
        return False, "پاسخ سوال امنیتی نادرست است."

    # پاسخ درست بود؛ رمز تازه را هش می‌کنیم و جای هش قبلی می‌گذاریم.
    new_hash = hash_password(new_password)
    cursor.execute("UPDATE users SET password_hash = ? WHERE username = ?", (new_hash, username))
    conn.commit()  # UPDATE را روی فایل دیتابیس ذخیره کن.
    conn.close()   # اتصال دیتابیس دیگر لازم نیست.
    return True, "رمز عبور با موفقیت به‌روزرسانی شد. اکنون وارد شوید."

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")

