from pydantic import BaseModel, EmailStr


class UserRegisterCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
