from sqlalchemy import Column, Integer, String
from database.database import Base

class PieceDB(Base):
    __tablename__ = "pieces"
    id = Column(Integer, primary_key=True)
    libelle_piece = Column(String, unique=True, nullable=False)
    reference_piece = Column(String, unique= True, nullable=False)
    qte_stock_piece = Column(Integer, nullable =False)