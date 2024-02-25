from typing import List
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from client.models.client_model import Client

from shared.dependencies import get_db

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

@router.post("/register", response_model=ClienteResponse, status_code=201)
def register_client(client_request: ClienteRequest, db: Session = Depends(get_db)) -> ClienteResponse:
    new_client = Client(**client_request.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    # return ClienteResponse(**new_client.__dict__)
    return new_client