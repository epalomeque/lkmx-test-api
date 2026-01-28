import uuid
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from .database import Base
import enum

class CategoryEnum(enum.Enum):
    FARMACIA = "FARMACIA"
    ABARROTES = "ABARROTES"
    PANADERIA = "PANADERIA"
    LACTEOS = "LACTEOS"
    CARNES = "CARNES"
    FRUTAS = "FRUTAS"

class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(precision=10, scale=2), nullable=False)
    category = Column(Enum(CategoryEnum), nullable=False)
    stock = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    lastname = Column(String(255), nullable=False)
    alias = Column(String(30), nullable=False)
    tel = Column(String(30)) # El requerimiento dice tel: integer, 30 caracteres. Pero 30 caracteres no cabe en integer. Lo pondré como String(30) o bigint si es numérico.
