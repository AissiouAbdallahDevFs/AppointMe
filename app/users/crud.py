from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.users import models, schemas
from app.users.auth import get_password_hash



def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate, role_name: str = "user"):
    # Récupérer le rôle
    role = db.query(models.Roles).filter(models.Roles.name == role_name).first()
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Role '{role_name}' does not exist.",
        )
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,
        role_id=role.id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user