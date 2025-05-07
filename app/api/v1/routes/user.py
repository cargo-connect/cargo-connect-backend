import os
from fastapi import APIRouter, Depends, status, HTTPException, Query
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.db.database import get_db
from app.api.v1.schemas.user import UserRegisterCreate, UserResponse, TokenResponse
from app.api.v1.models.user import User
from app.api.v1.services.user import register_user, login_user
from app.api.core.security import get_current_user, get_current_verified_user, create_email_verification_token, verify_email_token
from app.api.core.email import send_verification_email

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED,)
async def register(user: UserRegisterCreate, db: Session = Depends(get_db)) -> UserResponse:
    db_user = register_user(user, db)

    token = create_email_verification_token(db_user.email)
    await send_verification_email(db_user.email, token)

    return UserResponse.model_validate(db_user)

@user_router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> TokenResponse:
    return login_user(form_data=form_data, db=db)


@user_router.get("/me", response_model=UserResponse,)
def get_current_user_info(current_user: User = Depends(get_current_verified_user)) -> UserResponse:
    return UserResponse.model_validate(current_user)

@user_router.get("/verify-email")
def verify_email(token: str = Query(...), db: Session = Depends(get_db)):
    user = verify_email_token(token, db)
    user.is_verified = True
    db.commit()
    frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000") # Default to a common frontend dev port if not set
    redirect_url = f"{frontend_url}/auth/login?verification_status=success"
    return RedirectResponse(url=redirect_url)


@user_router.post("/resend-verification")
async def resend_verification_email(current_user: User = Depends(get_current_user)):
    if current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already verified"
        )
    
    token = create_email_verification_token(current_user.email)
    await send_verification_email(current_user.email, token)
    
    return {"message": "Verification email sent successfully"}
