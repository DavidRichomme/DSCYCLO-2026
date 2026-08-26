from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database.database import get_db

import services.user_services as user_services
import services.piece_services as piece_services
import services.repair_services as repair_services
import services.activity_log_service as activity_log_services



router = APIRouter(tags=["Onboarding"])
templates = Jinja2Templates(directory="templates")


@router.get("/onboarding")
def onboarding(request : Request, db : Session = Depends(get_db)):

# Test de l'existance du cookie de session lié au username
# Si le cookie n'existe pas alors redirection vers login
    username = request.cookies.get("Session_user")
    if username is None:
        return RedirectResponse("/login")
        
# Test de l'existance du user meme si le cookie existe
# Si pas de user alors redirection vers login
    current_user = user_services.get_user_by_username_dashboard(username, db)
    if current_user is None: 
        return RedirectResponse("/login")


    last_repairs_list = repair_services.get_last_repairs(db)
    suspended_repairs_list = repair_services.get_suspended_repairs(db)
    pieces_critical_list = piece_services.get_critical_stock_service(db)
    last_activity_logs = activity_log_services.get_last_activiy_log_service(db)

    return templates.TemplateResponse("onboarding.html", {
        "request": request,
        "current_user": current_user,
        "last_repairs" : last_repairs_list,
        "suspended_repairs" : suspended_repairs_list, 
        "critical_stock" : pieces_critical_list,
        "last_activity_logs" : last_activity_logs
    })