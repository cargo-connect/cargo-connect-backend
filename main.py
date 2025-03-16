from fastapi import FastAPI
from routers.user_auth_router import user_auth

app = FastAPI()
app.include_router(user_auth.router)


@app.get("/")
def home():
    return {"message": "Welcome to Cargo-Connect!"}
