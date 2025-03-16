from fastapi import APIRouter, HTTPException, status
from schemas.user_auth_schema.user_auth import UserRegisterCreate, UserLogin
from crud.user_auth_crud.user_auth import create_user, authenticate_user

router = APIRouter()


@router.post("/register")
def register_user(user_data: UserRegisterCreate):
    user = create_user(user_data)
    if user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully", "user": user}


@router.post("/login")
def login_user(user_data: UserLogin):
    user = authenticate_user(user_data)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return {"message": "Login successful", "user_id": user['id']}
