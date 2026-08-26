from sqlalchemy import Column, Integer, String, DateTime, Enum as SqlEnum
from database.database import Base
from models.activity_log_model import ActionType


class ActivityLogDB(Base):
    __tablename__ = "activity_logs"
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    action = Column(SqlEnum(ActionType), nullable=False)
    objet = Column(String, nullable=False)
    date_action = Column(DateTime, nullable=False)