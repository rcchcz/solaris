from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy import func
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

# @router.get("/list", response_model=List[ProductResponse])
# def list_products(db: Session = Depends(get_db)) -> List[Product]:
#     return db.query(Product).all()

@router.get("/list", response_model=List[ProductResponse])
def list_products(page: int = Query(1, gt=0), page_size: int = Query(10, gt=0), db: Session = Depends(get_db)) -> List[Product]:
    total_items = db.query(func.count(Product.id)).scalar()
    total_pages = (total_items + page_size - 1) // page_size
    # TODO: move this to exceptions_handler section
    if page > total_pages:
        raise HTTPException(status_code=404, detail="Page not found.")
    skip = (page - 1) * page_size
    products = db.query(Product).offset(skip).limit(page_size).all()
    return products

@router.get("/{id_product}", response_model=ProductResponse)
def product_by_id(id_product: int, db: Session = Depends(get_db)) -> ProductResponse:
    product: Product = db.query(Product).get(id_product)

    if product is None:
        raise NotFound('Product')
    
    return product