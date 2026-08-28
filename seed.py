from database.database import SessionLocal
from database.user_db import UserDB
from utils.security import hash_password

db = SessionLocal()

existing_admin = db.query(UserDB).filter(UserDB.is_admin == True).first()

if existing_admin:
    print("Un admin existe déjà, aucune action effectuée.")
else:
    admin = UserDB(
        username="admin",
        password=hash_password("admin123"),
        is_admin=True
    )
    db.add(admin)
    db.commit()
    print("Compte admin créé : username='admin', password='admin123'")

db.close()