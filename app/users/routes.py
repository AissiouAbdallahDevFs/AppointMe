from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.users import schemas, crud, auth
from app.users.auth import verify_password, create_access_token
from app.users.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],  
)

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db), role: str = "user"):
    db_user = crud.create_user(db=db, user=user, role_name=role)
    return {
        "id": db_user.id,
        "email": db_user.email,
        "is_active": db_user.is_active,
        "role": db_user.role.name,  
    }


# Route pour la connexion
@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}


# Route protégée
@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {"email": current_user["sub"]}