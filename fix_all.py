# === 1. i18n translations ===
path = "app/static/js/i18n.js"
f = open(path, "r", encoding="utf-8")
s = f.read()
f.close()

# Achievement translations
if "a_first_food" not in s:
    ach_ru = 'a_first_food:"Первая еда",ad_first_food:"Добавь первый приём пищи",a_food_7:"Неделя питания",ad_food_7:"Записывай еду 7 дней",a_food_30:"Месяц питания",ad_food_30:"Записывай еду 30 дней",a_first_water:"Первый стакан",ad_first_water:"Добавь воду впервые",a_water_7:"Неделя воды",ad_water_7:"Пей воду 7 дней подряд",a_water_30:"Месяц воды",ad_water_30:"Пей воду 30 дней подряд",a_first_weight:"Первое взвешивание",ad_first_weight:"Запиши вес впервые",a_weight_10:"10 взвешиваний",ad_weight_10:"Запиши вес 10 раз",a_water_10l:"10 литров воды",ad_water_10l:"Выпей 10 литров воды суммарно",a_water_50l:"50 литров воды",ad_water_50l:"Выпей 50 литров воды суммарно",a_streak_3:"3 дня подряд",ad_streak_3:"Серия активности 3 дня",a_streak_7:"Неделя подряд",ad_streak_7:"Серия активности 7 дней",'
    ach_en = 'a_first_food:"First meal",ad_first_food:"Log your first meal",a_food_7:"Week of food",ad_food_7:"Log food for 7 days",a_food_30:"Month of food",ad_food_30:"Log food for 30 days",a_first_water:"First glass",ad_first_water:"Log water for the first time",a_water_7:"Week of water",ad_water_7:"Drink water for 7 days in a row",a_water_30:"Month of water",ad_water_30:"Drink water for 30 days in a row",a_first_weight:"First weigh-in",ad_first_weight:"Log your weight for the first time",a_weight_10:"10 weigh-ins",ad_weight_10:"Log your weight 10 times",a_water_10l:"10 liters of water",ad_water_10l:"Drink 10 liters of water total",a_water_50l:"50 liters of water",ad_water_50l:"Drink 50 liters of water total",a_streak_3:"3 days streak",ad_streak_3:"Activity streak of 3 days",a_streak_7:"Week streak",ad_streak_7:"Activity streak of 7 days",'
    s = s.replace('d30:"30д"},', 'd30:"30д",' + ach_ru + '},')
    s = s.replace('d30:"30d"},', 'd30:"30d",' + ach_en + '},')
    print("1a. Achievement translations added")
else:
    print("1a. Achievement translations exist")

# Reminder translations
if "rem_title" not in s:
    rem_ru = 'rem_title:"🔔 Напоминания",rem_perm_text:"Разреши уведомления чтобы получать напоминания",rem_perm_blocked:"Уведомления заблокированы в настройках браузера",rem_perm_btn:"Разрешить",rem_active:"⏰ Активные напоминания",rem_no_active:"Нет активных напоминаний",rem_every:"каждые",rem_min:"мин",rem_water_title:"Пить воду",rem_water_desc:"Каждые 1-3 часа",rem_food_title:"Приём пищи",rem_food_desc:"Завтрак, обед, ужин",rem_weight_title:"Взвеситься",rem_weight_desc:"Раз в день утром",rem_steps_title:"Подвигаться",rem_steps_desc:"Каждые 1-2 часа",'
    rem_en = 'rem_title:"🔔 Reminders",rem_perm_text:"Allow notifications to receive reminders",rem_perm_blocked:"Notifications blocked in browser settings",rem_perm_btn:"Allow",rem_active:"⏰ Active reminders",rem_no_active:"No active reminders",rem_every:"every",rem_min:"min",rem_water_title:"Drink water",rem_water_desc:"Every 1-3 hours",rem_food_title:"Meal time",rem_food_desc:"Breakfast, lunch, dinner",rem_weight_title:"Weigh yourself",rem_weight_desc:"Once a day in the morning",rem_steps_title:"Move around",rem_steps_desc:"Every 1-2 hours",'
    # Insert before closing } of ru
    s = s.replace(ach_ru + '},', ach_ru + rem_ru + '},')
    s = s.replace(ach_en + '},', ach_en + rem_en + '},')
    print("1b. Reminder translations added")
else:
    print("1b. Reminder translations exist")

f = open(path, "w", encoding="utf-8")
f.write(s)
f.close()

# === 2. Route ===
path2 = "app/routes/pages.py"
f = open(path2, "r", encoding="utf-8")
s2 = f.read()
f.close()

if "reminders" not in s2:
    s2 += '\n\n@router.get("/reminders", response_class=HTMLResponse)\nasync def reminders_page(request: Request):\n    return templates.TemplateResponse("reminders.html", {"request": request})\n'
    f = open(path2, "w", encoding="utf-8")
    f.write(s2)
    f.close()
    print("2. Route added")
else:
    print("2. Route exists")

# === 3. Bell button ===
path3 = "app/static/js/app.js"
f = open(path3, "r", encoding="utf-8")
s3 = f.read()
f.close()

if "reminders" not in s3:
    bell = '''
// Reminder bell
(function(){
    var b=document.createElement("a");
    b.href="/reminders";
    b.style.cssText="position:fixed;top:16px;right:16px;width:44px;height:44px;border-radius:50%;background:#1c1c2e;display:flex;align-items:center;justify-content:center;font-size:22px;text-decoration:none;z-index:1000;box-shadow:0 2px 8px rgba(0,0,0,.3);";
    b.textContent="\\ud83d\\udd14";
    document.body.appendChild(b);
})();
'''
    s3 += bell
    f = open(path3, "w", encoding="utf-8")
    f.write(s3)
    f.close()
    print("3. Bell button added")
else:
    print("3. Bell exists")

print("\nDone! Restart uvicorn.")