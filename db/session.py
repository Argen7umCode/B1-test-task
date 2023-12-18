import os
from typing import Generator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base

DATABASE_URL = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5432/postgres'

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# Dependency
def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()
