from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from app.services.auth import decode_token
from app.services.database import get_db
import json

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

MEAL_PLANS = [
    {
        "id": 1,
        "name": "Сбалансированный день",
        "name_en": "Balanced Day",
        "description": "Идеальный рацион на каждый день",
        "description_en": "Perfect daily nutrition plan",
        "icon": "🥗",
        "total_cal": 2100,
        "total_protein": 140,
        "total_fat": 70,
        "total_carbs": 230,
        "meals": [
            {
                "type": "breakfast",
                "type_name": "Завтрак",
                "type_name_en": "Breakfast",
                "icon": "🌅",
                "items": [
                    {"name": "Овсянка с бананом", "name_en": "Oatmeal with banana", "cal": 350, "protein": 12, "fat": 8, "carbs": 58},
                    {"name": "Яйцо варёное 2шт", "name_en": "Boiled eggs x2", "cal": 155, "protein": 13, "fat": 11, "carbs": 1},
                    {"name": "Чай зелёный", "name_en": "Green tea", "cal": 5, "protein": 0, "fat": 0, "carbs": 1}
                ]
            },
            {
                "type": "lunch",
                "type_name": "Обед",
                "type_name_en": "Lunch",
                "icon": "☀️",
                "items": [
                    {"name": "Куриная грудка 200г", "name_en": "Chicken breast 200g", "cal": 330, "protein": 62, "fat": 7, "carbs": 0},
                    {"name": "Гречка 150г", "name_en": "Buckwheat 150g", "cal": 200, "protein": 8, "fat": 3, "carbs": 38},
                    {"name": "Салат овощной", "name_en": "Vegetable salad", "cal": 80, "protein": 2, "fat": 5, "carbs": 8}
                ]
            },
            {
                "type": "snack",
                "type_name": "Перекус",
                "type_name_en": "Snack",
                "icon": "🍎",
                "items": [
                    {"name": "Творог 5% 200г", "name_en": "Cottage cheese 5% 200g", "cal": 240, "protein": 30, "fat": 10, "carbs": 6},
                    {"name": "Яблоко", "name_en": "Apple", "cal": 80, "protein": 0, "fat": 0, "carbs": 20}
                ]
            },
            {
                "type": "dinner",
                "type_name": "Ужин",
                "type_name_en": "Dinner",
                "icon": "🌙",
                "items": [
                    {"name": "Рыба запечённая 200г", "name_en": "Baked fish 200g", "cal": 280, "protein": 40, "fat": 12, "carbs": 0},
                    {"name": "Рис 100г", "name_en": "Rice 100g", "cal": 130, "protein": 3, "fat": 0, "carbs": 28},
                    {"name": "Брокколи 150г", "name_en": "Broccoli 150g", "cal": 50, "protein": 5, "fat": 1, "carbs": 6}
                ]
            }
        ]
    },
    {
        "id": 2,
        "name": "Высокобелковый",
        "name_en": "High Protein",
        "description": "Для набора мышечной массы",
        "description_en": "For muscle gain",
        "icon": "💪",
        "total_cal": 2500,
        "total_protein": 200,
        "total_fat": 80,
        "total_carbs": 220,
        "meals": [
            {
                "type": "breakfast",
                "type_name": "Завтрак",
                "type_name_en": "Breakfast",
                "icon": "🌅",
                "items": [
                    {"name": "Омлет из 4 яиц", "name_en": "4-egg omelette", "cal": 400, "protein": 28, "fat": 30, "carbs": 2},
                    {"name": "Тост цельнозерновой 2шт", "name_en": "Whole grain toast x2", "cal": 180, "protein": 8, "fat": 2, "carbs": 34},
                    {"name": "Протеиновый коктейль", "name_en": "Protein shake", "cal": 200, "protein": 35, "fat": 3, "carbs": 8}
                ]
            },
            {
                "type": "lunch",
                "type_name": "Обед",
                "type_name_en": "Lunch",
                "icon": "☀️",
                "items": [
                    {"name": "Говядина 250г", "name_en": "Beef 250g", "cal": 500, "protein": 65, "fat": 25, "carbs": 0},
                    {"name": "Макароны 150г", "name_en": "Pasta 150g", "cal": 250, "protein": 9, "fat": 2, "carbs": 50},
                    {"name": "Овощной микс", "name_en": "Veggie mix", "cal": 60, "protein": 3, "fat": 1, "carbs": 10}
                ]
            },
            {
                "type": "snack",
                "type_name": "Перекус",
                "type_name_en": "Snack",
                "icon": "🍎",
                "items": [
                    {"name": "Греческий йогурт 300г", "name_en": "Greek yogurt 300g", "cal": 200, "protein": 30, "fat": 6, "carbs": 12},
                    {"name": "Орехи 30г", "name_en": "Nuts 30g", "cal": 180, "protein": 5, "fat": 16, "carbs": 4}
                ]
            },
            {
                "type": "dinner",
                "type_name": "Ужин",
                "type_name_en": "Dinner",
                "icon": "🌙",
                "items": [
                    {"name": "Лосось 200г", "name_en": "Salmon 200g", "cal": 400, "protein": 40, "fat": 25, "carbs": 0},
                    {"name": "Картофель 200г", "name_en": "Potato 200g", "cal": 160, "protein": 4, "fat": 0, "carbs": 36},
                    {"name": "Шпинат тушёный", "name_en": "Sauteed spinach", "cal": 50, "protein": 5, "fat": 2, "carbs": 4}
                ]
            }
        ]
    },
    {
        "id": 3,
        "name": "Лёгкий для похудения",
        "name_en": "Light Weight Loss",
        "description": "Дефицит калорий без голода",
        "description_en": "Calorie deficit without hunger",
        "icon": "🔥",
        "total_cal": 1500,
        "total_protein": 120,
        "total_fat": 45,
        "total_carbs": 150,
        "meals": [
            {
                "type": "breakfast",
                "type_name": "Завтрак",
                "type_name_en": "Breakfast",
                "icon": "🌅",
                "items": [
                    {"name": "Творог 2% 150г с ягодами", "name_en": "Cottage cheese 2% 150g with berries", "cal": 180, "protein": 22, "fat": 3, "carbs": 16},
                    {"name": "Кофе без сахара", "name_en": "Coffee no sugar", "cal": 5, "protein": 0, "fat": 0, "carbs": 1}
                ]
            },
            {
                "type": "lunch",
                "type_name": "Обед",
                "type_name_en": "Lunch",
                "icon": "☀️",
                "items": [
                    {"name": "Индейка 200г", "name_en": "Turkey 200g", "cal": 300, "protein": 50, "fat": 10, "carbs": 0},
                    {"name": "Киноа 100г", "name_en": "Quinoa 100g", "cal": 150, "protein": 6, "fat": 2, "carbs": 27},
                    {"name": "Салат с огурцом и помидором", "name_en": "Cucumber tomato salad", "cal": 50, "protein": 2, "fat": 2, "carbs": 6}
                ]
            },
            {
                "type": "snack",
                "type_name": "Перекус",
                "type_name_en": "Snack",
                "icon": "🍎",
                "items": [
                    {"name": "Кефир 1% 250мл", "name_en": "Kefir 1% 250ml", "cal": 100, "protein": 8, "fat": 2, "carbs": 10},
                    {"name": "Морковь", "name_en": "Carrot", "cal": 40, "protein": 1, "fat": 0, "carbs": 9}
                ]
            },
            {
                "type": "dinner",
                "type_name": "Ужин",
                "type_name_en": "Dinner",
                "icon": "🌙",
                "items": [
                    {"name": "Треска на пару 200г", "name_en": "Steamed cod 200g", "cal": 200, "protein": 40, "fat": 2, "carbs": 0},
                    {"name": "Кабачки запечённые 200г", "name_en": "Baked zucchini 200g", "cal": 50, "protein": 3, "fat": 1, "carbs": 8},
                    {"name": "Зелёный салат", "name_en": "Green salad", "cal": 30, "protein": 2, "fat": 1, "carbs": 4}
                ]
            }
        ]
    },
    {
        "id": 4,
        "name": "Вегетарианский",
        "name_en": "Vegetarian",
        "description": "Полноценный рацион без мяса",
        "description_en": "Complete nutrition without meat",
        "icon": "🌿",
        "total_cal": 1900,
        "total_protein": 90,
        "total_fat": 65,
        "total_carbs": 250,
        "meals": [
            {
                "type": "breakfast",
                "type_name": "Завтрак",
                "type_name_en": "Breakfast",
                "icon": "🌅",
                "items": [
                    {"name": "Гранола с молоком", "name_en": "Granola with milk", "cal": 350, "protein": 10, "fat": 12, "carbs": 52},
                    {"name": "Банан", "name_en": "Banana", "cal": 100, "protein": 1, "fat": 0, "carbs": 26}
                ]
            },
            {
                "type": "lunch",
                "type_name": "Обед",
                "type_name_en": "Lunch",
                "icon": "☀️",
                "items": [
                    {"name": "Чечевичный суп 300мл", "name_en": "Lentil soup 300ml", "cal": 250, "protein": 18, "fat": 5, "carbs": 35},
                    {"name": "Хлеб цельнозерновой 2шт", "name_en": "Whole grain bread x2", "cal": 180, "protein": 8, "fat": 2, "carbs": 34},
                    {"name": "Хумус 50г", "name_en": "Hummus 50g", "cal": 120, "protein": 6, "fat": 7, "carbs": 10}
                ]
            },
            {
                "type": "snack",
                "type_name": "Перекус",
                "type_name_en": "Snack",
                "icon": "🍎",
                "items": [
                    {"name": "Тофу жареный 150г", "name_en": "Fried tofu 150g", "cal": 200, "protein": 18, "fat": 12, "carbs": 4},
                    {"name": "Апельсин", "name_en": "Orange", "cal": 60, "protein": 1, "fat": 0, "carbs": 14}
                ]
            },
            {
                "type": "dinner",
                "type_name": "Ужин",
                "type_name_en": "Dinner",
                "icon": "🌙",
                "items": [
                    {"name": "Паста с грибами", "name_en": "Mushroom pasta", "cal": 380, "protein": 14, "fat": 10, "carbs": 58},
                    {"name": "Салат с авокадо", "name_en": "Avocado salad", "cal": 200, "protein": 4, "fat": 16, "carbs": 10}
                ]
            }
        ]
    }
]


@router.get("/meal-plans", response_class=HTMLResponse)
async def meal_plans_page(request: Request):
    return templates.TemplateResponse("meal_plans.html", {"request": request})


@router.get("/api/meal-plans")
async def get_meal_plans():
    return MEAL_PLANS


@router.get("/api/meal-plans/{plan_id}")
async def get_meal_plan(plan_id: int):
    for p in MEAL_PLANS:
        if p["id"] == plan_id:
            return p
    return JSONResponse(status_code=404, content={"error": "Plan not found"})


@router.post("/api/meal-plans/{plan_id}/apply")
async def apply_meal_plan(plan_id: int, request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    plan = None
    for p in MEAL_PLANS:
        if p["id"] == plan_id:
            plan = p
            break
    if not plan:
        return JSONResponse(status_code=404, content={"error": "Plan not found"})

    from datetime import date
    import random
    today_date = date.today()
    today = today_date.isoformat()
    db = get_db()

    # Use day-of-week seed for variety
    day_of_week = today_date.weekday()  # 0=Mon, 6=Sun
    base_meals = plan["meals"]

    # Shuffle items within each meal based on day
    rng = random.Random(plan_id * 100 + day_of_week)
    shuffled_meals = []
    for meal in base_meals:
        items = list(meal["items"])
        rng.shuffle(items)
        # Swap some items between days by rotating
        rotated = items[day_of_week % len(items):] + items[:day_of_week % len(items)]
        shuffled_meals.append({"type": meal["type"], "items": rotated})

    try:
        db.execute("DELETE FROM day_plan WHERE user_id=? AND plan_date=?", (user_id, today))
        for meal in shuffled_meals:
            for item in meal["items"]:
                db.execute(
                    "INSERT INTO day_plan (user_id, plan_date, meal_type, product_name, product_name_en, grams, calories, protein, fat, carbs, eaten) VALUES (?,?,?,?,?,?,?,?,?,?,0)",
                    (user_id, today, meal["type"], item["name"], item.get("name_en",""), 100, item["cal"], item["protein"], item["fat"], item["carbs"])
                )
        db.commit()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    return {"ok": True, "message": "Plan applied", "total_cal": plan["total_cal"]}
