from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os


load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@localhost:5433/bike_repair_db"
# SQLALCHEMY_DATABASE_URL = "sqlite:///./bike_repair.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Methode qui crée la connexion a la database et qui la referme autonmatiquement
# Ca referme aussi la connexion en cas d'erreur
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()