from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from uuid import UUID
from datetime import datetime
from typing import List, Optional
from .models import CategoryEnum

class ProductBase(BaseModel):
    name: str = Field(..., max_length=255)
    price: Decimal = Field(..., max_digits=10, decimal_places=2)
    category: CategoryEnum
    stock: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: UUID
    created_at: datetime
    last_modification: datetime
    model_config = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    name: str = Field(..., max_length=255)
    lastname: str = Field(..., max_length=255)
    alias: str = Field(..., max_length=30)
    tel: Optional[str] = Field(None, max_length=30)

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: UUID
    model_config = ConfigDict(from_attributes=True)

class AggregationResponse(BaseModel):
    category: CategoryEnum
    total_stock: int
    average_price: Decimal
    product_count: int

class LoginRequest(BaseModel):
    alias: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
