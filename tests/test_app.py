import pytest
from app import app
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client

def test_index_page(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Welcome to CRM System' in rv.data

def test_customers_page(client):
    rv = client.get('/customers')
    assert rv.status_code == 200
    assert b'Customers' in rv.data

def test_add_customer(client):
    rv = client.get('/add_customer')
    assert rv.status_code == 200
    assert b'Add New Customer' in rv.data

def test_api_customers(client):
    rv = client.get('/api/customers')
    assert rv.status_code == 200
    assert rv.is_json 