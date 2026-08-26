from models.bike_model import BikeUpdate, Bike
import repositories.bike_repository as bike_repository
from sqlalchemy.orm import Session


def get_bike_list(db : Session):
    return bike_repository.get_all_bikes_repo(db)

def get_bike_by_id(bike_id : int , db : Session):
    return bike_repository.get_one_bike_by_id_repo(bike_id, db)

def create_bike(bike : Bike, db : Session):
    return bike_repository.create_bike_repo(bike, db)

def update_bike_put(bike_id : int, updated_bike : Bike,  db : Session):
    return bike_repository.update_bike_put_repo(bike_id, updated_bike, db)

def update_bike_patch(bike_id : int, updated_bike : BikeUpdate, db : Session):
    return bike_repository.update_bike_patch_repo(bike_id, updated_bike, db)

def delete_bike_by_id(bike_id: int, db : Session):
    return bike_repository.delete_bike_by_id_repo(bike_id, db)