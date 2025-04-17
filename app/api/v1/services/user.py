from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api.v1.models.user import User
from app.api.v1.schemas.user import UserRegisterCreate, UserLogin, UserResponse
from app.api.core.security import hash_password, verify_password, create_access_token, authenticate_user
from datetime import timedelta
from typing import Dict, Any


def register_user(user: UserRegisterCreate, db: Session) -> UserResponse:
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    hashed_password = hash_password(user.password)
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        id=db_user.id,
        full_name=db_user.full_name,
        email=db_user.email,
        phone_number=db_user.phone_number,
    )


def login_user(form_data: OAuth2PasswordRequestForm, db: Session) -> Dict[str,
                                                                          Any]:
    db_user = authenticate_user(db, form_data.username, form_data.password)

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    access_token = create_access_token(data={"sub": db_user.email},
                                       expires_delta=timedelta(minutes=30))
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": UserResponse(
            id=db_user.id,
            full_name=db_user.full_name,
            email=db_user.email,
            phone_number=db_user.phone_number,
        )
    }
