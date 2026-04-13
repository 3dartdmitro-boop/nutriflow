path = "app/templates/reminders.html"
f = open(path, "r", encoding="utf-8")
s = f.read()
f.close()

# Replace static description with dynamic one
# Find where description is rendered and make it show chosen times for "times" type
old = "T(c.dk)"
new = "(c.type==='times'&&s.enabled?(s.times||c.dt).join(', '):T(c.dk))"

s = s.replace(old, new)

f = open(path, "w", encoding="utf-8")
f.write(s)
f.close()
print("Done — description now shows selected times when active")