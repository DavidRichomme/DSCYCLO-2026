from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routes.user_routes import router as user_router
from routes.bike_routes import router as bike_router
from routes.piece_routes import router as piece_router
from routes.repair_routes import router as repair_router
from routes.dashboard_routes import router as dashboard_router
from routes.onboarding_routes import router as onboarding_router
from routes.auth_routes import router as auth_router
from database.database import Base, engine
from database import user_db, bike_db, piece_db, repair_db, activity_log_db # important : force l'import du modèle pour qu'il soit enregistré


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(user_router)
app.include_router(bike_router)
app.include_router(piece_router)
app.include_router(repair_router)

# Pour l'interface web
app.include_router(dashboard_router)
app.include_router(onboarding_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)