import os

path = "app/templates/food.html"
f = open(path, "r", encoding="utf-8")
s = f.read()
f.close()

# Fix 1: "Граммы" label with colon on new line - broken HTML
# Current: <label data-i18n="grams">Граммы</label>:
# Need: <label data-i18n="grams_label">Граммы:</label>
s = s.replace(
    '<label style="font-size:14px" data-i18n="grams">\u0413\u0440\u0430\u043c\u043c\u044b</label>:',
    '<label style="font-size:14px" data-i18n="grams_label">\u0413\u0440\u0430\u043c\u043c\u044b:</label>'
)
print("1. Fixed grams label")

f = open(path, "w", encoding="utf-8")
f.write(s)
f.close()
print("OK - food.html saved")

# Fix 2: Add grams_label to i18n
path2 = "app/static/js/i18n.js"
f = open(path2, "r", encoding="utf-8")
s2 = f.read()
f.close()

if "grams_label" not in s2:
    s2 = s2.replace('grams:"\u0413\u0440\u0430\u043c\u043c\u044b"', 'grams:"\u0413\u0440\u0430\u043c\u043c\u044b",grams_label:"\u0413\u0440\u0430\u043c\u043c\u044b:"')
    s2 = s2.replace('grams:"Grams"', 'grams:"Grams",grams_label:"Grams:"')
    print("2. Added grams_label to i18n")

f = open(path2, "w", encoding="utf-8")
f.write(s2)
f.close()
print("OK - i18n.js saved")

# Fix 3: Check food.js for hardcoded б/ж/у in log
path3 = "app/static/js/food.js"
f = open(path3, "r", encoding="utf-8")
s3 = f.read()
f.close()

# Find the log rendering with б/ж/у
idx = s3.find("\u0431 /")
if idx < 0:
    idx = s3.find("\u0431/")
if idx > 0:
    start = s3.rfind("\n", 0, idx)
    end = s3.find("\n", idx)
    print("3. Found in food.js:", repr(s3[start+1:end]))
else:
    # Try to find protein display
    idx = s3.find("protein")
    if idx > 0:
        for i in range(5):
            ni = s3.find("protein", idx+1)
            if ni > 0: idx = ni
        start = s3.rfind("\n", 0, idx)
        end = s3.find("\n", idx)
        print("3. Protein context:", repr(s3[start+1:end][:150]))

os.remove("fix_food2.py")
print("Self-deleted")