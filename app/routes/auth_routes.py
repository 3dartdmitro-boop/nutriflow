from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.services.database import get_db
from app.services.auth import hash_password, verify_password, create_token, decode_token

router = APIRouter(prefix="/api/auth")


class RegisterRequest(BaseModel):
    email: str
    name: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class UpdateProfileRequest(BaseModel):
    name: str


@router.post("/register")
def register(data: RegisterRequest):
    db = get_db()
    existing = db.execute("SELECT id FROM users WHERE email = ?", (data.email,)).fetchone()
    if existing:
        return JSONResponse(status_code=400, content={"error": "Email already registered"})
    pw_hash = hash_password(data.password)
    cur = db.execute(
        "INSERT INTO users (email, name, password_hash) VALUES (?, ?, ?)",
        (data.email, data.name, pw_hash),
    )
    db.commit()
    user_id = cur.lastrowid
    token = create_token(user_id)
    return {"token": token, "user": {"id": user_id, "name": data.name, "email": data.email, "avatar_path": ""}}


@router.post("/login")
def login(data: LoginRequest):
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE email = ?", (data.email,)).fetchone()
    if not user:
        return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
    if not verify_password(data.password, user["password_hash"]):
        return JSONResponse(status_code=401, content={"error": "Invalid credentials"})
    token = create_token(user["id"])
    return {"token": token, "user": {"id": user["id"], "name": user["name"], "email": user["email"], "avatar_path": user["avatar_path"]}}


@router.get("/me")
def me(request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchone()
    if not user:
        return JSONResponse(status_code=404, content={"error": "User not found"})
    return {"id": user["id"], "name": user["name"], "email": user["email"], "avatar_path": user["avatar_path"]}


@router.put("/profile")
def update_profile(data: UpdateProfileRequest, request: Request):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})
    db = get_db()
    db.execute("UPDATE users SET name = ? WHERE id = ?", (data.name, user_id))
    db.commit()
    return {"ok": True}