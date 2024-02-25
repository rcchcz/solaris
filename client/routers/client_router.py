from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from client.models.client_model import Client

from shared.dependencies import get_db
from shared.exceptions import NotFound

router = APIRouter(prefix="/client")

class ClienteResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_model = True

class ClienteRequest(BaseModel):
    name: str = Field(min_length=3, max_length=50)
    email: str = Field(min_length=3, max_length=50)

@router.get("/list", response_model=List[ClienteResponse])
def list_clients(db: Session = Depends(get_db)) -> List[Client]:
    return db.query(Client).all()

@router.get("/{id_client}", response_model=ClienteResponse)
def client_by_id(id_client: int, db: Session = Depends(get_db)) -> ClienteResponse:
    return search_client_by_id(id_client, db)

@router.post("/register", response_model=ClienteResponse, status_code=201)
def register_client(client_request: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    new_client = Client(**client_request.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    # return ClienteResponse(**new_client.__dict__)
    return new_client

@router.put("/update/{id_client}", response_model=ClienteResponse, status_code=200)
def update_client(id_client: int, client_request: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    client: Client = search_client_by_id(id_client, db)
    client.name = client_request.name
    client.email = client_request.email

    db.add(client)
    db.commit()
    db.refresh(client)

    return client

@router.delete("/delete/{id_client}", status_code=204)
def delete_client(id_client: int, db: Session = Depends(get_db)) -> None:
    client: Client = search_client_by_id(id_client, db)
    db.delete(client)
    db.commit()

# HELPER METHODS
def search_client_by_id(id_client: int, db: Session) -> Client:
    client: Client = db.query(Client).get(id_client)

    if client is None:
        raise NotFound('Client')
    
    return client
