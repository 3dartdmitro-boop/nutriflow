from app.services.database import get_db
db = get_db()
tables = db.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    print(t[0])
print("---")
# Check if products stored in JSON or API
import os
for f in os.listdir("app/services"):
    print("service:", f)