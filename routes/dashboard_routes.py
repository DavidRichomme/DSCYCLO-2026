from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import UserRole
import services.user_services as user_services
import services.bike_services as bike_services
import services.piece_services as piece_services
import services.repair_services as repair_services

router = APIRouter(tags=["Dashboard"])
templates = Jinja2Templates(directory="templates")


@router.get("/dashboard")
def dashboard(request: Request, entite: str = "bikes", edit_id : int = None, db: Session = Depends(get_db)):

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

# Test pour rediriger les non admin vers bikes plutot que users car ils ne doivent pas y avoir accès
    if entite == "users" and current_user.role != UserRole.ADMIN:
        return RedirectResponse("/dashboard?entite=bikes")

    edit_item = None
    
    if entite == "users":
        data = user_services.get_users_list(db)
        if edit_id is not None:
            edit_item = user_services.get_user_by_id(edit_id, db)
    elif entite == "bikes":
        data = bike_services.get_bike_list(db)
        if edit_id is not None:
            edit_item = bike_services.get_bike_by_id(edit_id, db)
    elif entite == "pieces":
        data = piece_services.get_all_pieces_services(db)
        if edit_id is not None:
            edit_item = piece_services.get_one_piece_by_id_services(edit_id, db)
    elif entite == "repairs":
        data = repair_services.get_all_repair_services(db)
        if edit_id is not None:
            edit_item = repair_services.get_one_repair_services(edit_id , db)

    bikes_list = bike_services.get_bike_list(db)
    users_list = user_services.get_users_list(db)
    pieces_list = piece_services.get_all_pieces_services(db)


    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "data": data,
        "entite": entite,
        "current_user": current_user,
        "edit_item" : edit_item,
        "bikes_list" : bikes_list,
        "users_list" : users_list, 
        "pieces_list" : pieces_list
    })