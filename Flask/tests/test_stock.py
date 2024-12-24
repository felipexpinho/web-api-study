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

def test_create_stock_success(setup_database):
    client = setup_database

    # Test creating a new stock
    response = client.post(
        "/stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": 300,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 201
    assert response.get_json()["data"] == {
        "id": 5,
        "store_id": 1,
        "product_id": 3,
        "price": 300.0,
        "is_available": True,
        "category": "Tênis",
        "store": "Nike",
        "product_name": "Forum Low",
    }

def test_create_stock_empty_json(setup_database):
    client = setup_database

    response = client.post("/stock", json={})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Field required"

def test_create_stock_wrong_key(setup_database):
    client = setup_database

    response = client.post("/store", json={"location": "São Paulo"})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Field required"

def test_create_stock_wrong_type_store_id(setup_database):
    client = setup_database

    response = client.post(
        "/stock",
        json={
            "store_id": None,
            "product_id": 3,
            "price": 200,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_create_stock_wrong_type_product_id(setup_database):
    client = setup_database

    response = client.post(
        "/stock",
        json={
            "store_id": 1,
            "product_id": None,
            "price": 200,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_create_stock_wrong_type_price(setup_database):
    client = setup_database

    response = client.post(
        "/stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": None,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_create_stock_wrong_type_is_available(setup_database):
    client = setup_database

    response = client.post(
        "/stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": 200,
            "is_available": None,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_create_stock_wrong_type_category(setup_database):
    client = setup_database

    response = client.post(
        "/stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": 200,
            "is_available": True,
            "category": None,
        },
    )
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"


# ------------ API GET ------------

def test_get_stock_empty(setup_database):
    client = setup_database

    response = client.get("/stock", query_string={})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stocks fetched successfully"
    assert response.get_json()["data"] == [
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
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store": "Nike",
        },
    ]

def test_get_stock_by_product_name(setup_database):
    client = setup_database

    response = client.get("/stock", query_string={"product_name": "Air"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stocks fetched successfully"
    assert response.get_json()["data"] == [
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
        }
    ]

def test_get_stock_by_max_price(setup_database):
    client = setup_database

    response = client.get("/stock", query_string={"max_price": 600})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stocks fetched successfully"
    assert response.get_json()["data"] == [
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
            "id": 4,
            "store_id": 2,
            "product_id": 4,
            "price": 600.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Mid",
            "store": "Adidas",
        },
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store": "Nike",
        },
    ]

def test_get_stock_by_is_available(setup_database):
    client = setup_database

    response = client.get("/stock", query_string={"is_available": True})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stocks fetched successfully"
    assert response.get_json()["data"] == [
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
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store": "Nike",
        },
    ]

def test_get_stock_by_category(setup_database):
    client = setup_database

    response = client.get("/stock", query_string={"category": "Tên"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stocks fetched successfully"
    assert response.get_json()["data"] == [
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
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store": "Nike",
        },
    ]

def test_get_store_not_in_database(setup_database):
    client = setup_database

    response = client.get("/stock", query_string={"product_name": "AllStar"})
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Stock not found"


# ------------ API DELETE ------------

def test_delete_stock_success(setup_database):
    client = setup_database

    response = client.delete("/stock/5")
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stock deleted successfully"
    assert response.get_json()["data"]["stock_id"] == 5

def test_delete_stock_not_in_database(setup_database):
    client = setup_database

    response = client.delete("/stock/10")
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Stock not found"


# ------------ API UPDATE ------------

def test_update_stock_success(setup_database):
    client = setup_database

    response = client.put("/stock/1", json={"price": 1000, "is_available": False, "category": "Sneaker"})
    assert response.status_code == 200
    assert response.get_json()["message"] == "Stock updated successfully"
    assert response.get_json()["data"] == {
        "id": 1,
        "store_id": 1,
        "product_id": 1,
        "price": 1000.0,
        "is_available": False,
        "category": "Sneaker",
        "product_name": "Air Max",
        "store": "Nike",
    }

def test_update_stock_wrong_type_price(setup_database):
    client = setup_database

    response = client.put("/stock/1", json={"price": None})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_update_stock_wrong_type_is_available(setup_database):
    client = setup_database

    response = client.put("/stock/1", json={"is_available": None})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_update_stock_wrong_type_is_category(setup_database):
    client = setup_database

    response = client.put("/stock/1", json={"category": None})
    assert response.status_code == 422
    assert response.get_json()["detail"][0]["msg"] == "Invalid type"

def test_update_stock_invalid_id(setup_database):
    client = setup_database

    response = client.put("/stock/10", json={"price": 1000})
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Stock not found"

def test_update_stock_missing_data(setup_database):
    client = setup_database

    response = client.put("/stock/1", json={})
    assert response.status_code == 404
    assert response.get_json()["detail"][0]["msg"] == "Nothing to update"

def test_update_stock_missing_id(setup_database):
    client = setup_database

    response = client.put("/stock/", json={"price": 1000})
    assert response.status_code == 405