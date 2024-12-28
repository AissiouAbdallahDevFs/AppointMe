from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relation avec Roles
    role_id = Column(Integer, ForeignKey("roles.id"))  # Clé étrangère vers la table roles
    role = relationship("Roles", back_populates="users")  # Relation SQLAlchemy

class Roles(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

    # Relation inverse avec User
    users = relationship("User", back_populates="role")  # Relation inverse pour accéder aux utilisateurs
