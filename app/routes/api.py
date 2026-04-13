from fastapi import APIRouter, Request
from pydantic import BaseModel
from typing import Optional
from app.services.nutrition import search_products
from app.services.database import get_db
from datetime import date

router = APIRouter(prefix="/api")


class CalcRequest(BaseModel):
    weight: float
    height: float
    age: int
    gender: str
    goal: str


class FoodRequest(BaseModel):
    meal_type: str
    product_name: str
    grams: float = 100
    calories: float
    protein: float
    fat: float
    carbs: float


class WaterRequest(BaseModel):
    amount_ml: int


class WeightRequest(BaseModel):
    weight: float


@router.post("/calculate")
def calculate(data: CalcRequest):
    if data.gender == "male":
        bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age + 5
    else:
        bmr = 10 * data.weight + 6.25 * data.height - 5 * data.age - 161
    multiplier = {"lose": 0.85, "maintain": 1.0, "gain": 1.15}
    calories = int(bmr * 1.55 * multiplier.get(data.goal, 1.0))
    protein = int(data.weight * 2.0)
    fat = int(calories * 0.25 / 9)
    carbs = int((calories - protein * 4 - fat * 9) / 4)
    db = get_db()
    db.execute("DELETE FROM user_settings")
    db.execute("INSERT INTO user_settings (calories, protein, fat, carbs) VALUES (?, ?, ?, ?)", (calories, protein, fat, carbs))
    db.commit()
    return {"calories": calories, "protein": protein, "fat": fat, "carbs": carbs}


@router.get("/products/search")
def products_search(q: str = "", lang: str = "ru"):
    return search_products(q, lang)


@router.get("/products")
def products(q: str = "", lang: str = "ru"):
    return search_products(q, lang)


@router.post("/food")
def add_food(data: FoodRequest):
    db = get_db()
    today = date.today().isoformat()
    db.execute(
        "INSERT INTO food_log (log_date, meal_type, product_name, grams, calories, protein, fat, carbs) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (today, data.meal_type, data.product_name, data.grams, data.calories, data.protein, data.fat, data.carbs),
    )
    db.commit()
    return {"ok": True}


@router.get("/food/today")
def food_today(meal: str = ""):
    db = get_db()
    today = date.today().isoformat()
    if meal:
        rows = db.execute(
            "SELECT id, meal_type, product_name, calories, protein, fat, carbs FROM food_log WHERE log_date = ? AND meal_type = ? ORDER BY id DESC",
            (today, meal),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT id, meal_type, product_name, calories, protein, fat, carbs FROM food_log WHERE log_date = ? ORDER BY id DESC",
            (today,),
        ).fetchall()
    result = []
    for r in rows:
        result.append({"id": r[0], "meal_type": r[1], "product_name": r[2], "calories": r[3], "protein": r[4], "fat": r[5], "carbs": r[6]})
    return result


@router.delete("/food/{food_id}")
def delete_food(food_id: int):
    db = get_db()
    db.execute("DELETE FROM food_log WHERE id = ?", (food_id,))
    db.commit()
    return {"ok": True}


@router.post("/water")
def add_water(data: WaterRequest):
    db = get_db()
    db.execute("INSERT INTO water_log (amount_ml) VALUES (?)", (data.amount_ml,))
    db.commit()
    return {"ok": True}


@router.get("/water/today")
def water_today():
    db = get_db()
    today = date.today().isoformat()
    rows = db.execute(
        "SELECT id, amount_ml, created_at FROM water_log WHERE DATE(created_at) = ? ORDER BY id DESC",
        (today,),
    ).fetchall()
    return [{"id": r[0], "amount_ml": r[1], "created_at": r[2]} for r in rows]



@router.delete("/water/undo")
def undo_water():
    db = get_db()
    today = date.today().isoformat()
    last = db.execute(
        "SELECT id FROM water_log WHERE DATE(created_at) = ? ORDER BY id DESC LIMIT 1",
        (today,),
    ).fetchone()
    if last:
        db.execute("DELETE FROM water_log WHERE id = ?", (last[0],))
        db.commit()
    return {"ok": True}


@router.delete("/water/{water_id}")
def delete_water(water_id: int):
    db = get_db()
    db.execute("DELETE FROM water_log WHERE id = ?", (water_id,))
    db.commit()
    return {"ok": True}




@router.post("/weight")
def add_weight(data: WeightRequest):
    db = get_db()
    today = date.today().isoformat()
    db.execute("INSERT INTO weight_log (weight, log_date) VALUES (?, ?)", (data.weight, today))
    db.commit()
    return {"ok": True}


@router.get("/weight/history")
def weight_history():
    db = get_db()
    rows = db.execute("SELECT id, weight, log_date FROM weight_log ORDER BY id ASC LIMIT 30").fetchall()
    return [{"id": r[0], "weight": r[1], "log_date": r[2]} for r in rows]


@router.delete("/weight/{weight_id}")
def delete_weight(weight_id: int):
    db = get_db()
    db.execute("DELETE FROM weight_log WHERE id = ?", (weight_id,))
    db.commit()
    return {"ok": True}


@router.get("/summary")
def summary():
    db = get_db()
    today = date.today().isoformat()
    settings = db.execute("SELECT calories, protein, fat, carbs FROM user_settings LIMIT 1").fetchone()
    if settings:
        target = {"calories": settings[0], "protein": settings[1], "fat": settings[2], "carbs": settings[3]}
    else:
        target = {"calories": 2000, "protein": 150, "fat": 70, "carbs": 200}
    eaten = db.execute(
        "SELECT COALESCE(SUM(calories),0), COALESCE(SUM(protein),0), COALESCE(SUM(fat),0), COALESCE(SUM(carbs),0) FROM food_log WHERE log_date = ?",
        (today,),
    ).fetchone()
    water = db.execute(
        "SELECT COALESCE(SUM(amount_ml),0) FROM water_log WHERE DATE(created_at) = ?",
        (today,),
    ).fetchone()
    return {
        "target": target,
        "eaten": {"calories": int(eaten[0]), "protein": int(eaten[1]), "fat": int(eaten[2]), "carbs": int(eaten[3])},
        "water_ml": water[0],
        "water_target": 2500,
    }


@router.delete("/reset/today")
def reset_today():
    db = get_db()
    today = date.today().isoformat()
    db.execute("DELETE FROM food_log WHERE log_date = ?", (today,))
    db.execute("DELETE FROM water_log WHERE DATE(created_at) = ?", (today,))
    db.execute("DELETE FROM day_plan WHERE plan_date = ?", (today,))
    db.commit()
    return {"ok": True}


@router.get("/goals/streak")
def get_streak():
    db = get_db()
    from datetime import timedelta
    today = date.today()
    streak = 0
    d = today - timedelta(days=1)
    while True:
        ds = d.strftime("%Y-%m-%d")
        food = db.execute("SELECT COUNT(*) FROM food_log WHERE log_date=?", (ds,)).fetchone()
        if food and food[0] > 0:
            streak += 1
            d -= timedelta(days=1)
        else:
            break
    today_food = db.execute("SELECT COUNT(*) FROM food_log WHERE log_date=?", (today.strftime("%Y-%m-%d"),)).fetchone()
    if today_food and today_food[0] > 0:
        streak += 1
    return {"streak": streak}


@router.post("/goals/weight")
def set_goal_weight(data: dict):
    db = get_db()
    db.execute("DELETE FROM goals WHERE goal_type='weight'")
    db.execute("INSERT INTO goals (goal_type, target_value) VALUES ('weight', ?)", (data["target_weight"],))
    db.commit()
    return {"ok": True}


@router.get("/goals/weight")
def get_goal_weight():
    db = get_db()
    goal = db.execute("SELECT target_value FROM goals WHERE goal_type='weight' LIMIT 1").fetchone()
    if not goal:
        return {"target_weight": None}
    target = goal[0]
    weights = db.execute("SELECT weight FROM weight_log ORDER BY id ASC").fetchall()
    start_w = weights[0][0] if weights else None
    current_w = weights[-1][0] if weights else None
    return {"target_weight": target, "start_weight": start_w, "current_weight": current_w}


@router.get("/goals/achievements")
def get_achievements():
    db = get_db()
    food_days = db.execute("SELECT COUNT(DISTINCT log_date) FROM food_log").fetchone()[0]
    water_days = db.execute("SELECT COUNT(DISTINCT DATE(created_at)) FROM water_log").fetchone()[0]
    weight_count = db.execute("SELECT COUNT(*) FROM weight_log").fetchone()[0]
    water_total = db.execute("SELECT COALESCE(SUM(amount_ml),0) FROM water_log").fetchone()[0]
    achievements = [
        {"key": "first_food", "icon": "\U0001f37d", "unlocked": food_days >= 1},
        {"key": "food_7days", "icon": "\U0001f4c5", "unlocked": food_days >= 7},
        {"key": "food_30days", "icon": "\U0001f3c6", "unlocked": food_days >= 30},
        {"key": "first_water", "icon": "\U0001f4a7", "unlocked": water_days >= 1},
        {"key": "water_7days", "icon": "\U0001f30a", "unlocked": water_days >= 7},
        {"key": "water_30days", "icon": "\U0001f3ca", "unlocked": water_days >= 30},
        {"key": "first_weight", "icon": "\u2696", "unlocked": weight_count >= 1},
        {"key": "weight_10", "icon": "\U0001f4ca", "unlocked": weight_count >= 10},
        {"key": "water_10l", "icon": "\U0001f6b0", "unlocked": water_total >= 10000},
        {"key": "water_50l", "icon": "\U0001f3c5", "unlocked": water_total >= 50000},
    ]
    return achievements


@router.get("/stats/calories")
def stats_calories(days: int = 7):
    db = get_db()
    from datetime import timedelta
    today = date.today()
    start = today - timedelta(days=days - 1)
    rows = db.execute(
        "SELECT log_date, SUM(calories) as total_cal, SUM(protein) as total_p, SUM(fat) as total_f, SUM(carbs) as total_c "
        "FROM food_log WHERE log_date >= ? GROUP BY log_date ORDER BY log_date",
        (start.isoformat(),),
    ).fetchall()
    data = {}
    for i in range(days):
        d = (start + timedelta(days=i)).isoformat()
        data[d] = {"date": d, "calories": 0, "protein": 0, "fat": 0, "carbs": 0}
    for r in rows:
        data[r[0]] = {"date": r[0], "calories": int(r[1]), "protein": int(r[2]), "fat": int(r[3]), "carbs": int(r[4])}
    return list(data.values())


@router.get("/stats/weight")
def stats_weight(days: int = 30):
    db = get_db()
    from datetime import timedelta
    today = date.today()
    start = today - timedelta(days=days - 1)
    rows = db.execute(
        "SELECT log_date, weight FROM weight_log WHERE log_date >= ? ORDER BY log_date",
        (start.isoformat(),),
    ).fetchall()
    return [{"date": r[0], "weight": r[1]} for r in rows]


@router.get("/stats/water")
def stats_water(days: int = 7):
    db = get_db()
    from datetime import timedelta
    today = date.today()
    start = today - timedelta(days=days - 1)
    rows = db.execute(
        "SELECT DATE(created_at) as d, SUM(amount_ml) as total FROM water_log "
        "WHERE DATE(created_at) >= ? GROUP BY DATE(created_at) ORDER BY d",
        (start.isoformat(),),
    ).fetchall()
    data = {}
    for i in range(days):
        d = (start + timedelta(days=i)).isoformat()
        data[d] = {"date": d, "water_ml": 0}
    for r in rows:
        data[r[0]] = {"date": r[0], "water_ml": int(r[1])}
    return list(data.values())


@router.get("/achievement-stats")
def achievement_stats():
    db = get_db()
    food_count = db.execute("SELECT COUNT(*) FROM food_log").fetchone()[0]
    food_days = db.execute("SELECT COUNT(DISTINCT log_date) FROM food_log").fetchone()[0]
    water_count = db.execute("SELECT COUNT(*) FROM water_log").fetchone()[0]
    water_days = db.execute("SELECT COUNT(DISTINCT DATE(created_at)) FROM water_log").fetchone()[0]
    water_total = db.execute("SELECT COALESCE(SUM(amount_ml),0) FROM water_log").fetchone()[0]
    weight_count = db.execute("SELECT COUNT(*) FROM weight_log").fetchone()[0]

    # Streak
    from datetime import timedelta
    today = date.today()
    streak = 0
    for i in range(365):
        d = today - timedelta(days=i)
        has_food = db.execute("SELECT 1 FROM food_log WHERE log_date=?", (d.isoformat(),)).fetchone()
        has_water = db.execute("SELECT 1 FROM water_log WHERE DATE(created_at)=?", (d.isoformat(),)).fetchone()
        if has_food or has_water:
            streak += 1
        else:
            if i > 0:
                break
    return {
        "food_count": food_count,
        "food_days": food_days,
        "water_count": water_count,
        "water_days": water_days,
        "water_total": water_total,
        "weight_count": weight_count,
        "streak": streak
    }


@router.delete("/reset/all")
def reset_all():
    db = get_db()
    db.execute("DELETE FROM food_log")
    db.execute("DELETE FROM water_log")
    db.execute("DELETE FROM weight_log")
    db.commit()
    return {"ok": True}


@router.get("/api/food-log/today")
async def get_today_food(request: Request):
    from app.services.auth import decode_token
    from datetime import date
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not auth"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Bad token"})
    db = get_db()
    today = date.today().isoformat()
    rows = db.execute(
        "SELECT meal_type, product_name, grams, calories, protein, fat, carbs FROM food_log WHERE user_id=? AND log_date=? ORDER BY id",
        (user_id, today)
    ).fetchall()
    result = []
    for r in rows:
        result.append({
            "meal_type": r[0],
            "name": r[1],
            "grams": r[2],
            "cal": r[3],
            "protein": r[4],
            "fat": r[5],
            "carbs": r[6]
        })
    return result


@router.get("/day-plan/today")
async def get_day_plan(request: Request):
    from app.services.auth import decode_token
    from datetime import date
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not auth"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Bad token"})
    db = get_db()
    today = date.today().isoformat()
    rows = db.execute(
        "SELECT id, meal_type, product_name, grams, calories, protein, fat, carbs, eaten, COALESCE(product_name_en,'') FROM day_plan WHERE user_id=? AND plan_date=? ORDER BY id",
        (user_id, today)
    ).fetchall()
    result = []
    for r in rows:
        result.append({
            "id": r[0], "meal_type": r[1], "name": r[2], "grams": r[3],
            "cal": r[4], "protein": r[5], "fat": r[6], "carbs": r[7], "eaten": r[8], "name_en": r[9]
        })
    return result


@router.post("/day-plan/toggle/{item_id}")
async def toggle_eaten(item_id: int, request: Request):
    from app.services.auth import decode_token
    from datetime import date
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not auth"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Bad token"})
    db = get_db()
    today = date.today().isoformat()
    row = db.execute("SELECT eaten, meal_type, product_name, grams, calories, protein, fat, carbs FROM day_plan WHERE id=? AND user_id=? AND plan_date=?", (item_id, user_id, today)).fetchone()
    if not row:
        return JSONResponse(status_code=404, content={"error": "Not found"})
    new_eaten = 0 if row[0] == 1 else 1
    db.execute("UPDATE day_plan SET eaten=? WHERE id=?", (new_eaten, item_id))
    if new_eaten == 1:
        db.execute(
            "INSERT INTO food_log (user_id, log_date, meal_type, product_name, grams, calories, protein, fat, carbs) VALUES (?,?,?,?,?,?,?,?,?)",
            (user_id, today, row[1], row[2], row[3], row[4], row[5], row[6], row[7])
        )
    else:
        db.execute(
            "DELETE FROM food_log WHERE rowid = (SELECT rowid FROM food_log WHERE user_id=? AND log_date=? AND product_name=? AND meal_type=? LIMIT 1)",
            (user_id, today, row[2], row[1])
        )
    db.commit()
    return {"ok": True, "eaten": new_eaten}
