from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from database.database import get_db
from models.bike_model import Bike, BikeUpdate, BikeOut
import services.bike_services as bike_services
from fastapi.templating import Jinja2Templates
# pour les logs 
from utils.auth import get_current_user
import services.activity_log_service as activity_log_services
from models.activity_log_model import ActivityLog, ActionType

router = APIRouter(tags=["Vélos"])
template = Jinja2Templates(directory="templates")

# ---------------------- METHODES CRUD POUR L'API REST (Fast API) Retournent un JSON ou une liste de Json---------------------------

# ---------------------- METHODES GET BIKES ---------------------------
# Récupere tout les bikes 
@router.get("/bikes", response_model=list[BikeOut])
def get_bike_list_route(db: Session = Depends(get_db)):
    return bike_services.get_bike_list(db)

@router.get("/bikes/{bike_id}", response_model=BikeOut)
def get_bike_by_id_route(bike_id : int, db: Session = Depends(get_db)):
    return bike_services.get_bike_by_id(bike_id, db)


# ---------------------- METHODES CREATE ET UPDATE BIKES ---------------------------
@router.post("/bikes", response_model=BikeOut)
def create_bike_route (bike: Bike, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = bike_services.create_bike(bike, db)
    log = ActivityLog(username=current_user.username, action=ActionType.CREATE, objet="bike")
    activity_log_services.create_activity_log_service(log, db)
    return  result

@router.put("/bikes/{bike_id}", response_model=BikeOut)
def update_bike_put_route(bike_id :int , updated_bike : Bike, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = bike_services.update_bike_put(bike_id, updated_bike, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="bike")
    activity_log_services.create_activity_log_service(log, db)
    return result

@router.patch("/bikes/{bike_id}", response_model=BikeOut)
def update_bike_patch_route(bike_id: int, updated_bike : BikeUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = bike_services.update_bike_patch(bike_id, updated_bike, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="bike")
    activity_log_services.create_activity_log_service(log, db)
    return result


# ---------------------- METHODE DELETE BIKE---------------------------
@router.delete("/bikes/{bike_id}")
def delete_user_by_id_route(bike_id : int, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = bike_services.delete_bike_by_id(bike_id, db)
    log = ActivityLog(username=current_user.username, action=ActionType.DELETE, objet="bike")
    activity_log_services.create_activity_log_service(log, db)
    return result



# ---------------------- METHODES CRUD POUR L'API REST (Fast API) Retournent un objet HTTP---------------------------
@router.get("/bikes/page")
def bikes_page(request: Request, db: Session = Depends(get_db)):
    bikes = bike_services.get_bike_list(db)
    return template.TemplateResponse("bikes.html", {"request": request, "bikes": bikes})
