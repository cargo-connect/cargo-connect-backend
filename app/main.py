from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes import user
from app.api.v1.routes import order


app = FastAPI(
    title="Cargo-Connect API System"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.user_router, prefix="/api/v1")
app.include_router(order.order_router, prefix="/api/v1")


@app.get("/")
def home():
    return {"message": "Welcome to Cargo-Connect!"}
