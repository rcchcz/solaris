from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session, joinedload
from client.models.client_model import Client
from client.models.product_model import Product
from client.routers.product_router import ProductResponse
from shared.dependencies import get_db
from client.routers.utils import search_client_by_id
from shared.exceptions import NotFound

router = APIRouter(prefix="/client")

class ClientResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_model = True

class ClientRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=50)

class ClientSchema(ClientResponse):
    favorite_products: List[ProductResponse]

class ClientSchemaRequest(ClientRequest):
    favorite_products: List[int]

class ProductSchema(ProductResponse):
    clients: List[ClientResponse]

# @router.get("/list", response_model=List[ClientResponse])
# def list_clients(db: Session = Depends(get_db)) -> List[Client]:
#     return db.query(Client).order_by(Client.created_at).all()

# TODO: refactor this to use fastapi_pagination
@router.get("/list", response_model=List[ClientSchema])
def list_clients(page: int = Query(1, gt=0), db: Session = Depends(get_db)) -> List[ClientSchema]:
    limit_per_page = 20
    offset = (page - 1) * limit_per_page
    return db.query(Client).options(joinedload(Client.favorite_products)).order_by(Client.created_at).offset(offset).limit(limit_per_page).all()

# @router.get("/{id_client}", response_model=ClientResponse)
# def client_by_id(id_client: int, db: Session = Depends(get_db)) -> ClientResponse:
#     return search_client_by_id(id_client, db)

@router.get("/{id_client}", response_model=ClientSchema)
def client_by_id(id_client: int, db: Session = Depends(get_db)):
    # client = db.query(Client).options(joinedload(Client.favorite_products)).\
    #         where(Client.id == id_client).one()
    client = db.query(Client).options(joinedload(Client.favorite_products)).\
             where(Client.id == id_client).one_or_none()
    
    if client is None:
        raise NotFound('Client')
    
    return client

@router.post("/register", response_model=ClientResponse, status_code=201)
def register_client(client_request: ClientRequest, db: Session = Depends(get_db)) -> ClientResponse:
    # CHECK IF THE EMAIL IS AREADY IN USE
    # TODO: refactor this check to use some sqlalchemy notation
    # TODO: move this to exceptions_handler section
    db_client = db.query(Client).filter(Client.email == client_request.email).first()
    if db_client:
        raise HTTPException(status_code=409, detail="Email already registered.")

    new_client = Client(**client_request.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    # return ClientResponse(**new_client.__dict__)
    return new_client

@router.put("/update/{id_client}", response_model=ClientSchema, status_code=200)
def update_client(id_client: int, client_request: ClientSchemaRequest, db: Session = Depends(get_db)) -> ClientResponse:
    client: ClientSchema = db.query(Client).options(joinedload(Client.favorite_products)).\
             where(Client.id == id_client).one_or_none()
    
    if client is None:
        raise NotFound('Client')
    
    if db.query(Client).filter(Client.email == client_request.email, Client.id != client.id).first():
        raise HTTPException(status_code=409, detail="Email already in use.")

    client.name = client_request.name
    client.email = client_request.email

    # TODO: create an endpoint to just add new favorites instead of update the whole list (?)
    client.favorite_products.clear()
    for product_id in client_request.favorite_products:
        db_product = db.query(Product).filter_by(id=product_id).one_or_none()
        if db_product and db_product not in client.favorite_products:
            client.favorite_products.append(db_product)

    db.add(client)
    db.commit()
    db.refresh(client)

    return client

@router.delete("/delete/{id_client}", status_code=204)
def delete_client(id_client: int, db: Session = Depends(get_db)) -> None:
    client: Client = search_client_by_id(id_client, db)
    db.delete(client)
    db.commit()
