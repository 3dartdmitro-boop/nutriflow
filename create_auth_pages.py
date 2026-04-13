# --- register.html ---
reg = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<link rel="icon" href="data:,">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>NutriFlow</title>
<link rel="stylesheet" href="/static/css/style.css?v=960">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",sans-serif;background:var(--bg);color:var(--text)}
.auth{min-height:100vh;min-height:100dvh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px 20px;max-width:430px;margin:0 auto}
.auth-logo{width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,#0071e3,#34c759);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;box-shadow:0 8px 30px rgba(0,113,227,0.3)}
.auth h1{font-size:28px;font-weight:800;margin-bottom:6px;text-align:center}
.auth-sub{color:var(--muted);font-size:14px;margin-bottom:28px;text-align:center}
.auth-form{width:100%;display:grid;gap:12px}
.auth-input{width:100%;padding:16px;border-radius:14px;border:1px solid var(--line);background:var(--card);color:var(--text);font-size:16px;outline:none;transition:border .2s}
.auth-input:focus{border-color:var(--accent)}
.auth-input::placeholder{color:var(--muted)}
.auth-btn{width:100%;padding:16px;border-radius:14px;border:none;background:linear-gradient(135deg,#0071e3,#0077ED);color:#fff;font-size:16px;font-weight:700;cursor:pointer;transition:all .2s;margin-top:4px}
.auth-btn:active{transform:scale(0.97)}
.auth-btn:disabled{opacity:0.5}
.auth-link{text-align:center;margin-top:16px;font-size:14px;color:var(--muted)}
.auth-link a{color:var(--accent);text-decoration:none;font-weight:600}
.auth-err{color:#ff3b30;font-size:13px;text-align:center;min-height:18px}
body.dark .auth-input{background:rgba(44,44,46,0.8);border-color:rgba(255,255,255,0.1);color:#f5f5f7}
</style>
</head>
<body>
<div class="auth">
<div class="auth-logo">
<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>
</div>
<h1 id="rTitle"></h1>
<p class="auth-sub" id="rSub"></p>
<div class="auth-form">
<input class="auth-input" type="text" id="rName" autocomplete="name">
<input class="auth-input" type="email" id="rEmail" autocomplete="email">
<input class="auth-input" type="password" id="rPass" autocomplete="new-password">
<p class="auth-err" id="rErr"></p>
<button class="auth-btn" id="rBtn" onclick="doReg()"></button>
</div>
<p class="auth-link" id="rLink"></p>
</div>
<script>
var L=localStorage.getItem("lang")||"ru";
var D=localStorage.getItem("theme")||"light";
if(D==="dark")document.body.classList.add("dark");
var T={
ru:{t:"Создать аккаунт",sub:"Заполните данные для регистрации",name:"Ваше имя",email:"Email",pass:"Пароль",btn:"Зарегистрироваться",link:'Уже есть аккаунт? <a href="/login">Войти</a>',err_fill:"Заполните все поля",err_email:"Этот email уже занят",err_net:"Ошибка сети"},
en:{t:"Create Account",sub:"Fill in your details to sign up",name:"Your name",email:"Email",pass:"Password",btn:"Sign Up",link:'Already have an account? <a href="/login">Sign in</a>',err_fill:"Fill in all fields",err_email:"This email is already taken",err_net:"Network error"}
};
function aL(){var t=T[L];
document.getElementById("rTitle").textContent=t.t;
document.getElementById("rSub").textContent=t.sub;
document.getElementById("rName").placeholder=t.name;
document.getElementById("rEmail").placeholder=t.email;
document.getElementById("rPass").placeholder=t.pass;
document.getElementById("rBtn").textContent=t.btn;
document.getElementById("rLink").innerHTML=t.link}
aL();
async function doReg(){
var t=T[L],n=document.getElementById("rName").value.trim(),e=document.getElementById("rEmail").value.trim(),p=document.getElementById("rPass").value;
document.getElementById("rErr").textContent="";
if(!n||!e||!p){document.getElementById("rErr").textContent=t.err_fill;return}
document.getElementById("rBtn").disabled=true;
try{var r=await fetch("/api/auth/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:n,email:e,password:p})});
var d=await r.json();
if(!r.ok){document.getElementById("rErr").textContent=t.err_email;document.getElementById("rBtn").disabled=false;return}
localStorage.setItem("token",d.token);localStorage.setItem("user",JSON.stringify(d.user));
window.location.href="/onboarding";
}catch(x){document.getElementById("rErr").textContent=t.err_net;document.getElementById("rBtn").disabled=false}}
</script>
</body>
</html>'''

# --- login.html ---
log = '''<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<link rel="icon" href="data:,">
<meta name="viewport" content="width=device-width,initial-scale=1.0,maximum-scale=1.0,user-scalable=no">
<title>NutriFlow</title>
<link rel="stylesheet" href="/static/css/style.css?v=960">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","Segoe UI",sans-serif;background:var(--bg);color:var(--text)}
.auth{min-height:100vh;min-height:100dvh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:24px 20px;max-width:430px;margin:0 auto}
.auth-logo{width:72px;height:72px;border-radius:20px;background:linear-gradient(135deg,#0071e3,#34c759);display:flex;align-items:center;justify-content:center;margin:0 auto 20px;box-shadow:0 8px 30px rgba(0,113,227,0.3)}
.auth h1{font-size:28px;font-weight:800;margin-bottom:6px;text-align:center}
.auth-sub{color:var(--muted);font-size:14px;margin-bottom:28px;text-align:center}
.auth-form{width:100%;display:grid;gap:12px}
.auth-input{width:100%;padding:16px;border-radius:14px;border:1px solid var(--line);background:var(--card);color:var(--text);font-size:16px;outline:none;transition:border .2s}
.auth-input:focus{border-color:var(--accent)}
.auth-input::placeholder{color:var(--muted)}
.auth-btn{width:100%;padding:16px;border-radius:14px;border:none;background:linear-gradient(135deg,#0071e3,#0077ED);color:#fff;font-size:16px;font-weight:700;cursor:pointer;transition:all .2s;margin-top:4px}
.auth-btn:active{transform:scale(0.97)}
.auth-btn:disabled{opacity:0.5}
.auth-link{text-align:center;margin-top:16px;font-size:14px;color:var(--muted)}
.auth-link a{color:var(--accent);text-decoration:none;font-weight:600}
.auth-err{color:#ff3b30;font-size:13px;text-align:center;min-height:18px}
body.dark .auth-input{background:rgba(44,44,46,0.8);border-color:rgba(255,255,255,0.1);color:#f5f5f7}
</style>
</head>
<body>
<div class="auth">
<div class="auth-logo">
<svg width="38" height="38" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 8h1a4 4 0 010 8h-1"/><path d="M2 8h16v9a4 4 0 01-4 4H6a4 4 0 01-4-4V8z"/><line x1="6" y1="1" x2="6" y2="4"/><line x1="10" y1="1" x2="10" y2="4"/><line x1="14" y1="1" x2="14" y2="4"/></svg>
</div>
<h1 id="lTitle"></h1>
<p class="auth-sub" id="lSub"></p>
<div class="auth-form">
<input class="auth-input" type="email" id="lEmail" autocomplete="email">
<input class="auth-input" type="password" id="lPass" autocomplete="current-password">
<p class="auth-err" id="lErr"></p>
<button class="auth-btn" id="lBtn" onclick="doLog()"></button>
</div>
<p class="auth-link" id="lLink"></p>
</div>
<script>
var L=localStorage.getItem("lang")||"ru";
var D=localStorage.getItem("theme")||"light";
if(D==="dark")document.body.classList.add("dark");
var T={
ru:{t:"Вход",sub:"Введите данные вашего аккаунта",email:"Email",pass:"Пароль",btn:"Войти",link:'Нет аккаунта? <a href="/register">Создать</a>',err_fill:"Заполните все поля",err_cred:"Неверный email или пароль",err_net:"Ошибка сети"},
en:{t:"Sign In",sub:"Enter your account details",email:"Email",pass:"Password",btn:"Sign In",link:'No account? <a href="/register">Create one</a>',err_fill:"Fill in all fields",err_cred:"Invalid email or password",err_net:"Network error"}
};
function aL(){var t=T[L];
document.getElementById("lTitle").textContent=t.t;
document.getElementById("lSub").textContent=t.sub;
document.getElementById("lEmail").placeholder=t.email;
document.getElementById("lPass").placeholder=t.pass;
document.getElementById("lBtn").textContent=t.btn;
document.getElementById("lLink").innerHTML=t.link}
aL();
async function doLog(){
var t=T[L],e=document.getElementById("lEmail").value.trim(),p=document.getElementById("lPass").value;
document.getElementById("lErr").textContent="";
if(!e||!p){document.getElementById("lErr").textContent=t.err_fill;return}
document.getElementById("lBtn").disabled=true;
try{var r=await fetch("/api/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:e,password:p})});
var d=await r.json();
if(!r.ok){document.getElementById("lErr").textContent=t.err_cred;document.getElementById("lBtn").disabled=false;return}
localStorage.setItem("token",d.token);localStorage.setItem("user",JSON.stringify(d.user));
window.location.href="/dashboard";
}catch(x){document.getElementById("lErr").textContent=t.err_net;document.getElementById("lBtn").disabled=false}}
</script>
</body>
</html>'''

with open('app/templates/register.html','w',encoding='utf-8') as f:
    f.write(reg)
with open('app/templates/login.html','w',encoding='utf-8') as f:
    f.write(log)

# Add routes to pages.py
f = open('app/routes/pages.py','r',encoding='utf-8')
s = f.read()
f.close()
added = False
if '/register' not in s:
    s += '\n\n@router.get("/register")\ndef register_page(request: Request):\n    return templates.TemplateResponse("register.html", {"request": request})\n'
    added = True
if '/login' not in s:
    s += '\n\n@router.get("/login")\ndef login_page(request: Request):\n    return templates.TemplateResponse("login.html", {"request": request})\n'
    added = True
if added:
    f = open('app/routes/pages.py','w',encoding='utf-8')
    f.write(s)
    f.close()

# Fix welcome.html links
f = open('app/templates/welcome.html','r',encoding='utf-8')
w = f.read()
f.close()
w = w.replace('/onboarding','/register').replace("href=\"/profile\"","href=\"/login\"")
f = open('app/templates/welcome.html','w',encoding='utf-8')
f.write(w)
f.close()

print("DONE: register.html, login.html created, routes added, welcome links fixed")