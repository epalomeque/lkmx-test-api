from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from ..database import get_db
from ..models import Product, User, CategoryEnum
from ..schemas import ProductCreate, Product as ProductSchema, UserCreate, User as UserSchema, AggregationResponse
from ..auth import get_current_user
import uuid

router = APIRouter(dependencies=[Depends(get_current_user)])

# --- Operaciones para Products ---

@router.post("/products", response_model=ProductSchema, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@router.get("/products", response_model=List[ProductSchema])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = db.query(Product).offset(skip).limit(limit).all()
    return products

@router.get("/products/{product_id}", response_model=ProductSchema)
def read_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@router.put("/products/{product_id}", response_model=ProductSchema)
def update_product(product_id: uuid.UUID, product: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: uuid.UUID, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None

# --- Operaciones para Users ---

@router.post("/users", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/users", response_model=List[UserSchema])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# --- Agregaciones / Reportes ---

@router.get("/reports/products/category", response_model=List[AggregationResponse])
def get_products_aggregation(db: Session = Depends(get_db)):
    results = db.query(
        Product.category,
        func.sum(Product.stock).label("total_stock"),
        func.avg(Product.price).label("average_price"),
        func.count(Product.id).label("product_count")
    ).group_by(Product.category).all()
    
    return [
        AggregationResponse(
            category=r.category,
            total_stock=r.total_stock,
            average_price=r.average_price,
            product_count=r.product_count
        ) for r in results
    ]
