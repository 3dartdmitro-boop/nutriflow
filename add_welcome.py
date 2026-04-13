f = open('app/routes/pages.py', 'r', encoding='utf-8')
s = f.read()
f.close()

if '/welcome' not in s:
    s += """

@router.get("/welcome")
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})
"""
    f = open('app/routes/pages.py', 'w', encoding='utf-8')
    f.write(s)
    f.close()
    print("welcome route added")
else:
    print("already exists")