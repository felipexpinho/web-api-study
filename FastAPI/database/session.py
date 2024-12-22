from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///sample.db?charset=utf8"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# For FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()