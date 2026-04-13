# 1. Add API endpoint to get today's food list
f = open('app/routes/api.py', 'r', encoding='utf-8')
s = f.read()
f.close()

if '/api/food-log/today' not in s:
    new_endpoint = '''

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
'''
    # Add before last line or at end
    s = s.rstrip() + '\n' + new_endpoint
    
    f = open('app/routes/api.py', 'w', encoding='utf-8')
    f.write(s)
    f.close()
    print("Added /api/food-log/today endpoint")

# 2. Add food list section to dashboard
f = open('app/templates/dashboard.html', 'r', encoding='utf-8')
d = f.read()
f.close()

if 'today-food-list' not in d:
    # Add section before "Быстрые действия"
    old = '<div class="card" style="padding:16px;margin-top:20px">\n        <h3'
    
    # Find the quick actions section
    idx = d.find('Быстрые действия')
    if idx == -1:
        idx = d.find('quick_actions')
    
    # Find the card div before it
    if idx > 0:
        # Go back to find the <div class="card" before "Быстрые действия"
        card_start = d.rfind('<div class="card"', 0, idx)
        
        food_list_section = '''<div class="card" style="padding:16px;margin-top:20px;border-radius:16px">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px">
            <h3 style="margin:0;font-size:17px" data-i18n="today_food_title">🍽 Сегодня съедено</h3>
            <span id="food-count" class="muted" style="font-size:13px"></span>
        </div>
        <div id="today-food-list" style="max-height:400px;overflow-y:auto">
            <p class="muted" style="text-align:center;font-size:14px" data-i18n="loading">Загрузка...</p>
        </div>
    </div>
    
    '''
        d = d[:card_start] + food_list_section + d[card_start:]
    
    # Now add the JS to load food list
    # Find the closing </script> and add before it
    script_end = d.rfind('</script>')
    
    food_list_js = '''
// Load today's food list
function loadTodayFood() {
    fetch("/api/food-log/today", {headers:{"Authorization":"Bearer "+token}})
    .then(function(r){return r.json()})
    .then(function(items){
        var container = document.getElementById("today-food-list");
        var countEl = document.getElementById("food-count");
        if(!container) return;
        
        if(!items.length || items.error) {
            var lang = localStorage.getItem("lang") || "ru";
            container.innerHTML = '<p class="muted" style="text-align:center;font-size:14px;padding:20px 0">' + 
                (lang==="en" ? "No food logged yet" : "Пока ничего не записано") + '</p>';
            if(countEl) countEl.textContent = "";
            return;
        }
        
        if(countEl) countEl.textContent = items.length + " шт";
        
        // Group by meal_type
        var groups = {};
        var mealOrder = ["breakfast","lunch","snack","dinner"];
        var mealIcons = {"breakfast":"🌅","lunch":"☀️","snack":"🍎","dinner":"🌙"};
        var mealNames = {"breakfast":"Завтрак","lunch":"Обед","snack":"Перекус","dinner":"Ужин"};
        var mealNamesEn = {"breakfast":"Breakfast","lunch":"Lunch","snack":"Snack","dinner":"Dinner"};
        
        items.forEach(function(item){
            var mt = item.meal_type || "other";
            if(!groups[mt]) groups[mt] = [];
            groups[mt].push(item);
        });
        
        var lang = localStorage.getItem("lang") || "ru";
        var html = "";
        
        mealOrder.forEach(function(mt){
            if(!groups[mt]) return;
            var icon = mealIcons[mt] || "🍽";
            var mname = lang==="en" ? (mealNamesEn[mt]||mt) : (mealNames[mt]||mt);
            var mealCal = 0;
            
            html += '<div style="margin-bottom:14px">';
            html += '<div style="font-size:14px;font-weight:600;margin-bottom:6px;color:var(--accent)">' + icon + ' ' + mname + '</div>';
            
            groups[mt].forEach(function(item){
                mealCal += (item.cal || 0);
                html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">';
                html += '<div style="flex:1"><span style="font-size:13px">' + item.name + '</span>';
                if(item.grams && item.grams != 100) html += ' <span class="muted" style="font-size:11px">' + item.grams + 'г</span>';
                html += '</div>';
                html += '<div style="text-align:right;font-size:12px">';
                html += '<span style="color:var(--accent)">' + Math.round(item.cal||0) + '</span>';
                html += ' <span class="muted">ккал</span>';
                html += '</div></div>';
            });
            
            html += '<div style="text-align:right;font-size:12px;color:var(--accent);margin-top:4px;font-weight:600">' + Math.round(mealCal) + ' ккал</div>';
            html += '</div>';
        });
        
        // Check for "other" types not in mealOrder
        Object.keys(groups).forEach(function(mt){
            if(mealOrder.indexOf(mt) === -1){
                var mealCal = 0;
                html += '<div style="margin-bottom:14px">';
                html += '<div style="font-size:14px;font-weight:600;margin-bottom:6px;color:var(--accent)">🍽 ' + mt + '</div>';
                groups[mt].forEach(function(item){
                    mealCal += (item.cal || 0);
                    html += '<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 0;border-bottom:1px solid rgba(255,255,255,0.05)">';
                    html += '<span style="font-size:13px">' + item.name + '</span>';
                    html += '<span style="font-size:12px;color:var(--accent)">' + Math.round(item.cal||0) + ' ккал</span>';
                    html += '</div>';
                });
                html += '<div style="text-align:right;font-size:12px;color:var(--accent);margin-top:4px;font-weight:600">' + Math.round(mealCal) + ' ккал</div>';
                html += '</div>';
            }
        });
        
        container.innerHTML = html;
    })
    .catch(function(e){
        console.error("Food list error:", e);
    });
}

// Call after dashboard loads
setTimeout(loadTodayFood, 500);

'''
    
    d = d[:script_end] + food_list_js + d[script_end:]
    
    f = open('app/templates/dashboard.html', 'w', encoding='utf-8')
    f.write(d)
    f.close()
    print("Added food list to dashboard")

# 3. Add i18n
f = open('app/static/js/i18n.js', 'r', encoding='utf-8')
i = f.read()
f.close()

if 'today_food_title' not in i:
    i = i.replace(
        '"meal_plans_btn":"Планы питания"',
        '"meal_plans_btn":"Планы питания","today_food_title":"🍽 Сегодня съедено"'
    )
    i = i.replace(
        '"meal_plans_btn":"Meal Plans"',
        '"meal_plans_btn":"Meal Plans","today_food_title":"🍽 Eaten Today"'
    )
    f = open('app/static/js/i18n.js', 'w', encoding='utf-8')
    f.write(i)
    f.close()
    print("Added i18n keys")

print("Done! Dashboard now shows today's food list")