import pytest
import warnings
import os

from fastapi.testclient import TestClient

from fastapi_app import app, get_db
from database.test_session import engine, override_get_db
from database.session import Base

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
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
        }
    )
    client.post("/stock", json={
            "store_id": 1,
            "product_id": 2,
            "price": 800,
            "is_available": True,
            "category": "Tênis"
        }
    )
    client.post("/stock", json={
            "store_id": 2,
            "product_id": 3,
            "price": 800,
            "is_available": True,
            "category": "Tênis"
        }
    )
    client.post("/stock", json={
            "store_id": 2,
            "product_id": 4,
            "price": 600,
            "is_available": True,
            "category": "Tênis"
        }
    )

    yield
    Base.metadata.drop_all(bind=engine)

    # Close the connection
    engine.dispose()

    TEST_DB_PATH = "./test.db"

    # Delete the test database
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)


# ------------ API POST ------------

def test_create_stock_success(setup_database):
    response = client.post(
        "stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": 300,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 201
    assert response.json()["data"] == {
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
    response = client.post("stock", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_stock_wrong_key(setup_database):
    response = client.post("stock", json={"location": "São Paulo"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_stock_wrong_type_store_id(setup_database):
    response = client.post(
        "stock",
        json={
            "store_id": "Teste",
            "product_id": 3,
            "price": 200,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

def test_create_stock_wrong_type_product_id(setup_database):
    response = client.post(
        "stock",
        json={
            "store_id": 1,
            "product_id": "Teste",
            "price": 200,
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid integer, unable to parse string as an integer"

def test_create_stock_wrong_type_price(setup_database):
    response = client.post(
        "stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": "Teste",
            "is_available": True,
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid number, unable to parse string as a number"

def test_create_stock_wrong_type_is_available(setup_database):
    response = client.post(
        "stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": 200,
            "is_available": "Teste",
            "category": "Tênis",
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid boolean, unable to interpret input"

def test_create_stock_wrong_type_category(setup_database):
    response = client.post(
        "stock",
        json={
            "store_id": 1,
            "product_id": 3,
            "price": 200,
            "is_available": True,
            "category": True,
        },
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

# ------------ API GET ------------

def test_get_stock_empty(setup_database):
    response = client.get("stocks", params={})
    assert response.status_code == 200
    assert response.json()["message"] == "Stocks fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "store_id": 1,
            "product_id": 1,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Max",
            "store_name": "Nike",
        },
        {
            "id": 2,
            "store_id": 1,
            "product_id": 2,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Force",
            "store_name": "Nike",
        },
        {
            "id": 3,
            "store_id": 2,
            "product_id": 3,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Adidas",
        },
        {
            "id": 4,
            "store_id": 2,
            "product_id": 4,
            "price": 600.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Mid",
            "store_name": "Adidas",
        },
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Nike",
        },
    ]

def test_get_stock_by_product_name(setup_database):
    response = client.get("stocks", params={"product_name": "Air"})
    assert response.status_code == 200
    assert response.json()["message"] == "Stocks fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "store_id": 1,
            "product_id": 1,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Max",
            "store_name": "Nike",
        },
        {
            "id": 2,
            "store_id": 1,
            "product_id": 2,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Force",
            "store_name": "Nike",
        }
    ]

def test_get_stock_by_max_price(setup_database):
    response = client.get("stocks", params={"max_price": 600})
    assert response.status_code == 200
    assert response.json()["message"] == "Stocks fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "store_id": 1,
            "product_id": 1,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Max",
            "store_name": "Nike",
        },
        {
            "id": 4,
            "store_id": 2,
            "product_id": 4,
            "price": 600.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Mid",
            "store_name": "Adidas",
        },
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Nike",
        },
    ]

def test_get_stock_by_is_available(setup_database):
    response = client.get("stocks", params={"is_available": True})
    assert response.status_code == 200
    assert response.json()["message"] == "Stocks fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "store_id": 1,
            "product_id": 1,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Max",
            "store_name": "Nike",
        },
        {
            "id": 2,
            "store_id": 1,
            "product_id": 2,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Force",
            "store_name": "Nike",
        },
        {
            "id": 3,
            "store_id": 2,
            "product_id": 3,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Adidas",
        },
        {
            "id": 4,
            "store_id": 2,
            "product_id": 4,
            "price": 600.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Mid",
            "store_name": "Adidas",
        },
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Nike",
        },
    ]

def test_get_stock_by_category(setup_database):
    response = client.get("stocks", params={"category": "Tên"})
    assert response.status_code == 200
    assert response.json()["message"] == "Stocks fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "store_id": 1,
            "product_id": 1,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Max",
            "store_name": "Nike",
        },
        {
            "id": 2,
            "store_id": 1,
            "product_id": 2,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Air Force",
            "store_name": "Nike",
        },
        {
            "id": 3,
            "store_id": 2,
            "product_id": 3,
            "price": 800.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Adidas",
        },
        {
            "id": 4,
            "store_id": 2,
            "product_id": 4,
            "price": 600.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Mid",
            "store_name": "Adidas",
        },
        {
            "id": 5,
            "store_id": 1,
            "product_id": 3,
            "price": 300.0,
            "is_available": True,
            "category": "Tênis",
            "product_name": "Forum Low",
            "store_name": "Nike",
        },
    ]

def test_get_stock_not_in_database(setup_database):
    response = client.get("stocks", params={"product_name": "AllStar"})
    assert response.status_code == 404
    assert response.json()["detail"] == "No matching stocks found"


# ------------ API DELETE ------------

def test_delete_stock_success(setup_database):
    response = client.delete("stock/5")
    assert response.status_code == 200
    assert response.json()["message"] == "Stock deleted successfully"
    assert response.json()["data"]["stock_id"] == 5

def test_delete_stock_not_in_database(setup_database):
    response = client.delete("stock/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Stock not found"


# ------------ API UPDATE ------------

def test_update_stock_success(setup_database):
    response = client.put("stock/1", json={"price": 1000, "is_available": False, "category": "Sneaker"})
    assert response.status_code == 200
    assert response.json()["message"] == "Stock updated successfully"
    assert response.json()["data"] == {
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
    response = client.put("stock/1", json={"price": None})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid number"

def test_update_stock_wrong_type_is_available(setup_database):
    response = client.put("stock/1", json={"is_available": None})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid boolean"

def test_update_stock_wrong_type_is_category(setup_database):
    response = client.put("stock/1", json={"category": None})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_update_stock_invalid_id(setup_database):
    response = client.put("stock/10", json={"price": 1000})
    assert response.status_code == 404
    assert response.json()["detail"] == "Stock not found"

def test_update_stock_missing_data(setup_database):
    response = client.put("stock/1", json={})
    assert response.status_code == 404
    assert response.json()["detail"] == "Nothing to update"

def test_update_stock_missing_id(setup_database):
    response = client.put("stock/", json={"price": 1000})
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"
