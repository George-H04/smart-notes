from .settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine(
    url=settings.test_database_url,
    pool_size=settings.pool_size,
    max_overflow=settings.max_overflow,
    pool_timeout=settings.pool_timeout,
    pool_recycle=settings.pool_recycle,
    pool_pre_ping=settings.pool_pre_ping,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
