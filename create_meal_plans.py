import os

# 1. Create meal plans route
os.makedirs('app/routes', exist_ok=True)

route_code = '''from fastapi import APIRouter, Request
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
    today = date.today().isoformat()
    db = get_db()

    for meal in plan["meals"]:
        for item in meal["items"]:
            db.execute(
                "INSERT INTO food_log (user_id, date, name, calories, protein, fat, carbs) VALUES (?,?,?,?,?,?,?)",
                (user_id, today, item["name"], item["cal"], item["protein"], item["fat"], item["carbs"])
            )
    db.commit()

    return {"ok": True, "message": "Plan applied", "total_cal": plan["total_cal"]}
'''

with open('app/routes/meal_plans.py', 'w', encoding='utf-8') as f:
    f.write(route_code)

# 2. Create template
template_code = '''{% extends "base.html" %}
{% block title %}NutriFlow - Планы питания{% endblock %}
{% block content %}
<section class="page" id="meal-plans-page" style="padding-bottom:100px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
        <h1 style="font-size:24px;margin:0" data-i18n="meal_plans_title">🥗 Планы питания</h1>
        <a href="/dashboard" style="color:var(--accent);text-decoration:none;font-size:14px">← Назад</a>
    </div>
    <p class="muted" style="margin-bottom:20px" data-i18n="meal_plans_desc">Выбери готовый рацион на день и добавь в дневник одним нажатием</p>
    <div id="plans-list"></div>
    <div id="plan-detail" class="hidden"></div>
</section>

<script>
var token = localStorage.getItem("token");
var currentLang = localStorage.getItem("lang") || "ru";

function loadPlans() {
    document.getElementById("plans-list").classList.remove("hidden");
    document.getElementById("plan-detail").classList.add("hidden");

    fetch("/api/meal-plans")
    .then(function(r){return r.json()})
    .then(function(plans){
        var html = "";
        plans.forEach(function(p){
            var name = currentLang==="en" && p.name_en ? p.name_en : p.name;
            var desc = currentLang==="en" && p.description_en ? p.description_en : p.description;
            html += '<div class="card" style="padding:16px;margin-bottom:12px;cursor:pointer;border-radius:16px" onclick="showPlan('+p.id+')">';
            html += '<div style="display:flex;align-items:center;gap:12px">';
            html += '<span style="font-size:36px">'+p.icon+'</span>';
            html += '<div style="flex:1">';
            html += '<h3 style="margin:0;font-size:17px">'+name+'</h3>';
            html += '<p class="muted" style="margin:4px 0 0;font-size:13px">'+desc+'</p>';
            html += '<div style="display:flex;gap:12px;margin-top:8px;font-size:12px">';
            html += '<span style="color:var(--accent)">🔥 '+p.total_cal+' ккал</span>';
            html += '<span style="color:#4ecdc4">🥩 '+p.total_protein+'г</span>';
            html += '<span style="color:#ffe66d">🧈 '+p.total_fat+'г</span>';
            html += '<span style="color:#ff6b6b">🍞 '+p.total_carbs+'г</span>';
            html += '</div></div>';
            html += '<span style="font-size:20px;color:var(--muted)">→</span>';
            html += '</div></div>';
        });
        document.getElementById("plans-list").innerHTML = html;
    });
}

function showPlan(id) {
    document.getElementById("plans-list").classList.add("hidden");
    document.getElementById("plan-detail").classList.remove("hidden");

    fetch("/api/meal-plans/"+id)
    .then(function(r){return r.json()})
    .then(function(p){
        var name = currentLang==="en" && p.name_en ? p.name_en : p.name;
        var html = '';
        html += '<div style="display:flex;align-items:center;gap:8px;margin-bottom:16px">';
        html += '<a href="#" onclick="loadPlans();return false" style="color:var(--accent);text-decoration:none;font-size:20px">←</a>';
        html += '<span style="font-size:28px">'+p.icon+'</span>';
        html += '<h2 style="margin:0;font-size:22px">'+name+'</h2>';
        html += '</div>';

        html += '<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-bottom:20px;text-align:center">';
        html += '<div class="card" style="padding:10px;border-radius:12px"><div style="font-size:18px;font-weight:700;color:var(--accent)">'+p.total_cal+'</div><div class="muted" style="font-size:11px">ккал</div></div>';
        html += '<div class="card" style="padding:10px;border-radius:12px"><div style="font-size:18px;font-weight:700;color:#4ecdc4">'+p.total_protein+'г</div><div class="muted" style="font-size:11px">белки</div></div>';
        html += '<div class="card" style="padding:10px;border-radius:12px"><div style="font-size:18px;font-weight:700;color:#ffe66d">'+p.total_fat+'г</div><div class="muted" style="font-size:11px">жиры</div></div>';
        html += '<div class="card" style="padding:10px;border-radius:12px"><div style="font-size:18px;font-weight:700;color:#ff6b6b">'+p.total_carbs+'г</div><div class="muted" style="font-size:11px">углеводы</div></div>';
        html += '</div>';

        p.meals.forEach(function(meal){
            var mealName = currentLang==="en" && meal.type_name_en ? meal.type_name_en : meal.type_name;
            html += '<div class="card" style="padding:14px;margin-bottom:10px;border-radius:14px">';
            html += '<h3 style="margin:0 0 10px;font-size:15px">'+meal.icon+' '+mealName+'</h3>';
            var mealCal = 0;
            meal.items.forEach(function(item){
                var itemName = currentLang==="en" && item.name_en ? item.name_en : item.name;
                mealCal += item.cal;
                html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">';
                html += '<span style="font-size:14px">'+itemName+'</span>';
                html += '<div style="text-align:right;font-size:12px">';
                html += '<span style="color:var(--accent)">'+item.cal+' ккал</span><br>';
                html += '<span class="muted">Б:'+item.protein+' Ж:'+item.fat+' У:'+item.carbs+'</span>';
                html += '</div></div>';
            });
            html += '<div style="text-align:right;margin-top:8px;font-size:13px;color:var(--accent);font-weight:600">Итого: '+mealCal+' ккал</div>';
            html += '</div>';
        });

        html += '<button onclick="applyPlan('+p.id+')" class="btn btn-primary full-width" style="margin-top:16px;padding:14px;font-size:16px;border-radius:14px">✅ Добавить весь план в дневник</button>';
        html += '<p id="apply-msg" style="text-align:center;margin-top:10px;font-size:14px"></p>';

        document.getElementById("plan-detail").innerHTML = html;
    });
}

function applyPlan(id) {
    fetch("/api/meal-plans/"+id+"/apply", {
        method: "POST",
        headers: {"Authorization": "Bearer "+token}
    })
    .then(function(r){return r.json()})
    .then(function(d){
        if(d.ok){
            var msg = document.getElementById("apply-msg");
            msg.style.color = "#30d158";
            msg.textContent = currentLang==="en" ? "✅ Plan added to your diary!" : "✅ План добавлен в дневник!";
            setTimeout(function(){window.location.href="/dashboard"},1500);
        }
    })
    .catch(function(){
        var msg = document.getElementById("apply-msg");
        msg.style.color = "#ff453a";
        msg.textContent = "Ошибка";
    });
}

loadPlans();
</script>
{% endblock %}
'''

with open('app/templates/meal_plans.html', 'w', encoding='utf-8') as f:
    f.write(template_code)

# 3. Register route in main.py
f = open('app/main.py', 'r', encoding='utf-8')
main = f.read()
f.close()

if 'meal_plans' not in main:
    main = main.replace(
        'from app.routes import',
        'from app.routes import meal_plans,\n    '  # wrong approach, do manual
    ) if 'from app.routes import' in main else main

# Safer approach - just add import and include
if 'meal_plans' not in main:
    # Find last router include
    import_line = 'from app.routes.meal_plans import router as meal_plans_router'
    include_line = 'app.include_router(meal_plans_router)'
    
    if import_line not in main:
        # Add import after last "from app.routes" import
        lines = main.split('\n')
        last_import_idx = 0
        last_include_idx = 0
        for i, line in enumerate(lines):
            if 'from app.routes' in line and 'import' in line:
                last_import_idx = i
            if 'app.include_router' in line:
                last_include_idx = i
        
        lines.insert(last_import_idx + 1, import_line)
        last_include_idx += 1  # shifted by 1
        lines.insert(last_include_idx + 1, include_line)
        main = '\n'.join(lines)
    
    with open('app/main.py', 'w', encoding='utf-8') as f:
        f.write(main)

# 4. Add link on dashboard
f = open('app/templates/dashboard.html', 'r', encoding='utf-8')
dash = f.read()
f.close()

if '/meal-plans' not in dash:
    # Find goals button and add meal plans button after quick actions
    old_btns = '<span data-i18n="goals_motivation">Цели и мотивация</span></a>'
    new_btns = old_btns + '''
    </div>
    <div style="display:grid;grid-template-columns:1fr;gap:10px;margin-top:10px">
    <a href="/meal-plans" class="btn btn-glass full-width" style="text-align:center;text-decoration:none;font-size:15px">🥗 <span data-i18n="meal_plans_btn">Планы питания</span></a>'''
    
    if old_btns in dash:
        dash = dash.replace(old_btns, new_btns)
    
    with open('app/templates/dashboard.html', 'w', encoding='utf-8') as f:
        f.write(dash)

print("Meal plans created!")
print("- app/routes/meal_plans.py")
print("- app/templates/meal_plans.html")
print("- main.py updated")
print("- dashboard link added")