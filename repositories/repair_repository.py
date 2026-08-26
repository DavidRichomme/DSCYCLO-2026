from sqlalchemy.orm import Session
from models.repair_model import Repair, RepairUpdate, RepairStatus, RepairOut
from database.repair_db import RepairDB, RepairPieceDB
from database.piece_db import PieceDB
from fastapi import HTTPException
from repositories.user_repository import to_user_out



def to_repair_out(repair_db: RepairDB) -> RepairOut:
    return RepairOut(
        id=repair_db.id,
        bike=repair_db.bike,
        user=to_user_out(repair_db.user),
        date_reparation=repair_db.date_reparation,
        commentaire=repair_db.commentaire,
        statut=repair_db.statut,
        pieces=repair_db.pieces
    )


def get_all_repair_repo(db: Session):
    repairs = db.query(RepairDB).order_by(RepairDB.id).all()
    return [to_repair_out(r) for r in repairs]


def get_one_repair_repo(repair_id: int, db: Session):
    repair = db.query(RepairDB).filter(RepairDB.id == repair_id).first()
    if repair is None:
        raise HTTPException(status_code=404, detail="La réparation recherchée n'existe pas")
    return to_repair_out(repair)


def create_repair_repo(repair_created: Repair, db: Session):
    repair_db = RepairDB(
        bike_id=repair_created.bike_id,
        user_id=repair_created.user_id,
        date_reparation=repair_created.date_reparation,
        commentaire=repair_created.commentaire,
        statut=repair_created.statut
    )
    db.add(repair_db)
    db.commit()
    db.refresh(repair_db)

    if repair_created.pieces:
        for piece_input in repair_created.pieces:
            repair_piece_db = RepairPieceDB(
                repair_id=repair_db.id,
                piece_id=piece_input.piece_id,
                quantite=piece_input.quantite
            )
            db.add(repair_piece_db)

        # Décrémente le stock de la pièce utilisée
        piece_db = db.query(PieceDB).filter(PieceDB.id == piece_input.piece_id).first()
        if piece_db:
            piece_db.qte_stock_piece -= piece_input.quantite

        db.commit()

    db.refresh(repair_db)
    return to_repair_out(repair_db)


def update_repair_patch_repo(repair_id: int, repair_updated: RepairUpdate, db: Session):
    repair_db = db.query(RepairDB).filter(RepairDB.id == repair_id).first()
    if repair_db is None:
        raise HTTPException(status_code=404, detail="La réparation recherchée n'existe pas")

    if repair_db.statut == RepairStatus.TERMINE:
        raise HTTPException(status_code=400, detail="Une réparation terminée ne peut plus être modifiée")

    update_data = repair_updated.dict(exclude_unset=True)

    if "pieces" in update_data:
        pieces_value = update_data.pop("pieces")

        # 1. Restaurer le stock des anciennes pièces avant de les supprimer
        anciennes_pieces = db.query(RepairPieceDB).filter(RepairPieceDB.repair_id == repair_id).all()
        for ancienne_piece in anciennes_pieces:
            piece_db = db.query(PieceDB).filter(PieceDB.id == ancienne_piece.piece_id).first()
            if piece_db:
                piece_db.qte_stock_piece += ancienne_piece.quantite

        # 2. Supprimer les anciennes associations
        db.query(RepairPieceDB).filter(RepairPieceDB.repair_id == repair_id).delete()

        # 3. Recréer les nouvelles associations + décrémenter le nouveau stock
        if pieces_value:
            for piece_input in pieces_value:
                repair_piece_db = RepairPieceDB(
                    repair_id=repair_id,
                    piece_id=piece_input["piece_id"],
                    quantite=piece_input["quantite"]
                )
                db.add(repair_piece_db)

                piece_db = db.query(PieceDB).filter(PieceDB.id == piece_input["piece_id"]).first()
                if piece_db:
                    piece_db.qte_stock_piece -= piece_input["quantite"]

    for key, value in update_data.items():
        setattr(repair_db, key, value)

    db.commit()
    db.refresh(repair_db)
    return to_repair_out(repair_db)



def get_last_repairs_repo(db: Session):
    repairs = db.query(RepairDB).order_by(RepairDB.date_reparation.desc()).limit(10).all()
    return [to_repair_out(r) for r in repairs]


def get_suspended_repairs_repo(db: Session):
    repairs = db.query(RepairDB).filter(RepairDB.statut == RepairStatus.SUSPENDU).order_by(RepairDB.date_reparation.desc()).all()
    return [to_repair_out(r) for r in repairs]




