from sqlalchemy.orm import Session
import repositories.activity_log_repository as activity_log_repository
from models.activity_log_model import ActivityLog


def create_activity_log_service (activity_created : ActivityLog , db : Session):
    return activity_log_repository.create_activity_log_repo(activity_created, db)


def get_last_activiy_log_service(db : Session):
    return activity_log_repository.get_last_activity_log_repo(db)