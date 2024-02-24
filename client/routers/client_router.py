from typing import List
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/client")

class ClienteResponse(BaseModel):
    id: int
    name: str
    email: str

class ClienteRequest(BaseModel):
    name: str
    email: str

@router.get("/list", response_model=List[ClienteResponse])
def list_clients():
    return [
        ClienteResponse(id=1, name="Kassio", email="kassio@mail.com"),
        ClienteResponse(id=2, name="Joao Pedro", email="jp@mail.com"),
        ClienteResponse(id=3, name="Gustvao", email="gustavo@mail.com"),
        ClienteResponse(id=4, name="Eliza", email="eliza@mail.com")
    ]

@router.post("/register", response_model=ClienteResponse, status_code=201)
def register_client(client: ClienteRequest):
    return ClienteResponse(id=5, name=client.name, email=client.email)