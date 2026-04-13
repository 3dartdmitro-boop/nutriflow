path = "app/templates/reminders.html"
f = open(path, "r", encoding="utf-8")
old = f.read()
f.close()

new = '''{% extends "base.html" %}
{% block title %}Reminders{% endblock %}
{% block content %}
<div style="max-width:480px;margin:0 auto;padding:20px;">

    <div style="display:flex;align-items:center;gap:10px;margin-bottom:24px;">
        <a href="/" style="color:var(--accent);text-decoration:none;font-size:20px;">&#8592;</a>
        <h2 style="margin:0;" id="rem-title"></h2>
    </div>

    <div id="perm-banner" style="display:none;background:#1a1a2e;border:1px solid #e74c3c;border-radius:16px;padding:16px;margin-bottom:16px;text-align:center;">
        <div style="font-size:28px;margin-bottom:8px;">&#x1f515;</div>
        <div style="font-size:14px;color:#ccc;margin-bottom:12px;" id="perm-text"></div>
        <button onclick="requestPerm()" id="perm-btn" style="background:var(--accent);color:#fff;border:none;padding:10px 24px;border-radius:12px;font-size:14px;cursor:pointer;"></button>
    </div>

    <div id="rem-cards"></div>

    <div style="margin-top:24px;">
        <h3 style="margin:0 0 12px;" id="active-title"></h3>
        <div id="active-list"></div>
        <div id="no-active" style="display:none;text-align:center;padding:20px;color:#666;font-size:14px;"></div>
    </div>
</div>

<script>
document.addEventListener("DOMContentLoaded", function(){

var RK = "nutriflow_reminders";
var timers = [];

function T(k){
    var lang = L();
    try{return TRANSLATIONS[lang][k]||TRANSLATIONS["ru"][k]||k;}catch(e){return k;}
}

var CARDS = [
    {id:"water", icon:"\\ud83d\\udca7", tk:"rem_water_title", dk:"rem_water_desc", type:"interval", intervals:[60,90,120,180], default_interval:120},
    {id:"food", icon:"\\ud83c\\udf7d\\ufe0f", tk:"rem_food_title", dk:"rem_food_desc", type:"times", default_times:["08:00","12:30","18:30"]},
    {id:"weight", icon:"\\u2696\\ufe0f", tk:"rem_weight_title", dk:"rem_weight_desc", type:"times", default_times:["08:00"]},
    {id:"steps", icon:"\\ud83d\\udeb6", tk:"rem_steps_title", dk:"rem_steps_desc", type:"interval", intervals:[60,90,120], default_interval:90}
];

function getSaved(){try{return JSON.parse(localStorage.getItem(RK))||{};}catch(e){return {};}}
function saveAll(s){localStorage.setItem(RK, JSON.stringify(s));}

function checkPerm(){
    if(!("Notification" in window)){document.getElementById("perm-banner").style.display="none";return;}
    if(Notification.permission==="granted"){document.getElementById("perm-banner").style.display="none";}
    else if(Notification.permission==="denied"){
        document.getElementById("perm-banner").style.display="block";
        document.getElementById("perm-btn").style.display="none";
        document.getElementById("perm-text").textContent=T("rem_perm_blocked");
    } else {
        document.getElementById("perm-banner").style.display="block";
    }
}

window.requestPerm=function(){
    Notification.requestPermission().then(function(p){checkPerm();if(p==="granted")startAllTimers();});
};

function notify(title,body){if(Notification.permission==="granted")new Notification(title,{body:body});}

function renderCards(){
    var g=document.getElementById("rem-cards"); g.innerHTML="";
    var saved=getSaved();

    CARDS.forEach(function(c){
        var s=saved[c.id]||{};
        var isOn=!!s.enabled;
        var d=document.createElement("div");
        d.style.cssText="background:var(--card);border-radius:16px;padding:16px;margin-bottom:12px;";

        var top='<div style="display:flex;align-items:center;gap:14px;">';
        top+='<div style="font-size:32px;width:48px;text-align:center;">'+c.icon+'</div>';
        top+='<div style="flex:1;"><div style="font-weight:600;font-size:15px;">'+T(c.tk)+'</div>';
        top+='<div style="font-size:12px;color:#888;margin-top:2px;">'+T(c.dk)+'</div></div>';

        // Toggle
        top+='<label style="position:relative;width:48px;height:28px;flex-shrink:0;cursor:pointer;" onclick="toggleRem(\''+c.id+'\','+(!isOn)+')">';
        top+='<div style="width:48px;height:28px;border-radius:14px;background:'+(isOn?"var(--accent)":"#444")+';position:relative;transition:.3s;">';
        top+='<div style="position:absolute;top:2px;'+(isOn?"right:2px":"left:2px")+';width:24px;height:24px;border-radius:50%;background:#fff;transition:.3s;"></div>';
        top+='</div></label></div>';

        var controls="";

        if(c.type==="interval"){
            var cur=s.interval||c.default_interval;
            controls='<div style="margin-top:10px;padding-left:62px;display:flex;gap:6px;flex-wrap:wrap;">';
            c.intervals.forEach(function(m){
                var sel=(cur===m&&isOn);
                controls+='<button onclick="setInt(\''+c.id+'\','+m+')" style="padding:4px 10px;border-radius:8px;border:1px solid '+(sel?"var(--accent)":"#444")+';background:'+(sel?"var(--accent)":"transparent")+';color:'+(sel?"#fff":"#aaa")+';font-size:12px;cursor:pointer;">'+m+' '+T("rem_min")+'</button>';
            });
            controls+='</div>';
        }

        if(c.type==="times"){
            var curTimes=s.times||c.default_times;
            controls='<div style="margin-top:10px;padding-left:62px;">';
            controls+='<div style="display:flex;gap:6px;flex-wrap:wrap;align-items:center;" id="times-'+c.id+'">';
            curTimes.forEach(function(t,i){
                controls+='<input type="time" value="'+t+'" onchange="updateTime(\''+c.id+'\','+i+',this.value)" style="padding:4px 8px;border-radius:8px;border:1px solid #444;background:#1a1a2e;color:#fff;font-size:13px;cursor:pointer;">';
            });
            controls+='<button onclick="addTime(\''+c.id+'\')" style="padding:4px 10px;border-radius:8px;border:1px dashed #555;background:transparent;color:#888;font-size:16px;cursor:pointer;">+</button>';
            if(curTimes.length>1){
                controls+='<button onclick="removeLastTime(\''+c.id+'\')" style="padding:4px 10px;border-radius:8px;border:1px dashed #555;background:transparent;color:#e74c3c;font-size:16px;cursor:pointer;">−</button>';
            }
            controls+='</div></div>';
        }

        d.innerHTML=top+controls;
        g.appendChild(d);
    });
    renderActive();
}

window.toggleRem=function(id,on){
    var saved=getSaved();
    if(!saved[id])saved[id]={};
    saved[id].enabled=on;
    var card=CARDS.find(function(c){return c.id===id;});
    if(card&&card.type==="interval"&&!saved[id].interval)saved[id].interval=card.default_interval;
    if(card&&card.type==="times"&&!saved[id].times)saved[id].times=card.default_times.slice();
    saveAll(saved);renderCards();restartTimers();
};

window.setInt=function(id,mins){
    var saved=getSaved();
    if(!saved[id])saved[id]={};
    saved[id].interval=mins;saved[id].enabled=true;
    saveAll(saved);renderCards();restartTimers();
};

window.updateTime=function(id,idx,val){
    var saved=getSaved();
    if(!saved[id])saved[id]={};
    var card=CARDS.find(function(c){return c.id===id;});
    if(!saved[id].times)saved[id].times=(card.default_times||[]).slice();
    saved[id].times[idx]=val;
    saved[id].enabled=true;
    saveAll(saved);renderCards();restartTimers();
};

window.addTime=function(id){
    var saved=getSaved();
    if(!saved[id])saved[id]={};
    var card=CARDS.find(function(c){return c.id===id;});
    if(!saved[id].times)saved[id].times=(card.default_times||[]).slice();
    saved[id].times.push("12:00");
    saved[id].enabled=true;
    saveAll(saved);renderCards();restartTimers();
};

window.removeLastTime=function(id){
    var saved=getSaved();
    if(!saved[id]||!saved[id].times||saved[id].times.length<=1)return;
    saved[id].times.pop();
    saveAll(saved);renderCards();restartTimers();
};

function renderActive(){
    var saved=getSaved();
    var list=document.getElementById("active-list");
    var noEl=document.getElementById("no-active");
    list.innerHTML="";var count=0;

    CARDS.forEach(function(c){
        if(!saved[c.id]||!saved[c.id].enabled)return;
        count++;
        var d=document.createElement("div");
        d.style.cssText="background:var(--card);border-radius:12px;padding:12px 16px;margin-bottom:8px;display:flex;align-items:center;justify-content:space-between;";
        var detail="";
        if(c.type==="interval"){var m=saved[c.id].interval||c.default_interval;detail=T("rem_every")+" "+m+" "+T("rem_min");}
        if(c.type==="times"){detail=(saved[c.id].times||c.default_times).join(", ");}
        d.innerHTML='<div style="display:flex;align-items:center;gap:10px;"><span style="font-size:20px;">'+c.icon+'</span><div><div style="font-size:14px;font-weight:500;">'+T(c.tk)+'</div><div style="font-size:11px;color:#888;">'+detail+'</div></div></div><button onclick="toggleRem(\''+c.id+'\',false)" style="background:none;border:none;color:#e74c3c;font-size:18px;cursor:pointer;">\\u2715</button>';
        list.appendChild(d);
    });
    noEl.style.display=count===0?"block":"none";
}

function clearAllTimers(){timers.forEach(function(t){clearInterval(t);clearTimeout(t);});timers=[];}
function restartTimers(){clearAllTimers();startAllTimers();}

function startAllTimers(){
    if(Notification.permission!=="granted")return;
    var saved=getSaved();
    CARDS.forEach(function(c){
        if(!saved[c.id]||!saved[c.id].enabled)return;
        if(c.type==="interval"){
            var mins=saved[c.id].interval||c.default_interval;
            var t=setInterval(function(){
                var msgs={water:{ru:["Время попить воды! \\ud83d\\udca7"],en:["Time to drink water! \\ud83d\\udca7"]},steps:{ru:["Пора размяться! \\ud83d\\udeb6"],en:["Time to move! \\ud83d\\udeb6"]}};
                var arr=(msgs[c.id]&&msgs[c.id][L()])||["Reminder"];
                notify(T(c.tk),arr[Math.floor(Math.random()*arr.length)]);
            },mins*60*1000);
            timers.push(t);
        }
        if(c.type==="times"){
            (saved[c.id].times||c.default_times).forEach(function(ts){
                scheduleDaily(ts,function(){
                    var msgs={food:{ru:["Время поесть! \\ud83c\\udf7d\\ufe0f"],en:["Time to eat! \\ud83c\\udf7d\\ufe0f"]},weight:{ru:["Запиши вес! \\u2696\\ufe0f"],en:["Log your weight! \\u2696\\ufe0f"]}};
                    var arr=(msgs[c.id]&&msgs[c.id][L()])||["Reminder"];
                    notify(T(c.tk),arr[Math.floor(Math.random()*arr.length)]);
                });
            });
        }
    });
}

function scheduleDaily(ts,cb){
    var p=ts.split(":");var h=parseInt(p[0]),m=parseInt(p[1]||0);
    var now=new Date(),target=new Date();
    target.setHours(h,m,0,0);
    if(target<=now)target.setDate(target.getDate()+1);
    var t=setTimeout(function(){cb();var t2=setInterval(cb,86400000);timers.push(t2);},target-now);
    timers.push(t);
}

document.getElementById("rem-title").textContent=T("rem_title");
document.getElementById("perm-text").textContent=T("rem_perm_text");
document.getElementById("perm-btn").textContent=T("rem_perm_btn");
document.getElementById("active-title").textContent=T("rem_active");
document.getElementById("no-active").textContent=T("rem_no_active");
checkPerm();renderCards();startAllTimers();
});
</script>
{% endblock %}
'''

f = open(path, "w", encoding="utf-8")
f.write(new)
f.close()
print("Done! reminders.html updated")