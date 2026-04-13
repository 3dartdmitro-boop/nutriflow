from fastapi import APIRouter, UploadFile, File, Request
from fastapi.responses import JSONResponse
from app.services.auth import decode_token
from app.services.database import get_db
import os
import uuid

router = APIRouter(prefix="/api")

AVATAR_DIR = "app/static/avatars"


@router.post("/upload/avatar")
async def upload_avatar(request: Request, file: UploadFile = File(...)):
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return JSONResponse(status_code=401, content={"error": "Not authenticated"})
    token = auth.split(" ")[1]
    user_id = decode_token(token)
    if not user_id:
        return JSONResponse(status_code=401, content={"error": "Invalid token"})

    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"{user_id}_{uuid.uuid4().hex[:8]}.{ext}"
    filepath = os.path.join(AVATAR_DIR, filename)

    content = await file.read()
    with open(filepath, "wb") as f:
        f.write(content)

    avatar_url = f"/static/avatars/{filename}"
    db = get_db()
    db.execute("UPDATE users SET avatar_path = ? WHERE id = ?", (avatar_url, user_id))
    db.commit()

    return {"avatar_path": avatar_url}