from pydantic import BaseModel, EmailStr


class UserRegisterBase(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone_number: str


class UserRegisterCreate(UserRegisterBase):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str
