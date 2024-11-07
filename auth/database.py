from fastapi import Depends
from datetime import datetime
from typing import AsyncGenerator
from sqlalchemy.orm import DeclarativeBase
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import TIMESTAMP, Column, String, Boolean, Integer, VARCHAR, ARRAY

DATABASE_URL = f"postgresql+asyncpg://postgres:345456zahar@localhost:5432/hakaton?async_fallback=True"

class Base(DeclarativeBase):
    pass

class User(SQLAlchemyBaseUserTable[int], Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=True)
    username = Column(VARCHAR, nullable=False)
    password_hash = Column(String(length=8), nullable=False)
    phone = Column(String, nullable=False)
    preferences = Column(ARRAY(Integer))
    refresh_token = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)
    update_at = Column(TIMESTAMP, default=datetime.utcnow)
    deleted_at = Column(TIMESTAMP, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    is_verified = Column(Boolean, default=False)


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)
