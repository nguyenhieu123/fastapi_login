from typing import Optional
from pydantic import BaseModel
from pydantic import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserSchema(UserBase):
    user_name: str

    class Config:
        orm_mode = True


class UserCreateSchema(UserSchema):
    password: str

    class Config:
        orm_mode = False


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    email: Optional[str] = None


class Login(BaseModel):
    email: EmailStr
    password: str
