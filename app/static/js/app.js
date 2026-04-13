document.addEventListener("DOMContentLoaded",function(){
applyLang();
var path=location.pathname;
var token=localStorage.getItem("token");
var publicPages=["/profile","/onboarding"];
if(!token && publicPages.indexOf(path)===-1){location.href="/profile";return;}
if(token && path!=="/profile" && path!=="/onboarding" && !localStorage.getItem("user_cal")){location.href="/onboarding";return;}
if(path==="/onboarding")initOnboarding();
if(path==="/dashboard")initDashboard();
if(path==="/food")initFood();
if(path==="/water")initWater();
if(path==="/weight")initWeight();
if(path==="/profile")initProfile();
if(path==="/goals")initGoals();
});
function getToken(){return localStorage.getItem("token")}
function setToken(t){localStorage.setItem("token",t)}
function clearToken(){localStorage.removeItem("token")}
function isRu(){return L()==="ru"}
function KCAL(){return isRu()?"\u043a\u043a\u0430\u043b":"kcal"}
function GR(){return isRu()?"\u0433":"g"}
function ML(){return isRu()?"\u043c\u043b":"ml"}
function PL(){return isRu()?"\u0431":"p"}
function FL(){return isRu()?"\u0436":"f"}
function CL(){return isRu()?"\u0443":"c"}
function macroStr(p,f,c){return Math.round(p)+" "+PL()+" / "+Math.round(f)+" "+FL()+" / "+Math.round(c)+" "+CL()}

function initOnboarding(){
var form=document.getElementById("nutrition-form");
var result=document.getElementById("result");
if(!form)return;
form.addEventListener("submit",function(e){
e.preventDefault();
var fd=new FormData(form);
var body={weight:parseFloat(fd.get("weight")),height:parseFloat(fd.get("height")),age:parseInt(fd.get("age")),gender:fd.get("gender"),goal:fd.get("goal")};
fetch("/api/calculate",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}).then(function(r){return r.json()}).then(function(d){
localStorage.setItem("user_cal",d.calories);
localStorage.setItem("user_prot",d.protein);
localStorage.setItem("user_fat",d.fat);
localStorage.setItem("user_carbs",d.carbs);
result.classList.remove("hidden");
result.innerHTML='<div class="card" style="text-align:center"><h3>'+d.calories+" "+KCAL()+'</h3><p>'+macroStr(d.protein,d.fat,d.carbs)+'</p><p class="muted">'+(isRu()?"\u041f\u0435\u0440\u0435\u043d\u0430\u043f\u0440\u0430\u0432\u043b\u044f\u0435\u043c...":"Redirecting...")+'</p></div>';
setTimeout(function(){location.href="/dashboard";},1500);
});
});
}

window.loadDashboard = initDashboard;
function initDashboard(){
var cal=parseInt(localStorage.getItem("user_cal"))||2000;
var prot=parseInt(localStorage.getItem("user_prot"))||150;
var fat=parseInt(localStorage.getItem("user_fat"))||55;
var carbs=parseInt(localStorage.getItem("user_carbs"))||250;
var tgt=document.getElementById("cal-target");if(tgt)tgt.textContent=cal;
var pt=document.getElementById("prot-target");if(pt)pt.textContent="/"+prot+GR();
var ft=document.getElementById("fat-target");if(ft)ft.textContent="/"+fat+GR();
var ct=document.getElementById("carb-target");if(ct)ct.textContent="/"+carbs+GR();
fetch("/api/food/today").then(function(r){return r.json()}).then(function(data){
var eaten=0,pe=0,fe=0,ce=0;
data.forEach(function(i){eaten+=i.calories;pe+=i.protein;fe+=i.fat;ce+=i.carbs});
var el=document.getElementById("cal-eaten");if(el)el.textContent=Math.round(eaten);
var ring=document.getElementById("cal-ring");
if(ring){var pct=cal>0?eaten/cal:0;var r=78;var circ=2*Math.PI*r;ring.style.strokeDasharray=circ;ring.style.strokeDashoffset=circ*(1-Math.min(pct,1));}
var pe2=document.getElementById("prot-eaten");if(pe2)pe2.textContent=Math.round(pe);
var fe2=document.getElementById("fat-eaten");if(fe2)fe2.textContent=Math.round(fe);
var ce2=document.getElementById("carb-eaten");if(ce2)ce2.textContent=Math.round(ce);
var pb=document.getElementById("prot-bar");if(pb)pb.style.width=Math.min(pe/prot*100,100)+"%";
var fb=document.getElementById("fat-bar");if(fb)fb.style.width=Math.min(fe/fat*100,100)+"%";
var cb=document.getElementById("carb-bar");if(cb)cb.style.width=Math.min(ce/carbs*100,100)+"%";
});
fetch("/api/water/today").then(function(r){return r.json()}).then(function(data){
var total=0;data.forEach(function(x){total+=x.amount_ml});
var wc=document.getElementById("water-current");if(wc)wc.textContent=total;
var wb=document.getElementById("water-bar");if(wb)wb.style.width=Math.min(total/2500*100,100)+"%";
});
var resetBtn=document.getElementById("reset-day-btn");
if(resetBtn)resetBtn.addEventListener("click",function(){if(confirm(isRu()?"\u0421\u0431\u0440\u043e\u0441\u0438\u0442\u044c?":"Reset?")){fetch("/api/reset/today",{method:"DELETE"}).then(function(){location.reload()});}});
}

function initFood(){
var cal=parseInt(localStorage.getItem("user_cal"))||2000;
var currentMeal="breakfast";
var searchInput=document.getElementById("product-search");
var productList=document.getElementById("product-list");
var foodLog=document.getElementById("food-log");
var mealTitle=document.getElementById("meal-log-title");
var calTarget=document.getElementById("food-cal-target");
if(calTarget)calTarget.textContent=cal;
var modal=document.getElementById("gram-modal");
var gramInput=document.getElementById("gram-input");
var gramPreview=document.getElementById("gram-preview");
var selectedProduct=null;

function loadTotals(){
fetch("/api/food/today").then(function(r){return r.json()}).then(function(data){
var eaten=0,pe=0,fe=0,ce=0;
data.forEach(function(i){eaten+=i.calories;pe+=i.protein;fe+=i.fat;ce+=i.carbs});
var eatEl=document.getElementById("food-cal-eaten");if(eatEl)eatEl.textContent=Math.round(eaten);
var ring=document.getElementById("food-cal-ring");
if(ring){var pct=cal>0?eaten/cal:0;var r=60;var circ=2*Math.PI*r;ring.style.strokeDasharray=circ;ring.style.strokeDashoffset=circ*(1-Math.min(pct,1));}
var fp=document.getElementById("food-prot");if(fp)fp.textContent=Math.round(pe);
var ff=document.getElementById("food-fat");if(ff)ff.textContent=Math.round(fe);
var fc=document.getElementById("food-carb");if(fc)fc.textContent=Math.round(ce);
});}

function loadMealLog(){
fetch("/api/food/today?meal="+currentMeal).then(function(r){return r.json()}).then(function(data){
foodLog.innerHTML="";
if(data.length===0){foodLog.innerHTML='<p class="muted" style="text-align:center;padding:12px">---</p>';return;}
data.forEach(function(item){
var div=document.createElement("div");
div.style.cssText="display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid rgba(128,128,128,0.15)";
div.innerHTML='<div style="flex:1"><strong>'+item.product_name+'</strong><br><span class="muted" style="font-size:11px">'+macroStr(item.protein,item.fat,item.carbs)+'</span></div><div style="text-align:right;display:flex;align-items:center;gap:8px"><span><strong>'+Math.round(item.calories)+"</strong> "+KCAL()+'</span><span class="food-del" data-id="'+item.id+'" style="cursor:pointer;color:#ff453a;font-size:20px">\u00d7</span></div>';
foodLog.appendChild(div);
});
foodLog.querySelectorAll(".food-del").forEach(function(btn){
btn.addEventListener("click",function(){fetch("/api/food/"+this.getAttribute("data-id"),{method:"DELETE"}).then(function(){loadTotals();loadMealLog();});});
});
});}

document.querySelectorAll(".meal-btn").forEach(function(btn){
btn.addEventListener("click",function(){
document.querySelectorAll(".meal-btn").forEach(function(b){b.classList.remove("active")});
btn.classList.add("active");
currentMeal=btn.getAttribute("data-meal");
if(mealTitle)mealTitle.textContent=btn.textContent;
loadMealLog();
});
});

var st=null;
if(searchInput)searchInput.addEventListener("input",function(){
var q=this.value.trim();
if(q.length<1){productList.innerHTML="";return;}
clearTimeout(st);
st=setTimeout(function(){
fetch("/api/products/search?q="+encodeURIComponent(q)+"&lang="+L()).then(function(r){return r.json()}).then(function(items){
productList.innerHTML="";
items.slice(0,8).forEach(function(p){
var div=document.createElement("div");
div.style.cssText="display:flex;justify-content:space-between;padding:10px;cursor:pointer;border-bottom:1px solid rgba(128,128,128,0.1)";
div.innerHTML="<span>"+p.name+"</span><span class='muted'>"+p.calories+" "+KCAL()+"/100 "+GR()+"</span>";
div.addEventListener("click",function(){
selectedProduct=p;
var mt=document.getElementById("gram-modal-title");if(mt)mt.textContent=p.name;
var mi=document.getElementById("gram-modal-info");if(mi)mi.textContent=p.calories+" "+KCAL()+"/100 "+GR();
if(gramInput)gramInput.value=100;
updatePreview();
if(modal)modal.classList.remove("hidden");
});
productList.appendChild(div);
});
});
},200);
});

function updatePreview(){
if(!selectedProduct||!gramPreview)return;
var g=parseFloat(gramInput.value)||0;var ratio=g/100;
gramPreview.innerHTML=Math.round(selectedProduct.calories*ratio)+" "+KCAL()+" | "+macroStr(selectedProduct.protein*ratio,selectedProduct.fat*ratio,selectedProduct.carbs*ratio);
}
if(gramInput)gramInput.addEventListener("input",updatePreview);
var cancelBtn=document.getElementById("gram-cancel");
if(cancelBtn)cancelBtn.addEventListener("click",function(){if(modal)modal.classList.add("hidden")});
var confirmBtn=document.getElementById("gram-confirm");
if(confirmBtn)confirmBtn.addEventListener("click",function(){
if(!selectedProduct)return;
var g=parseFloat(gramInput.value)||100;var ratio=g/100;
var body={product_name:selectedProduct.name,grams:g,calories:Math.round(selectedProduct.calories*ratio),protein:Math.round(selectedProduct.protein*ratio*10)/10,fat:Math.round(selectedProduct.fat*ratio*10)/10,carbs:Math.round(selectedProduct.carbs*ratio*10)/10,meal_type:currentMeal};
fetch("/api/food",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body)}).then(function(){
if(modal)modal.classList.add("hidden");
if(searchInput)searchInput.value="";
if(productList)productList.innerHTML="";
loadTotals();loadMealLog();
});
});
loadTotals();loadMealLog();
}

function initWater(){
var totalEl=document.getElementById("water-total");
var ring=document.getElementById("water-ring");
var logEl=document.getElementById("water-history");
var goal=2500;

function load(){
fetch("/api/water/today").then(function(r){return r.json()}).then(function(data){
var total=0;data.forEach(function(x){total+=x.amount_ml});
if(totalEl)totalEl.textContent=total;
if(ring){var pct=goal>0?total/goal:0;var r=86;var circ=2*Math.PI*r;ring.style.strokeDasharray=circ;ring.style.strokeDashoffset=circ*(1-Math.min(pct,1));}
if(logEl){logEl.innerHTML="";if(data.length===0){logEl.innerHTML='<p class="muted" style="text-align:center">---</p>';}else{data.forEach(function(item){
var div=document.createElement("div");
div.style.cssText="display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid rgba(128,128,128,0.1)";
div.innerHTML="<span>"+item.amount_ml+" "+ML()+"</span><span class='muted'>"+(item.created_at||"").substring(11,16)+"</span>";
logEl.appendChild(div);
});}}
});}

document.querySelectorAll(".water-btn").forEach(function(btn){
btn.addEventListener("click",function(){
var amount=parseInt(btn.getAttribute("data-ml"));
if(amount>0){fetch("/api/water",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({amount_ml:amount})}).then(function(){load()});}
});
});

var customForm=document.getElementById("water-custom-form");
if(customForm){customForm.addEventListener("submit",function(e){
e.preventDefault();
var inp=this.querySelector("input[name=custom_ml]");
var amount=parseInt(inp.value);
if(amount>0){fetch("/api/water",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({amount_ml:amount})}).then(function(){inp.value="";load()});}
});}

var undoBtn=document.getElementById("undo-water-btn");
if(undoBtn)undoBtn.addEventListener("click",function(){fetch("/api/water/undo",{method:"DELETE"}).then(function(){load()});});

load();
}

function initWeight(){
var form=document.getElementById("weight-form");
var canvas=document.getElementById("weight-chart");
var historyEl=document.getElementById("weight-history");
if(!form||!canvas)return;
var ctx=canvas.getContext("2d");

function fmtDate(s){
if(!s)return"";
var parts=s.split("-");
if(parts.length===3)return parts[2]+"."+parts[1];
return s;
}

function drawChart(data){
if(data.length===0){ctx.clearRect(0,0,canvas.width,canvas.height);return;}
var W=canvas.width=canvas.parentElement.clientWidth;var H=canvas.height=220;
ctx.clearRect(0,0,W,H);
var weights=data.map(function(d){return d.weight});
var dates=data.map(function(d){return d.log_date});
var mn=Math.min.apply(null,weights)-1;var mx=Math.max.apply(null,weights)+1;
if(mn===mx){mn-=1;mx+=1;}
var pad=40,padB=55,gW=W-pad*2,gH=H-pad-padB;
ctx.strokeStyle="rgba(255,255,255,0.1)";ctx.lineWidth=1;
for(var i=0;i<5;i++){var y=pad+gH*i/4;ctx.beginPath();ctx.moveTo(pad,y);ctx.lineTo(W-pad,y);ctx.stroke();var val=mx-(mx-mn)*i/4;ctx.fillStyle="#98989d";ctx.font="11px sans-serif";ctx.textAlign="right";ctx.fillText(val.toFixed(1),pad-6,y+4);}
var pts=[];
for(var i=0;i<data.length;i++){var x=data.length===1?W/2:pad+(gW*i/(data.length-1));var y=pad+gH*(1-(weights[i]-mn)/(mx-mn));pts.push({x:x,y:y});}
ctx.fillStyle="#98989d";ctx.font="10px sans-serif";ctx.textAlign="center";
var step=Math.max(1,Math.floor(data.length/6));
for(var i=0;i<data.length;i+=step){ctx.save();ctx.translate(pts[i].x,H-padB+14);ctx.fillText(fmtDate(dates[i]),0,0);ctx.restore();}
var grad=ctx.createLinearGradient(0,pad,0,H-padB);grad.addColorStop(0,"rgba(0,113,227,0.25)");grad.addColorStop(1,"rgba(0,113,227,0)");
ctx.beginPath();ctx.moveTo(pts[0].x,H-padB);for(var i=0;i<pts.length;i++)ctx.lineTo(pts[i].x,pts[i].y);ctx.lineTo(pts[pts.length-1].x,H-padB);ctx.closePath();ctx.fillStyle=grad;ctx.fill();
ctx.beginPath();ctx.moveTo(pts[0].x,pts[0].y);for(var i=1;i<pts.length;i++)ctx.lineTo(pts[i].x,pts[i].y);ctx.strokeStyle="#0071e3";ctx.lineWidth=2.5;ctx.lineJoin="round";ctx.stroke();
for(var i=0;i<pts.length;i++){ctx.beginPath();ctx.arc(pts[i].x,pts[i].y,5,0,Math.PI*2);ctx.fillStyle="#0071e3";ctx.fill();ctx.beginPath();ctx.arc(pts[i].x,pts[i].y,2.5,0,Math.PI*2);ctx.fillStyle="#1c1c1e";ctx.fill();}
}

function renderHistory(data){
if(!historyEl)return;
historyEl.innerHTML="";
if(data.length===0){historyEl.innerHTML='<p class="muted" style="text-align:center;padding:12px">---</p>';return;}
var sorted=data.slice().reverse();
sorted.forEach(function(item){
var div=document.createElement("div");
div.style.cssText="display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(128,128,128,0.15)";
var kg=isRu()?"\u043a\u0433":"kg";
div.innerHTML='<div><strong>'+item.weight+' '+kg+'</strong><br><span class="muted" style="font-size:12px">'+fmtDate(item.log_date)+'</span></div><button style="background:none;border:none;color:#ff453a;font-size:22px;cursor:pointer;padding:4px 8px" data-id="'+item.id+'">\u00d7</button>';
div.querySelector("button").addEventListener("click",function(){
fetch("/api/weight/"+this.getAttribute("data-id"),{method:"DELETE"}).then(function(){loadAll();});
});
historyEl.appendChild(div);
});
}

function loadAll(){
fetch("/api/weight/history").then(function(r){return r.json()}).then(function(data){
drawChart(data);
renderHistory(data);
});
}

form.addEventListener("submit",function(e){
e.preventDefault();
var wv=parseFloat(new FormData(form).get("weight"));
if(!wv||wv<20||wv>400)return;
fetch("/api/weight",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({weight:wv})}).then(function(){form.reset();loadAll();});
});
loadAll();
}

function goAfterAuth(){
var cal=localStorage.getItem("user_cal");
if(cal){location.href="/dashboard";}else{location.href="/onboarding";}
}

function initProfile(){
var authSec=document.getElementById("auth-section");
var profSec=document.getElementById("profile-section");
var errEl=document.getElementById("auth-error");
var token=getToken();
if(token){checkAuth()}else{showAuth()}

function showAuth(){if(authSec)authSec.classList.remove("hidden");if(profSec)profSec.classList.add("hidden")}
function showProf(){if(authSec)authSec.classList.add("hidden");if(profSec)profSec.classList.remove("hidden")}

var showReg=document.getElementById("show-register");
var showLog=document.getElementById("show-login");
var showLogWrap=document.getElementById("show-login-wrap");
if(showReg)showReg.addEventListener("click",function(e){e.preventDefault();document.getElementById("login-form").classList.add("hidden");document.getElementById("register-form").classList.remove("hidden");showReg.parentElement.style.display="none";if(showLogWrap)showLogWrap.style.display="block";});
if(showLog)showLog.addEventListener("click",function(e){e.preventDefault();document.getElementById("register-form").classList.add("hidden");document.getElementById("login-form").classList.remove("hidden");if(showLogWrap)showLogWrap.style.display="none";showReg.parentElement.style.display="block";});

var loginForm=document.getElementById("login-form");
if(loginForm)loginForm.addEventListener("submit",function(e){e.preventDefault();if(errEl)errEl.textContent="";var fd=new FormData(this);fetch("/api/auth/login",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:fd.get("email"),password:fd.get("password")})}).then(function(r){if(!r.ok)return r.json().then(function(d){throw d});return r.json()}).then(function(d){setToken(d.token);goAfterAuth();}).catch(function(d){if(errEl)errEl.textContent=d.error||"Error";});});

var regForm=document.getElementById("register-form");
if(regForm)regForm.addEventListener("submit",function(e){e.preventDefault();if(errEl)errEl.textContent="";var fd=new FormData(this);fetch("/api/auth/register",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({email:fd.get("email"),name:fd.get("name"),password:fd.get("password")})}).then(function(r){if(!r.ok)return r.json().then(function(d){throw d});return r.json()}).then(function(d){setToken(d.token);goAfterAuth();}).catch(function(d){if(errEl)errEl.textContent=d.error||"Error";});});

function checkAuth(){fetch("/api/auth/me",{headers:{"Authorization":"Bearer "+getToken()}}).then(function(r){if(!r.ok){clearToken();showAuth();return null}return r.json()}).then(function(u){if(!u)return;showProf();var pn=document.getElementById("profile-name");if(pn)pn.value=u.name;var pe=document.getElementById("profile-email");if(pe)pe.value=u.email;var letter=document.getElementById("avatar-letter");var img=document.getElementById("avatar-img");if(u.avatar_path&&img){img.src=u.avatar_path+"?t="+Date.now();img.style.display="block";if(letter)letter.style.display="none"}else if(letter){letter.textContent=(u.name||u.email)[0].toUpperCase();letter.style.display="block";if(img)img.style.display="none"}});}

var profForm=document.getElementById("profile-form");
if(profForm)profForm.addEventListener("submit",function(e){e.preventDefault();var name=document.getElementById("profile-name").value;fetch("/api/auth/profile",{method:"PUT",headers:{"Content-Type":"application/json","Authorization":"Bearer "+getToken()},body:JSON.stringify({name:name})}).then(function(){alert(isRu()?"\u0421\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u043e!":"Saved!")});});

var avatarWrap=document.getElementById("avatar-wrap");
if(avatarWrap)avatarWrap.addEventListener("click",function(e){e.preventDefault();document.getElementById("avatar-input").click();});
var avatarInput=document.getElementById("avatar-input");
if(avatarInput)avatarInput.addEventListener("change",function(){var file=this.files[0];if(!file)return;var fd=new FormData();fd.append("file",file);fetch("/api/upload/avatar",{method:"POST",headers:{"Authorization":"Bearer "+getToken()},body:fd}).then(function(r){return r.json()}).then(function(d){if(d.avatar_path){var img=document.getElementById("avatar-img");if(img){img.src=d.avatar_path+"?t="+Date.now();img.style.display="block";}var letter=document.getElementById("avatar-letter");if(letter)letter.style.display="none"}});});

var logoutBtn=document.getElementById("logout-btn");
if(logoutBtn)logoutBtn.addEventListener("click",function(){clearToken();location.href="/profile"});
}

function initGoals(){
var streakEl=document.getElementById("streak-num");
var streakMsg=document.getElementById("streak-msg");
if(!streakEl)return;

fetch("/api/goals/streak").then(function(r){return r.json()}).then(function(d){
var s=d.streak||0;
streakEl.textContent=s;
}).catch(function(){});

fetch("/api/achievement-stats").then(function(r){return r.json()}).then(function(S){
}).catch(function(){});
}

function setBar(id,pct){var el=document.getElementById(id);if(el)el.style.width=Math.min(pct,100)+"%";}


