from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import app
from shared.database import Base
from shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = 'sqlite:///.test.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread':False})
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db


def test_list_clients():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    client.post('/client/register', json={'name': 'Kassio', 'email': 'kassio@mail.com'})
    client.post('/client/register', json={'name': 'Joao Pedro', 'email': 'jp@mail.com'})
    
    response = client.get('/client/list')
    assert response.status_code == 200
    #assert response.json() == [{'id': 1, 'name': 'Kassio', 'email': 'kassio@mail.com'}, {'id': 2, 'name': 'Joao Pedro', 'email': 'jp@mail.com'}, {'id': 3, 'name': 'Gustvao', 'email': 'gustavo@mail.com'}, {'id': 4, 'name': 'Eliza', 'email': 'eliza@mail.com'}]
    assert response.json() == [{'id': 1, 'name': 'Kassio', 'email': 'kassio@mail.com'}, {'id': 2, 'name': 'Joao Pedro', 'email': 'jp@mail.com'}]

def test_register_client():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    new_client_expected = new_client.copy()
    new_client_expected['id'] = 1

    response = client.post('/client/register', json=new_client)
    assert response.status_code == 201
    assert response.json() == new_client_expected
    