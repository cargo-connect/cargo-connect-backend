from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv


load_dotenv()
# DATABASE_URL = os.getenv("DB_URL")
DATABASE_URL = os.getenv("DB_URL", "sqlite:///cargoconnect.db")  # Fallback to SQLite

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# from sqlalchemy import create_engine
# from sqlalchemy.orm import declarative_base, sessionmaker
# import os
# from dotenv import load_dotenv

# load_dotenv()
# # Load from root .env file
# load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

# DB_URL = os.getenv("DB_URL")

# if not DB_URL:
#     raise ValueError("DB_URL environment variable is not set.")

# # SQLite requires special connection args
# if DB_URL.startswith("sqlite://"):
#     engine = create_engine(
#         DB_URL,
#         connect_args={"check_same_thread": False},
#         echo=False
#     )
# else:
#     engine = create_engine(DB_URL, echo=False)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
