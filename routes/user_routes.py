from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database.database import get_db
from models.user_model import User, UserUpdate, UserOut
import services.user_services as user_services
from utils.auth import require_admin
# Pour les logs
import services.activity_log_service as activity_log_services
from models.activity_log_model import ActivityLog, ActionType


router = APIRouter(tags=["Utilisateurs"])

# ---------------------- METHODES CRUD POUR L'API REST (Fast API) ---------------------------

# ---------------------- METHODES GET USERS ---------------------------
# Récupere tout les users 
@router.get("/users", response_model=list[UserOut])
def get_users_list_route(db: Session = Depends(get_db), current_user = Depends(require_admin)):
    return user_services.get_users_list(db)


# Récupere les user selon leur ID
@router.get("/users/{user_id}", response_model=UserOut)
def get_user_by_id_route(user_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
        return user_services.get_user_by_id(user_id, db)



# ---------------------- METHODES CREATE ET UPDATE USERS ---------------------------
# Crée un user a la liste user_database
@router.post("/users", response_model=UserOut)
def create_user_route(user: User, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    result = user_services.create_user(user, db)
    log = ActivityLog(username=current_user.username, action=ActionType.CREATE, objet="user")
    activity_log_services.create_activity_log_service(log, db)
    return result 


# Mise a jour d'un User a partir de son ID
@router.put("/users/{user_id}", response_model=UserOut)
def put_update_user_route(user_id: int, updated_user: User, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    result = user_services.update_user_by_put(user_id, updated_user, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="user")
    activity_log_services.create_activity_log_service(log, db)
    return result


# Mise a jour d'un user (certain champs seulement) a partir d'un ID 
@router.patch("/users/{user_id}", response_model=UserOut)
def patch_update_user_route(user_id: int, updated_user: UserUpdate, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    result = user_services.update_user_by_patch(user_id, updated_user, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="user")
    activity_log_services.create_activity_log_service(log, db)
    return result


# ---------------------- METHODE DELETE USER---------------------------
# Supprime un user de la liste user_database
@router.delete("/users/{user_id}")
def delete_user_route(user_id: int, db: Session = Depends(get_db), current_user = Depends(require_admin)):
    result = user_services.delete_user_by_id(user_id, db)
    log = ActivityLog(username=current_user.username, action=ActionType.DELETE, objet="user")
    activity_log_services.create_activity_log_service(log, db)
    return result 

