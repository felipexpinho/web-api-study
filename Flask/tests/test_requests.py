import requests

def create_store(store_name):
    url = "http://localhost:8000/store"

    # Data for the new store
    store_data = {
        "name": store_name,
    }

    # Send the POST request
    response = requests.post(url, json=store_data)

    # Check the response status
    if response.status_code == 201:
        print("Store created successfully.")
        print("Response:", response.json())
    else:
        print(f"Failed to create store. Status code: {response.status_code}")
        print("Response:", response.json())

def create_product(product_name):
    url = "http://localhost:8000/product"

    # Data for the new product
    product_data = {
        "name": product_name,
    }

    # Send the POST request
    response = requests.post(url, json=product_data)

    # Check the response status
    if response.status_code == 201:
        print("Product created successfully.")
        print("Response:", response.json())
    else:
        print(f"Failed to create store. Status code: {response.status_code}")
        print("Response:", response.json())

def create_stock(store_id, product_id, price, is_available, category):
    url = "http://localhost:8000/stock"

    # Data for the new stock
    stock_data = {
        "store_id": store_id,  # The ID of the store where the stock will be added
        "product_id": product_id,  # The ID of the product
        "price": price,  # Price of the stock
        "is_available": is_available,  # Availability status of the product
        "category": category  # Category of the product
    }

    # Send the POST request
    response = requests.post(url, json=stock_data)

    # Check the response status
    if response.status_code == 201:
        print("Stock created successfully.")
        print("Response:", response.json())
    else:
        print(f"Failed to create stock. Status code: {response.status_code}")
        print("Response:", response.json())


def get_store(id = None, name = None):
    url = "http://127.0.0.1:8000/stores"

    params = {}

    if id:
        params["id"] = id
    if name:
        params["name"] = name

    # Sending the GET request to the FastAPI server
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        store_data = response.json()  # Parse the JSON response
        print(store_data)
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_product(id = None, name = None):
    url = "http://127.0.0.1:8000/products"

    params = {}

    if id:
        params["id"] = id
    if name:
        params["name"] = name

    # Sending the GET request to the FastAPI server
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        store_data = response.json()  # Parse the JSON response
        print(store_data)
    else:
        print(f"Error: {response.status_code}, {response.text}")

def get_stocks(product_name=None, store_name=None, max_price=None, is_available=None, category=None):
    url = "http://127.0.0.1:8000/stocks"
    params = {}

    if product_name:
        params["product_name"] = product_name
    if store_name:
        params["store_name"] = store_name
    if max_price:
        params["max_price"] = max_price
    if is_available is not None:
        params["is_available"] = is_available
    if category:
        params["category"] = category

    # Sending the GET request to the FastAPI server
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        stock_data = response.json()  # Parse the JSON response
        print(stock_data)
    else:
        print(f"Error: {response.status_code}, {response.text}")


def delete_store(store_id: int):
    url = f"http://127.0.0.1:8000/store/{store_id}"

    # Sending DELETE request to the FastAPI server
    response = requests.delete(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Store {store_id} deleted successfully.")
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")


def delete_product(product_id: int):
    url = f"http://127.0.0.1:8000/product/{product_id}"

    # Sending DELETE request to the FastAPI server
    response = requests.delete(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Product {product_id} deleted successfully.")
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")


def delete_stock(stock_id: int):
    url = f"http://127.0.0.1:8000/stock/{stock_id}"

    # Sending DELETE request to the FastAPI server
    response = requests.delete(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Stock {stock_id} deleted successfully.")
        print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")


def update_store(store_id: int, name: str):
    url = f"http://127.0.0.1:8000/store/{store_id}"

    data = {
        "name": name
    }

    # Sending PUT request to update the store
    response = requests.put(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Store {store_id} updated successfully.")
        print(response.json())  # Print the response data if available
    else:
        print(f"Error: {response.status_code}, {response.text}")


def update_product(product_id: int, name: str):
    url = f"http://127.0.0.1:8000/product/{product_id}"

    data = {
        "name": name
    }

    # Sending PUT request to update the product
    response = requests.put(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Product {product_id} updated successfully.")
        print(response.json())  # Print the response data if available
    else:
        print(f"Error: {response.status_code}, {response.text}")


def update_stock(stock_id: int, price: float = None, is_available: bool = None, category: str = None):
    url = f"http://127.0.0.1:8000/stock/{stock_id}"

    data = {}
    if price is not None:
        data["price"] = price
    if is_available is not None:
        data["is_available"] = is_available
    if category is not None:
        data["category"] = category

    # Sending PUT request to update the stock
    response = requests.put(url, json=data)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print(f"Stock {stock_id} updated successfully.")
        print(response.json())  # Print the response data if available
    else:
        print(f"Error: {response.status_code}, {response.text}")


def check_rate_limit():
    url = "http://127.0.0.1:8000/limited-requests"
    # Send a GET request to the rate-limited endpoint
    response = requests.get(url)

    return {"status_code": response.status_code, "content": response.json()}

def populate_table():
    create_store("Nike")
    create_store("Adidas")
    create_product("Air Max")
    create_product("Air Force")
    create_product("Forum Low")
    create_product("Forum Mid")
    create_stock(1, 1, 300, True, "Tênis")
    create_stock(1, 2, 800, True, "Tênis")
    create_stock(2, 3, 800, True, "Tênis")
    create_stock(2, 4, 600, True, "Tênis")


create_store(None)