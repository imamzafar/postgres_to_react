import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()


@lru_cache
def get_database_url() -> str:
    """Return the database URL from the environment or a sensible local default."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/inventory_db",
    )


DATABASE_URL = get_database_url()

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
Base = declarative_base()


def get_db():
    """Yield a transactional database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
