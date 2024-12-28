from app.database import SessionLocal
from app.users.models import Roles

def initialize_roles():
    """
    Insère des rôles par défaut dans la base de données.
    """
    db = SessionLocal()
    try:
        roles = [
            {"name": "admin", "description": "Administrateur du système", "is_active": True},
            {"name": "user", "description": "Utilisateur normal", "is_active": True},
        ]
        for role in roles:
            existing_role = db.query(Roles).filter(Roles.name == role["name"]).first()
            if not existing_role:
                db.add(Roles(**role))
        db.commit()
    finally:
        db.close()
