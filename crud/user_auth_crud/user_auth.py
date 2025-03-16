from passlib.context import CryptContext
from schemas.user_auth_schema.user_auth import UserRegisterCreate, UserLogin


user_db = {}


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_user(user_data: UserRegisterCreate):
    if user_data.email in user_db:
        return None

    hashed_password = hash_password(user_data.password)
    user_id = len(user_db) + 1

    user_db[user_data.email] = {
        "id": user_id,
        "full_name": user_data.full_name,
        "email": user_data.email,
        "password_hash": hashed_password,
        "phone_number": user_data.phone_number,
    }

    return user_db[user_data.email]


def authenticate_user(user_data: UserLogin):
    user = user_db.get(user_data.email)
    if not user or not verify_password(user_data.password,
                                       user["password_hash"]):
        return None
    return user
