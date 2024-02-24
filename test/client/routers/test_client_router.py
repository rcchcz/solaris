from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_list_clients():
    response = client.get('/client/list')
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Kassio', 'email': 'kassio@mail.com'}, {'id': 2, 'name': 'Joao Pedro', 'email': 'jp@mail.com'}, {'id': 3, 'name': 'Gustvao', 'email': 'gustavo@mail.com'}, {'id': 4, 'name': 'Eliza', 'email': 'eliza@mail.com'}]

def test_register_client():
    new_client = {
        'name': 'Magalu',
        'email': 'magalu@mail.com'
    }

    new_client_expected = new_client.copy()
    new_client_expected['id'] = 5

    response = client.post('/client/register', json=new_client)
    assert response.status_code == 201
    assert response.json() == new_client_expected
    