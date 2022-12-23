from datetime import datetime

from sqlalchemy.sql import func
from sqlmodel import Column
from sqlmodel import DateTime
from sqlmodel import Field
from sqlmodel import SQLModel


class Tenant(SQLModel, table=True):
    __tablename__ = "tenants"
    id: int = Field(default=None, primary_key=True)
    name: str


class Toy(SQLModel, table=True):
    __tablename__ = "toys"
    id: int = Field(default=None, primary_key=True)
    tenant_id: int = Field(foreign_key="tenants.id", nullable=False, default=None)
    name: str
