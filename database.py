from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DB_URL = 'postgresql://localhost:5432/postgres'
engine = create_engine(
    SQLALCHEMY_DB_URL,
    pool_pre_ping=True,
    pool_size = 15,
    max_overflow = 0
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Session:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()