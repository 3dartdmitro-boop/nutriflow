f = 'app/templates/reminders.html'
lines = open(f, 'r', encoding='utf-8').readlines()
found = False
out = []
for line in lines:
    if 'c.id!=="weight"' in line and 'c.dk' in line:
        if not found:
            found = True
            out.append(line)
        # skip duplicate
    else:
        out.append(line)
open(f, 'w', encoding='utf-8').writelines(out)
print('OK')
