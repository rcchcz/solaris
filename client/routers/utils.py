from sqlalchemy.orm import Session
from client.models.client_model import Client
from shared.exceptions import NotFound

def search_client_by_id(id_client: int, db: Session) -> Client:
    client: Client = db.query(Client).get(id_client)

    if client is None:
        raise NotFound('Client')
    
    return client