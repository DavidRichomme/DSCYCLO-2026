from database.bike_db import BikeDB
from fastapi import HTTPException
from models.bike_model import Bike, BikeUpdate
from sqlalchemy.orm import Session



def get_all_bikes_repo(db :Session):
    return db.query(BikeDB).order_by(BikeDB.id).all()


def get_one_bike_by_id_repo(bike_id: int, db :Session):
    bike = db.query(BikeDB).filter(BikeDB.id == bike_id).first()
    if bike is None:
        raise HTTPException(status_code=404, detail="Le velo recherché n'existe pas")
    return bike 


def create_bike_repo(bike_created : Bike, db : Session):
     bike_db = BikeDB(bike_number = bike_created.bike_number,
                      attribution_nom = bike_created.attribution_nom,
                      attribution_prenom = bike_created.attribution_prenom)
     db.add(bike_db)
     db.commit()
     db.refresh(bike_db)
     return(bike_db)


def update_bike_put_repo(bike_id : int, bike_updated: Bike, db : Session):
    bike_db = db.query(BikeDB).filter(BikeDB.id == bike_id).first()
    if bike_db is None:
        raise HTTPException(status_code=404, detail="Le velo recherché n'existe pas")

    bike_db.bike_number = bike_updated.bike_number
    bike_db.attribution_nom = bike_updated.attribution_nom
    bike_db.attribution_prenom = bike_updated.attribution_prenom

    db.commit()
    db.refresh(bike_db)
    return bike_db


def update_bike_patch_repo(bike_id : int, bike_updated: BikeUpdate, db : Session):
    bike_db = db.query(BikeDB).filter(BikeDB.id == bike_id).first()
    if bike_db is None:
        raise HTTPException(status_code=404, detail="Le velo recherché n'existe pas")
    # Stockage des champs a modifier 
    update_data = bike_updated.dict(exclude_unset=True)

    # Parcours de tous les champs de update_data 
    for key, value in update_data.items():
        setattr(bike_db, key, value)

    db.commit()
    db.refresh(bike_db)
    return bike_db
    


def delete_bike_by_id_repo(bike_id : int, db : Session):
    bike_db = db.query(BikeDB).filter(BikeDB.id == bike_id).first()
    if bike_db is None:
        raise HTTPException(status_code=404, detail="Le velo recherché n'existe pas")

    db.delete(bike_db)
    db.commit()
    return {"info": f"Le velo n: {bike_db.bike_number} a bien ete supprimé"}