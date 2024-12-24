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

def test_create_product_success(setup_database):
    response = client.post("product", json={"name": "Test Product"})
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "Test Product"

def test_create_product_empty_json(setup_database):
    response = client.post("product", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_product_wrong_key(setup_database):
    response = client.post("product", json={"location": "São Paulo"})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_create_product_wrong_type(setup_database):
    response = client.post("product", json={"name": None})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"


# ------------ API GET ------------

def test_get_product_empty(setup_database):
    response = client.get("product", params={})
    assert response.status_code == 200
    assert response.json()["message"] == "Products fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "name": "Air Max",
            "stock": [
                {
                    "id": 1,
                    "store_id": 1,
                    "product_id": 1,
                    "price": 300.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Max",
                    "store_name": "Nike",
                }
            ],
        },
        {
            "id": 2,
            "name": "Air Force",
            "stock": [
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
            ],
        },
        {
            "id": 3,
            "name": "Forum Low",
            "stock": [
                {
                    "id": 3,
                    "store_id": 2,
                    "product_id": 3,
                    "price": 800.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Forum Low",
                    "store_name": "Adidas",
                }
            ],
        },
        {
            "id": 4,
            "name": "Forum Mid",
            "stock": [
                {
                    "id": 4,
                    "store_id": 2,
                    "product_id": 4,
                    "price": 600.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Forum Mid",
                    "store_name": "Adidas",
                }
            ],
        },
        {"id": 5, "name": "Test Product", "stock": []},
    ]

def test_get_product_by_id(setup_database):
    response = client.get("product", params={"id": 1})
    assert response.status_code == 200
    assert response.json()["message"] == "Products fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "name": "Air Max",
            "stock": [
                {
                    "id": 1,
                    "store_id": 1,
                    "product_id": 1,
                    "price": 300.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Max",
                    "store_name": "Nike",
                }
            ],
        }
    ]

def test_get_product_by_name(setup_database):
    response = client.get("product", params={"name": "Air"})
    assert response.status_code == 200
    assert response.json()["message"] == "Products fetched successfully"
    assert response.json()["data"] == [
        {
            "id": 1,
            "name": "Air Max",
            "stock": [
                {
                    "id": 1,
                    "store_id": 1,
                    "product_id": 1,
                    "price": 300.0,
                    "is_available": True,
                    "category": "Tênis",
                    "product_name": "Air Max",
                    "store_name": "Nike",
                }
            ],
        },
        {
            "id": 2,
            "name": "Air Force",
            "stock": [
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
            ],
        },
    ]

def test_get_product_not_in_database(setup_database):
    response = client.get("product", params={"name": "AllStar"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


# ------------ API DELETE ------------

def test_delete_product_success(setup_database):
    response = client.delete("product/5")
    assert response.status_code == 200
    assert response.json()["message"] == "Product deleted successfully"
    assert response.json()["data"]["product_id"] == 5

def test_delete_product_not_in_database(setup_database):
    response = client.delete("product/10")
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"


# ------------ API UPDATE ------------

def test_update_product_success(setup_database):
    response = client.put("product/1", json={"name": "Air Max Branco"})
    assert response.status_code == 200
    assert response.json()["message"] == "Product updated successfully"
    assert response.json()["data"] == {
        "id": 1,
        "name": "Air Max Branco",
    }

def test_update_product_wrong_type(setup_database):
    response = client.put("product/1", json={"name": None})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Input should be a valid string"

def test_update_product_invalid_id(setup_database):
    response = client.put("product/10", json={"name": "Test"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"

def test_update_product_missing_data(setup_database):
    response = client.put("product/1", json={})
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Field required"

def test_update_product_missing_id(setup_database):
    response = client.put("product/", json={"name": "Test"})
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"
