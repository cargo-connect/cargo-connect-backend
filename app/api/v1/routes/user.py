from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.db.database import get_db
from app.api.v1.schemas.user import UserRegisterCreate,UserResponse,UserLogin,TokenResponse
from app.api.v1.models.user import User
from app.api.v1.services.user import register_user, login_user
from app.api.core.security import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED,)
def register(user: UserRegisterCreate,db: Session = Depends(get_db)) -> UserResponse:
    return register_user(user, db)

@user_router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> TokenResponse:
    return login_user(form_data=form_data, db=db)

@user_router.get("/me",response_model=UserResponse,)
def get_current_user_info(current_user: User = Depends(get_current_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)
