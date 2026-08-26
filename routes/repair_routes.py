from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session
from database.database import get_db
from models.repair_model import Repair, RepairUpdate, RepairOut
import services.repair_services as repair_services
from datetime import datetime
from utils.auth import get_current_user
# pour les logs 
import services.activity_log_service as activity_log_services
from models.activity_log_model import ActivityLog, ActionType


router = APIRouter(tags=["Réparations"])


@router.get("/repairs", response_model=list[RepairOut])
def get_repair_list_route(db: Session = Depends(get_db)):
    return repair_services.get_all_repair_services(db)


@router.get("/repairs/{repair_id}", response_model=RepairOut)
def get_repair_route(repair_id : int , db :Session = Depends(get_db)):
    return repair_services.get_one_repair_services(repair_id, db)


@router.post("/repairs", response_model=RepairOut)
def create_repair_route(repair_created: Repair, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    repair_created.user_id = current_user.id
    repair_created.date_reparation = datetime.now()
    result = repair_services.create_repair_services(repair_created, db)

    log = ActivityLog(username=current_user.username, action=ActionType.CREATE, objet="repair")
    activity_log_services.create_activity_log_service(log, db)

    return result


@router.patch("/repairs/{repair_id}", response_model=RepairOut)
def update_repair_route( repair_id : int, repair_updated: RepairUpdate, db : Session = Depends(get_db), current_user = Depends(get_current_user)):
    result = repair_services.update_repair_patch_services(repair_id, repair_updated, db)
    log = ActivityLog(username=current_user.username, action=ActionType.UPDATE, objet="repair")
    activity_log_services.create_activity_log_service(log, db)
    return result

