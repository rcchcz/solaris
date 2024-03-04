from fastapi import HTTPException
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from main import app
from shared.database import Base
from shared.dependencies import get_db
from shared.exceptions import NotFound

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

def test_successful_client_registration():
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

def test_duplicate_email_client_registration():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    response = client.post('/client/register', json=new_client)
    assert response.status_code == 201

    try:
        response = client.post('/client/register', json=new_client)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.detail == {'detail': 'Email already registered.'}

def test_successful_client_by_id():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    response = client.post('/client/register', json=new_client)
    assert response.status_code == 201

    client_expected = new_client.copy()
    client_expected['id'] = 1
    client_expected['favorite_products'] = []

    response = client.get('/client/1')
    assert response.status_code == 200    
    assert response.json() == client_expected

def test_notfound_client_by_id():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        response = client.get('/client/1')
    except NotFound as e:
        assert e.status_code == 404    
        assert e.detail == {'detail': 'Client not found.'}

def test_successful_client_by_id_with_favorite_products():
    product = { "price": 5000,
                "image": "img001.jpg",
                "brand": "Brand 1",
                "title": "Title 1",
                "review_score": 4.75
                }
    
    product_response = client.post('/product/register', json=product)
    product_id = product_response.json()['id']

    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    response = client.post('/client/register', json=new_client)
    assert response.status_code == 201
    
    client_id = response.json()['id']
    client_details = {
        'name': 'Magalu',
        'email': 'magalu@mail.com',
        'favorite_products': [product_id]
    }

    response = client.put(f'/client/update/{client_id}', json=client_details)
    assert response.status_code == 200

    client_expected = {
        'id': client_id,
        'name': 'Magalu',
        'email': 'magalu@mail.com',
        'favorite_products': [{ "id": product_id,
                                "price": 5000,
                                "image": "img001.jpg",
                                "brand": "Brand 1",
                                "title": "Title 1",
                                "review_score": 4.75
                            }]
    }

    response = client.get(f'/client/{client_id}')
    assert response.status_code == 200    
    assert response.json() == client_expected

def test_successful_client_update():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    response_post = client.post('/client/register', json=new_client)
    assert response_post.status_code == 201

    update_client = {
        'name': 'Magalu',
        'email': 'newmagalu@mail.com',
        'favorite_products': []
    }

    update_client_expected = update_client.copy()
    update_client_expected['id'] = 1

    response_put = client.put('/client/update/1', json=update_client)

    assert response_put.status_code == 200
    assert response_put.json()['id'] == update_client_expected['id']
    assert response_put.json()['name'] == update_client_expected['name']
    assert response_put.json()['email'] == update_client_expected['email']

def test_duplicate_email_client_update():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_client1 = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    new_client2 = {
        'name': 'Luizalabs',
        'email': 'luizalabs@mail.com'
    }

    response_post1 = client.post('/client/register', json=new_client1)
    assert response_post1.status_code == 201

    response_post2 = client.post('/client/register', json=new_client2)
    assert response_post2.status_code == 201

    update_client = {
        'name': 'Magalu',
        'email': 'luizalabs@mail.com', # TESTING EMAIL ALREADY IN USE
        'favorite_products': []
    }

    client_id = response_post1.json()['id']

    try:
        client.put(f'/client/update/{client_id}', json=update_client)
    except HTTPException as e:
        assert e.status_code == 409
        assert e.detail == 'Email already in use.'

def test_successful_client_delete():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    response_post = client.post('/client/register', json=new_client)
    id_client = response_post.json()['id']

    response_delete = client.delete(f'/client/delete/{id_client}')

    assert response_delete.status_code == 204

def test_notfound_client_delete():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    try:
        client.delete('/client/delete/1')
    except NotFound as e:
        assert e.status_code == 404
        assert e.detail == 'Client not found.'

def test_list_clients():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.post('/client/register', json={'name': 'Kassio', 'email': 'kassio@mail.com', 'favorite_products': []})
    assert response.status_code == 201
    
    response = client.post('/client/register', json={'name': 'Joao Pedro', 'email': 'jp@mail.com', 'favorite_products': []})
    assert response.status_code == 201

    response = client.post('/client/register', json={'name': 'Gustavo', 'email': 'gustavo@mail.com', 'favorite_products': []})
    assert response.status_code == 201

    response = client.post('/client/register', json={'name': 'Eliza', 'email': 'eliza@mail.com', 'favorite_products': []})
    assert response.status_code == 201
    
    response = client.get('/client/list')
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Kassio', 'email': 'kassio@mail.com', 'favorite_products': []},
                               {'id': 2, 'name': 'Joao Pedro', 'email': 'jp@mail.com', 'favorite_products': []},
                               {'id': 3,'name': 'Gustavo', 'email': 'gustavo@mail.com', 'favorite_products': []},
                               {'id': 4, 'name': 'Eliza', 'email': 'eliza@mail.com', 'favorite_products': []}]

def test_empty_list_clients():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    response = client.get('/client/list')

    assert response.status_code == 200
    assert response.json() == []