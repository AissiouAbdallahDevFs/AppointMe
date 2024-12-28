from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr  
class UserCreate(UserBase):
    password: str  

class UserResponse(BaseModel):
    id: int
    email: str
    is_active: bool
    role: str  

    class Config:
        orm_mode = True
