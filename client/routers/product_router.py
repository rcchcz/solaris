from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from client.models.product_model import Product
from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/product")

class ProductResponse(BaseModel):
    id: int
    price: float
    image: str
    brand: str
    title: str
    review_score: float

    class Config:
        orm_model = True

class ProductRequest(BaseModel):
    price: float
    image: str
    brand: str
    title: str
    review_score: float

@router.get("/list", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)) -> List[Product]:
    return db.query(Product).all()

@router.get("/{id_product}", response_model=ProductResponse)
def product_by_id(id_product: int, db: Session = Depends(get_db)) -> ProductResponse:
    product: Product = db.query(Product).get(id_product)

    if product is None:
        raise NotFound('Product')
    
    return product