import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from app.middleware.postgres_rls import get_global_tenant_id


DATABASE_URL = f"postgresql+asyncpg://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@{os.environ['POSTGRES_WRITER_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)


async def get_superuser_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        yield session


async def get_session() -> AsyncSession:
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        try:
            tenant_id = int(get_global_tenant_id())
            query = text(f"SET app.current_tenant={tenant_id};")
            await session.execute(text("SET SESSION ROLE tenant_user;"))
            await session.execute(query)
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.execute(text("RESET ROLE;"))
            await session.commit()
            pass
