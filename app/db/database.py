from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
)

# session factory เดียวพอ
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# dependency สำหรับ FastAPI
async def get_db():
    async with async_session() as session:
        yield session
