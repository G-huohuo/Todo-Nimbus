from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from typing import Generator

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)
Base = declarative_base()

# FastAPI 依赖：直接 yield Session 对象（不要用 @contextmanager）

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()