from sqlalchemy.orm import Session
from database.activity_log_db import ActivityLogDB
from models.activity_log_model import ActivityLog
from datetime import datetime


def create_activity_log_repo(log_created: ActivityLog, db: Session):
    log_db = ActivityLogDB(
        username=log_created.username,
        action=log_created.action,
        objet=log_created.objet,
        date_action=datetime.now()
    )
    db.add(log_db)
    db.commit()



def get_last_activity_log_repo( db : Session):
    return db.query(ActivityLogDB).order_by(ActivityLogDB.date_action.desc()).limit(10).all()