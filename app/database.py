from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os


# USA A VARIÁVEL DE AMBIENTE 'DATABASE_URL'.
# Se não for definida, usa o 'sqlite:///./contracts.db' como fallback.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./contracts.db")

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
