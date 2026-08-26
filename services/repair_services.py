from sqlalchemy.orm import Session
import repositories.repair_repository as repair_repository
from models.repair_model import Repair, RepairUpdate

def get_all_repair_services (db :Session):
    return repair_repository.get_all_repair_repo(db)

def get_one_repair_services (repair_id : int , db :Session):
    return repair_repository.get_one_repair_repo(repair_id ,db)

def create_repair_services (repair_created : Repair, db : Session):
    return repair_repository.create_repair_repo(repair_created , db)

def update_repair_patch_services(repair_id : int, repair_updated : RepairUpdate, db : Session):
    return repair_repository.update_repair_patch_repo(repair_id, repair_updated, db)



# Pour la page d'onboarding
def get_last_repairs(db :Session):
    return repair_repository.get_last_repairs_repo(db)

def get_suspended_repairs(db : Session):
    return repair_repository.get_suspended_repairs_repo(db)
