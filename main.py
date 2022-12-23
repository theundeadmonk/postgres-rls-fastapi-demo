from fastapi import Depends, FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_superuser_session, get_session
from app.models import Tenant, Toy
from app.middleware.postgres_rls import PostgresRLSMiddleware


app = FastAPI()
app.add_middleware(PostgresRLSMiddleware)


@app.get("/ping")
async def pong():
    return {"ping": "pong!"}


@app.post("/tenants")
async def create_tenant(
    tenant: Tenant, session: AsyncSession = Depends(get_superuser_session)
):
    tenant = Tenant(name=tenant.name)
    session.add(tenant)
    await session.commit()
    await session.refresh(tenant)
    return tenant


@app.post("/toys")
async def create_toy(toy: Toy, session: AsyncSession = Depends(get_session)):
    toy = Toy(name=toy.name, tenant_id=toy.tenant_id)
    session.add(toy)
    await session.commit()
    await session.refresh(toy)
    return toy


@app.get("/toys", response_model=list[Toy])
async def get_songs(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Toy))
    toys = result.scalars().all()
    return [Toy(name=toy.name, id=toy.id) for toy in toys]
