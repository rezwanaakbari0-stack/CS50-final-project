import sqlite3
from pathlib import Path
from flask import Flask, render_template, request, jsonify, g

BASE = Path(__file__).parent
DB_PATH = BASE / "messages.db"

app = Flask(__name__)

LESSONS = [
    {"id": 1, "icon": "🩺", "title": "کمک‌های اولیه در حادثه", "text": "قبل از رسیدن آمبولانس چه کنیم؟", "category": "سلامت"},
    {"id": 2, "icon": "🧼", "title": "بهداشت فردی", "text": "عادت‌های ساده برای پیشگیری از بیماری.", "category": "سلامت"},
    {"id": 3, "icon": "🫀", "title": "آشنایی با آناتومی", "text": "بدن انسان به زبان ساده.", "category": "سلامت"},
    {"id": 4, "icon": "🌐", "title": "اولین صفحه HTML", "text": "ساخت صفحه وب با چند خط کد.", "category": "کدنویسی"},
    {"id": 5, "icon": "🎨", "title": "استایل با CSS", "text": "رنگ، فونت و چیدمان زیبا.", "category": "کدنویسی"},
    {"id": 6, "icon": "🐍", "title": "شروع پایتون", "text": "متغیر، شرط و حلقه.", "category": "کدنویسی"},
    {"id": 7, "icon": "🎤", "title": "ارائه به انگلیسی", "text": "ساختار یک ارائه‌ی موفق.", "category": "زبان"},
    {"id": 8, "icon": "📖", "title": "لغات پرکاربرد", "text": "۱۰۰ واژه‌ی ضروری روزمره.", "category": "زبان"},
]

COURSES = [
    {"icon": "🩺", "title": "کمک‌های اولیه", "text": "نجات جان در لحظه‌های حساس.", "sessions": 8, "level": "مبتدی", "perks": "گواهی پایان دوره"},
    {"icon": "💻", "title": "مبانی وب", "text": "HTML، CSS و جاوااسکریپت از صفر.", "sessions": 12, "level": "مبتدی", "perks": "پروژه عملی"},
    {"icon": "🗣️", "title": "انگلیسی مکالمه", "text": "صحبت و ارائه با اعتمادبه‌نفس.", "sessions": 10, "level": "متوسط", "perks": "تمرین گروهی"},
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)


# Home page: both endpoint names work
@app.route("/", endpoint="index")
@app.route("/", endpoint="home")
def home():
    return render_template(
        "index.html",
        page="home",
        lessons=LESSONS[:3],
        courses=COURSES
    )


@app.route("/lessons")
def lessons():
    categories = sorted({l["category"] for l in LESSONS})
    return render_template(
        "lessons.html",
        page="lessons",
        categories=categories
    )


@app.route("/courses")
def courses():
    return render_template(
        "courses.html",
        page="courses",
        courses=COURSES
    )


@app.route("/contact")
def contact():
    return render_template(
        "contact.html",
        page="contact"
    )


@app.route("/api/lessons")
def api_lessons():
    category = request.args.get("category", "all")

    items = (
        LESSONS if category == "all"
        else [l for l in LESSONS if l["category"] == category]
    )

    return jsonify(items)


@app.route("/api/contact", methods=["POST"])
def api_contact():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    message = str(data.get("message", "")).strip()

    if not name or "@" not in email or not message:
        return jsonify(
            ok=False,
            error="لطفاً همه‌ی فیلدها را درست پر کنید."
        ), 400

    if len(name) > 100 or len(email) > 200 or len(message) > 3000:
        return jsonify(
            ok=False,
            error="متن شما بیش از حد طولانی است."
        ), 400

    db = get_db()

    db.execute(
        "INSERT INTO messages (name, email, message) VALUES (?, ?, ?)",
        (name, email, message)
    )

    db.commit()

    return jsonify(ok=True)


init_db()


if __name__ == "__main__":
    app.run(debug=True)