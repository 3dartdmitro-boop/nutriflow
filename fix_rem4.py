path = "app/templates/reminders.html"
f = open(path, "r", encoding="utf-8")
s = f.read()
f.close()

# Replace the IIFE wrapper with DOMContentLoaded
s = s.replace('(function(){', 'document.addEventListener("DOMContentLoaded",function(){')
s = s.replace('})();', '});')

f = open(path, "w", encoding="utf-8")
f.write(s)
f.close()
print("Done — wrapped in DOMContentLoaded")