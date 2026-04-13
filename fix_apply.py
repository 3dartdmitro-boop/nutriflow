path = "app/routes/meal_plans.py"
f = open(path, "r", encoding="utf-8")
s = f.read()
f.close()

# Find and replace the apply function
old_apply_start = "@router.post(\"/api/meal-plans/{plan_id}/apply\")"
idx = s.find(old_apply_start)
if idx == -1:
    print("apply endpoint not found")
    exit()

# Find end of function (next @router or end of file)
next_route = s.find("\n@router.", idx + 10)
if next_route == -1:
    old_apply = s[idx:]
else:
    old_apply = s[idx:next_route]

new_apply = '''@router.post("/api/meal-plans/{plan_id}/apply")
async def apply_meal_plan(plan_id: int, request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    # Map plan_id to plan_type
    plan_map = {1: "balanced", 2: "high_protein", 3: "weight_loss", 4: "vegetarian"}
    plan_type = plan_map.get(plan_id)
    if not plan_type:
        return JSONResponse(status_code=404, content={"error": "Plan not found"})

    plan_info = None
    for p in MEAL_PLANS:
        if p["id"] == plan_id:
            plan_info = p
            break

    from datetime import date
    from app.services.nutrition import generate_meal_plan

    today_date = date.today()
    today = today_date.isoformat()
    # Seed = user_id + plan_id + day_of_year -> same plan for same day, different each day
    seed = user_id * 10000 + plan_id * 1000 + today_date.timetuple().tm_yday
    meals = generate_meal_plan(plan_type, seed=seed)

    db = get_db()
    try:
        db.execute("DELETE FROM day_plan WHERE user_id=? AND plan_date=?", (user_id, today))
        for meal in meals:
            for item in meal["items"]:
                db.execute(
                    "INSERT INTO day_plan (user_id, plan_date, meal_type, product_name, product_name_en, grams, calories, protein, fat, carbs, eaten) VALUES (?,?,?,?,?,?,?,?,?,?,0)",
                    (user_id, today, meal["type"], item["name"], item.get("name_en",""), item.get("grams",100), item["cal"], item["protein"], item["fat"], item["carbs"])
                )
        db.commit()
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

    total_cal = sum(item["cal"] for meal in meals for item in meal["items"])
    return {"ok": True, "message": "Plan generated", "total_cal": total_cal}
'''

s = s.replace(old_apply, new_apply)
f = open(path, "w", encoding="utf-8")
f.write(s)
f.close()
print("OK - apply now generates from product base")

import os
os.remove("fix_apply.py")