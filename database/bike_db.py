from sqlalchemy import Column, Integer, String
from database.database import Base

class BikeDB(Base):
    __tablename__ = "bikes"
    id = Column(Integer, primary_key=True)
    bike_number = Column(String, unique=True, nullable=False)
    attribution_nom = Column(String, nullable=True)
    attribution_prenom = Column(String, nullable=True)
