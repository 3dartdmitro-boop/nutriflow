# 1. Remove floating bell from app.js
path = "app/static/js/app.js"
f = open(path, "r", encoding="utf-8")
s = f.read()
f.close()

# Remove the bell code block
if "Reminder bell" in s:
    start = s.find("// Reminder bell")
    end = s.find("})();", start)
    if end > start:
        s = s[:start] + s[end+5:]
        f = open(path, "w", encoding="utf-8")
        f.write(s)
        f.close()
        print("1. Removed floating bell from app.js")
else:
    print("1. No floating bell in app.js")

# 2. Add bell button to base.html header next to theme and lang buttons
path2 = "app/templates/base.html"
f = open(path2, "r", encoding="utf-8")
s2 = f.read()
f.close()

if "reminders" not in s2:
    old = '<button class="lang-toggle-small" onclick="toggleLang()" id="lang-btn">EN</button>'
    new = '<button class="lang-toggle-small" onclick="toggleLang()" id="lang-btn">EN</button>\n    <a href="/reminders" style="width:36px;height:36px;border-radius:50%;background:rgba(255,255,255,.08);display:flex;align-items:center;justify-content:center;font-size:18px;text-decoration:none;border:none;cursor:pointer;" title="Reminders">🔔</a>'
    s2 = s2.replace(old, new)
    print("2. Bell added to header")
else:
    print("2. Bell already in header")

# 3. Bump cache version
s2 = s2.replace("v=700", "v=701")
print("3. Cache bumped to v=701")

f = open(path2, "w", encoding="utf-8")
f.write(s2)
f.close()

print("\nDone!")