from fastapi import FastAPI
from app.database import Base, engine
from app.initial_data import initialize_roles
from app.users.routes import router as users_router

def create_app() -> FastAPI:
    """
    Crée et configure l'application FastAPI.
    """
    app = FastAPI()

    # Initialiser la base de données et les rôles par défaut
    setup_database()

    # Enregistrer les routeurs
    register_routers(app)

    return app

def setup_database():
    """
    Configure la base de données et initialise les données par défaut.
    """
    Base.metadata.create_all(bind=engine)
    initialize_roles()

def register_routers(app: FastAPI):
    """
    Enregistre les routeurs FastAPI dans l'application.
    """
    app.include_router(users_router)

# Créer l'application
app = create_app()


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur AppointMe  !"}

