import pytest
import os
from utils.create_app import create_app
from database.test_session import Base, engine
from database.session import Base

@pytest.fixture(scope="module")
def setup_database():
    # Setup the Flask app and create database tables
    app = create_app(config_name="testing")
    with app.app_context():
        Base.metadata.create_all(bind=engine)
        
        # Get the test client for making requests
        client = app.test_client()

        # Insert test data into the database using client requests
        client.post("/store", json={"name": "Nike"})
        client.post("/store", json={"name": "Adidas"})
        client.post("/product", json={"name": "Air Max"})
        client.post("/product", json={"name": "Air Force"})
        client.post("/product", json={"name": "Forum Low"})
        client.post("/product", json={"name": "Forum Mid"})
        client.post("/stock", json={
            "store_id": 1,
            "product_id": 1,
            "price": 300,
            "is_available": True,
            "category": "Tênis"
        })
        client.post("/stock", json={
            "store_id": 1,
            "product_id": 2,
            "price": 800,
            "is_available": True,
            "category": "Tênis"
        })
        client.post("/stock", json={
            "store_id": 2,
            "product_id": 3,
            "price": 800,
            "is_available": True,
            "category": "Tênis"
        })
        client.post("/stock", json={
            "store_id": 2,
            "product_id": 4,
            "price": 600,
            "is_available": True,
            "category": "Tênis"
        })

        yield client  # Yield the client so it can be used in tests

        # Cleanup after tests: Drop tables and remove test database
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

        TEST_DB_PATH = "./test.db"
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

# ------------ API POST ------------

def test_create_store_success(setup_database):
    client = setup_database

    # Test creating a new store
    response = client.post("/store", json={"name": "Test Store"})
    assert response.status_code == 201
    assert response.get_json()["data"]["name"] == "Test Store"

def test_create_store_empty_json(setup_database):
    client = setup_database

    response = client.post("/store", json={})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Field required"

def test_create_store_wrong_key(setup_database):
    client = setup_database

    response = client.post("/store", json={"location": "São Paulo"})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Field required"

def test_create_store_wrong_type(setup_database):
    client = setup_database

    response = client.post("/store", json={"name": None})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["error"] == "Input should be a valid string"


# ------------ API GET ------------

def test_get_store_empty(setup_database):
    client = setup_database

    response = client.get("/store", query_string={})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stores fetched successfully"
    assert response.get_json()["data"] == [
        {
            "id": 1,
            "name": "Nike",
            "stock": [
                {
                    "id": 1,
                    "store_id": 1,
                    "product_id": 1,
                    "price": 300.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Max",
                    "store": "Nike",
                },
                {
                    "id": 2,
                    "store_id": 1,
                    "product_id": 2,
                    "price": 800.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Force",
                    "store": "Nike",
                },
            ],
        },
        {
            "id": 2,
            "name": "Adidas",
            "stock": [
                {
                    "id": 3,
                    "store_id": 2,
                    "product_id": 3,
                    "price": 800.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Forum Low",
                    "store": "Adidas",
                },
                {
                    "id": 4,
                    "store_id": 2,
                    "product_id": 4,
                    "price": 600.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Forum Mid",
                    "store": "Adidas",
                },
            ],
        },
        {"id": 3, "name": "Test Store", "stock": []},
    ]

def test_get_store_by_id(setup_database):
    client = setup_database

    response = client.get("/store", query_string={"id": 1})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stores fetched successfully"
    assert response.get_json()["data"] == [
        {
            "id": 1,
            "name": "Nike",
            "stock": [
                {
                    "id": 1,
                    "store_id": 1,
                    "product_id": 1,
                    "price": 300.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Max",
                    "store": "Nike",
                },
                {
                    "id": 2,
                    "store_id": 1,
                    "product_id": 2,
                    "price": 800.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Force",
                    "store": "Nike",
                },
            ],
        }
    ]

def test_get_store_by_name(setup_database):
    client = setup_database

    response = client.get("/store", query_string={"name": "Nik"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stores fetched successfully"
    assert response.get_json()["data"] == [
        {
            "id": 1,
            "name": "Nike",
            "stock": [
                {
                    "id": 1,
                    "store_id": 1,
                    "product_id": 1,
                    "price": 300.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Max",
                    "store": "Nike",
                },
                {
                    "id": 2,
                    "store_id": 1,
                    "product_id": 2,
                    "price": 800.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Force",
                    "store": "Nike",
                },
            ],
        }
    ]

def test_get_store_not_in_database(setup_database):
    client = setup_database

    response = client.get("/store", query_string={"name": "Kabum"})
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Store not found"


# ------------ API DELETE ------------

def test_delete_store_success(setup_database):
    client = setup_database

    response = client.delete("/store/3")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Store deleted successfully"
    assert response.get_json()["data"]["store_id"] == 3

def test_delete_store_not_in_database(setup_database):
    client = setup_database

    response = client.delete("/store/4")
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Store not found"


# ------------ API UPDATE ------------

def test_update_store_success(setup_database):
    client = setup_database

    response = client.put("/store/1", json={"name": "Nike 2.0"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Store updated successfully"
    assert response.get_json()["data"] == {"id": 1, "name": "Nike 2.0"}

def test_update_store_wrong_type(setup_database):
    client = setup_database

    response = client.put("/store/1", json={"name": None})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["error"] == "Input should be a valid string"

def test_update_store_invalid_id(setup_database):
    client = setup_database

    response = client.put("/store/10", json={"name": "Test"})
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Store not found"

def test_update_store_missing_data(setup_database):
    client = setup_database

    response = client.put("/store/1", json={})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Field required"

def test_update_store_missing_id(setup_database):
    client = setup_database

    response = client.put("/store/", json={"name": "Test"})
    assert response.status_code == 405