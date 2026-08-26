from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi import Form
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import User
from services.user_services import get_user_by_username
from utils.security import verify_password
# pour les logs 
from utils.auth import get_current_user
import services.activity_log_service as activity_log_services
from models.activity_log_model import ActionType, ActivityLog


router = APIRouter(tags=["Login"])
templates = Jinja2Templates(directory="templates")


# Route qui affiche le formulaire sur la page login.html
@router.get("/login")
def login_get_route(request :Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login_post_route(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = get_user_by_username(username, db)

    if user is None or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Identifiants incorrects"})

# Redirection et initialisation du cookie de session
    response = RedirectResponse("/onboarding", status_code=303)
    response.set_cookie(key= "Session_user", value=user.username)

# tracage des logs 
    log = ActivityLog(username=user.username, action=ActionType.LOGIN, objet="login")
    activity_log_services.create_activity_log_service(log, db)
    return response


@router.get("/logout")
def logout_get_route(db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    response = RedirectResponse("/login", status_code=307)
    response.delete_cookie(key="Session_user")

    log = ActivityLog(username=current_user.username, action=ActionType.LOGOUT, objet="login")
    activity_log_services.create_activity_log_service(log, db)

    return response