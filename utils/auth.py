from fastapi import Request, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
import services.user_services as user_services
from models.user_model import UserRole

def get_current_user(request: Request, db: Session = Depends(get_db)):
    username = request.cookies.get("Session_user")
    if username is None:
        raise HTTPException(status_code=403, detail="Non connecté")

    current_user = user_services.get_user_by_username_dashboard(username, db)
    if current_user is None:
        raise HTTPException(status_code=403, detail="Non connecté")

    return current_user


def require_admin(current_user = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Réservé aux administrateurs")
    return current_user