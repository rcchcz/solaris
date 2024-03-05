from fastapi import HTTPException
from fastapi.testclient import TestClient
import pytest
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

@pytest.fixture(autouse=True)
def setup_database():
    # new database for each test
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_successful_product_registration():
    new_product = { "price": 5000,
                    "image": "img001.jpg",
                    "brand": "Brand 1",
                    "title": "Title 1",
                    "review_score": 4.75
                  }
    
    expected_product = {  "id": 1,
                           "price": 5000,
                           "image": "img001.jpg",
                           "brand": "Brand 1",
                           "title": "Title 1",
                           "review_score": 4.75
                        }
    
    product_response = client.post('/product/register', json=new_product)
    assert product_response.status_code == 201
    assert product_response.json() == expected_product

def test_successful_product_delete():
    new_product = { "price": 5000,
                    "image": "img001.jpg",
                    "brand": "Brand 1",
                    "title": "Title 1",
                    "review_score": 4.75
                  }
    
    product_response = client.post('/product/register', json=new_product)
    assert product_response.status_code == 201

    product_response = client.delete('/product/delete/1')
    assert product_response.status_code == 204

def test_notfound_product_delete():
    try:
        client.delete('/product/delete/1')
    except NotFound as e:
        assert e.status_code == 404
        assert e.detail == 'Product not found.'

def test_successful_product_by_id():
    new_product = { "price": 5000,
                    "image": "img001.jpg",
                    "brand": "Brand 1",
                    "title": "Title 1",
                    "review_score": 4.75
                  }
    
    expected_product = {  "id": 1,
                           "price": 5000,
                           "image": "img001.jpg",
                           "brand": "Brand 1",
                           "title": "Title 1",
                           "review_score": 4.75
                        }
    
    product_response = client.post('/product/register', json=new_product)
    assert product_response.status_code == 201

    product_response = client.get('/product/1')
    assert product_response.status_code == 200
    assert product_response.json() == expected_product

def test_notfound_product_by_id():
    try:
        client.get('/product/1')
    except NotFound as e:
        assert e.status_code == 404
        assert e.detail == 'Product not found.'

def test_successful_product_list():
    new_product1 = { "price": 5000,
                    "image": "img001.jpg",
                    "brand": "Brand 1",
                    "title": "Title 1",
                    "review_score": 4.75
                  }
    
    new_product2 = { "price": 10000,
                    "image": "img002.jpg",
                    "brand": "Brand 2",
                    "title": "Title 2",
                    "review_score": 5
                  }
    
    expected = [{  "id": 1,
                    "price": 5000,
                    "image": "img001.jpg",
                    "brand": "Brand 1",
                    "title": "Title 1",
                    "review_score": 4.75
                },
                {   "id": 2,
                    "price": 10000,
                    "image": "img002.jpg",
                    "brand": "Brand 2",
                    "title": "Title 2",
                    "review_score": 5
                }]
    
    product_response = client.post('/product/register', json=new_product1)
    assert product_response.status_code == 201

    product_response = client.post('/product/register', json=new_product2)
    assert product_response.status_code == 201

    product_response = client.get('/product/list')
    assert product_response.status_code == 200
    assert product_response.json() == expected

def test_empty_product_list():
    product_response = client.get('/product/list')
    
    assert product_response.status_code == 200
    assert product_response.json() == []

