from app.services.database import get_db

db = get_db()

db.execute('''CREATE TABLE IF NOT EXISTS day_plan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER DEFAULT 0,
    plan_date TEXT NOT NULL,
    meal_type TEXT NOT NULL,
    product_name TEXT,
    grams REAL DEFAULT 100,
    calories REAL DEFAULT 0,
    protein REAL DEFAULT 0,
    fat REAL DEFAULT 0,
    carbs REAL DEFAULT 0,
    eaten INTEGER DEFAULT 0
)''')

db.commit()
print("day_plan table created")