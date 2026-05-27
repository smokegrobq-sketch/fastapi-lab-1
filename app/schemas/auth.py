from pydantic import BaseModel, EmailStr, Field

from app.schemas.users import UserCreate, UserRead


class UserRegister(UserCreate):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead
