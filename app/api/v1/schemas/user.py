from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime


class UserRegisterBase(BaseModel):
    full_name: str
    email: EmailStr
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True
    )


class UserRegisterCreate(UserRegisterBase):
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone_number: str

    model_config = ConfigDict(
        from_attributes=True
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


class TokenPayload(BaseModel):
    sub: str
    exp: datetime
    type: str