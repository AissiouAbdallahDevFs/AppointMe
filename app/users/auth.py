from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from decouple import config
from datetime import datetime, timedelta
from passlib.context import CryptContext

# Configuration JWT
SECRET_KEY = config("SECRET_KEY", default="supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# OAuth2PasswordBearer : permet de récupérer le token dans l'en-tête Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

# Contexte pour hacher les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hachage du mot de passe
def get_password_hash(password: str):
    """
    Hache un mot de passe en utilisant bcrypt.
    """
    return pwd_context.hash(password)


# Vérification du mot de passe
def verify_password(plain_password: str, hashed_password: str):
    """
    Vérifie si un mot de passe en clair correspond à son hash.
    """
    return pwd_context.verify(plain_password, hashed_password)


# Créer un token JWT
def create_access_token(data: dict):
    """
    Crée un token JWT pour l'utilisateur avec une durée de validité.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Vérifier et décoder un token JWT
def verify_access_token(token: str):
    """
    Vérifie la validité d'un token JWT et retourne son payload.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None


# Dépendance pour récupérer l'utilisateur actuel
def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Dépendance FastAPI pour récupérer l'utilisateur courant depuis un token JWT.
    """
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return payload  # Retourne les données du token (par exemple, email)
