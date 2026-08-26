from models.user_model import User ,UserUpdate
import repositories.user_repository as user_repository
from sqlalchemy.orm import Session


def get_users_list(db :Session):
    return user_repository.get_all_users_repo(db)


def get_user_by_id(user_id: int, db :Session):
    return user_repository.get_one_user_repo(user_id, db)

def get_user_by_username(username: str, db: Session):
    return user_repository.get_user_by_username_repo(username, db)

def get_user_by_username_dashboard(username : str ,db : Session):
    return user_repository.get_user_by_username_for_dashboard_repo(username ,db)

def create_user(user: User, db :Session):
    return user_repository.create_user_repo(user, db)


def update_user_by_put(user_id:int, updated_user:User, db :Session):
    return user_repository.update_user_put_repo(user_id, updated_user, db)


def update_user_by_patch(user_id: int , updated_user : UserUpdate, db :Session):
    return user_repository.update_user_patch_repo(user_id , updated_user, db)


def delete_user_by_id(user_id : int, db :Session):
    return user_repository.delete_user_by_id_repo(user_id, db)
