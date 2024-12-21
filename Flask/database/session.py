from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("sqlite:///sample.db?charset=utf8")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# For FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()