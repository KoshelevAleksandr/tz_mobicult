from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from config import DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME

# DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


# engine = create_async_engine(DATABASE_URL)
# async_session_maker = sessionmaker(bind=engine, class_=AsyncSession,  expire_on_commit=False)
#
#
# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session

DATABASE_LOCAL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
local_engine = create_engine(DATABASE_LOCAL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=local_engine)


def get_session():

    session = Session()
    try:
        yield session
    finally:
        session.close()


