from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from database.database import Base
from models.repair_model import RepairStatus


class RepairDB(Base):
    __tablename__ = "repairs"
    id = Column(Integer, primary_key=True)
    bike_id = Column(Integer, ForeignKey("bikes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_reparation = Column(DateTime, nullable=False)
    commentaire = Column(String, nullable=True)
    statut = Column(SqlEnum(RepairStatus), nullable=False, default=RepairStatus.A_FAIRE)

    pieces = relationship("RepairPieceDB", back_populates="repair")
    bike = relationship("BikeDB")
    user = relationship("UserDB")


class RepairPieceDB(Base):
    __tablename__ = "repair_piece"
    id = Column(Integer, primary_key=True)
    repair_id = Column(Integer, ForeignKey("repairs.id"), nullable=False)
    piece_id = Column(Integer, ForeignKey("pieces.id"), nullable=False)
    quantite = Column(Integer, nullable=False, default=1)

    repair = relationship("RepairDB", back_populates="pieces")
    piece = relationship("PieceDB")