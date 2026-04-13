from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/onboarding")
def onboarding(request: Request):
    return templates.TemplateResponse("onboarding.html", {"request": request})

@router.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@router.get("/food")
def food(request: Request):
    return templates.TemplateResponse("food.html", {"request": request})

@router.get("/water")
def water(request: Request):
    return templates.TemplateResponse("water.html", {"request": request})

@router.get("/weight")
def weight(request: Request):
    return templates.TemplateResponse("weight.html", {"request": request})

@router.get("/profile")
def profile(request: Request):
    return templates.TemplateResponse("profile.html", {"request": request})

@router.get("/history")
def history(request: Request):
    return templates.TemplateResponse("history.html", {"request": request})

@router.get("/goals")
def goals(request: Request):
    return templates.TemplateResponse("goals.html", {"request": request})


@router.get("/progress", response_class=HTMLResponse)
def progress_page(request: Request):
    return templates.TemplateResponse("progress.html", {"request": request})


@router.get("/welcome")
def welcome(request: Request):
    return templates.TemplateResponse("welcome.html", {"request": request})


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/reminders", response_class=HTMLResponse)
async def reminders_page(request: Request):
    return templates.TemplateResponse("reminders.html", {"request": request})
