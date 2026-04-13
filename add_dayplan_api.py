f = open('app/routes/api.py', 'r', encoding='utf-8')
s = f.read()
f.close()

new_endpoints = '''

@router.get("/api/day-plan/today")
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
        "SELECT id, meal_type, product_name, grams, calories, protein, fat, carbs, eaten FROM day_plan WHERE user_id=? AND plan_date=? ORDER BY id",
        (user_id, today)
    ).fetchall()
    result = []
    for r in rows:
        result.append({
            "id": r[0], "meal_type": r[1], "name": r[2], "grams": r[3],
            "cal": r[4], "protein": r[5], "fat": r[6], "carbs": r[7], "eaten": r[8]
        })
    return result


@router.post("/api/day-plan/toggle/{item_id}")
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
            "DELETE FROM food_log WHERE user_id=? AND log_date=? AND product_name=? AND meal_type=? LIMIT 1",
            (user_id, today, row[2], row[1])
        )
    db.commit()
    return {"ok": True, "eaten": new_eaten}
'''

if '/api/day-plan/today' not in s:
    s = s.rstrip() + '\n' + new_endpoints
    f = open('app/routes/api.py', 'w', encoding='utf-8')
    f.write(s)
    f.close()
    print("Added day-plan API endpoints")
else:
    print("Already exists")