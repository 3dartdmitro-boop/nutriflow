f = open('app/templates/profile.html', 'r', encoding='utf-8')
s = f.read()
f.close()

# Add "Edit body data" button after logout button
old = '<button id="logout-btn" class="btn btn-glass full-width" style="margin-top:12px;color:#ff453a" data-i18n="logout">Выйти</button>'

new = '''<button id="logout-btn" class="btn btn-glass full-width" style="margin-top:12px;color:#ff453a" data-i18n="logout">Выйти</button>
        <a href="/onboarding" class="btn btn-glass full-width" style="margin-top:12px;text-align:center;text-decoration:none;display:block" data-i18n="edit_body_data">⚙️ Изменить данные тела</a>'''

s = s.replace(old, new)

f = open('app/templates/profile.html', 'w', encoding='utf-8')
f.write(s)
f.close()
print("added edit body data button to profile")