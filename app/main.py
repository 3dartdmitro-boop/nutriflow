from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes.api import router as api_router
from app.routes.pages import router as pages_router
from app.routes.auth_routes import router as auth_router
from app.routes.upload import router as upload_router
from app.routes.meal_plans import router as meal_plans_router
from app.services.database import init_db
from starlette.middleware.gzip import GZipMiddleware

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=500)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/sw.js")
async def service_worker():
    return FileResponse(
        "app/static/sw.js",
        media_type="application/javascript",
        headers={"Service-Worker-Allowed": "/"}
    )


app.include_router(api_router)
app.include_router(pages_router)
app.include_router(auth_router)
app.include_router(upload_router)
app.include_router(meal_plans_router)

init_db()