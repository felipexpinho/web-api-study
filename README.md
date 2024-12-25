# web-api-study
A simple project to create APIs that access a sql database with Flask and FastAPI

# Frameworks and Libraries

**Flask**: Framework to create the API.

**FastAPI**: Framework to create the API.

**SlowAPI**: Lib for limiting the requests per hour in FastAPI.

**Flask_Limiter**: Lib for limiting the requests per hour in Flask.

**Pydantic**: Lib to create the schema for validation of payload objects.

**Pytest**: Lib to create the Unit Tests.

**Requests**: Lib to create requests to help me test and validade the APIs.

**SQLAlchemy**: Lib to manage the SQL Database.

**Uvicorn**: Lib to run the FastAPI API.

**Typing**: Lib for typing functions to improve readability.


# Database
## Product
| Field | Type | Description |
|-------|------|-------------|
| id    | integer | Unique identifier for the product. |
| name  | string | Name of the product. |
| stock | list[Stock] | List of all the stocks that connect this Product to Stores. |

## Store
| Field | Type | Description |
|-------|------|-------------|
| id    | integer | Unique identifier for the store. |
| name  | string | Name of the store. |
| stock | list[Stock] | List of all the stocks that connect this Store to Products. |

## Stock
| Field | Type | Description |
|-------|------|-------------|
| id | integer | Unique identifier for the stock. |
| store_id | integer | Unique identifier for the store related to this stock. |
| product_id | integer | Unique identifier for the product related to this stock. |
| price | float | Price of the product in a specific store. |
| is_available | boolean | True if it's the product is available in the store; False if it's not. |
| category | string | Category of the product in a specific store. |
| store | Store | The Store related to this Stock. |
| product | Product | The Product related to this Stock. |


# Endpoints
## Stock
| Endpoint | Expected Payload | Description |
|------------|------------|------------|
| POST /Stock | {<br>&nbsp;&nbsp;&nbsp;&nbsp;store_id: int,<br>&nbsp;&nbsp;&nbsp;&nbsp;product_id: int,<br>&nbsp;&nbsp;&nbsp;&nbsp;price: float,<br>&nbsp;&nbsp;&nbsp;&nbsp;is_available: bool,<br>&nbsp;&nbsp;&nbsp;&nbsp;category: str<br>} | Create a new stock in the database with the given content of the payload. |
| GET /Stock | {<br>&nbsp;&nbsp;&nbsp;&nbsp;store_name: Optional[str],<br>&nbsp;&nbsp;&nbsp;&nbsp;product_name: Optional[str],<br>&nbsp;&nbsp;&nbsp;&nbsp;max_price: Optional[float],<br>&nbsp;&nbsp;&nbsp;&nbsp;is_available: Optional[bool],<br>&nbsp;&nbsp;&nbsp;&nbsp;category: Optional[str]<br>} | Get all the stocks given the payload. If no keys are given, it will fetch all stocks from the database. |
| DELETE /Stock/<stock_id> |  | Delete the stock given the stock_id. |
| PUT /Stock/<stock_id> | {<br>&nbsp;&nbsp;&nbsp;&nbsp;price: Optional[float],<br>&nbsp;&nbsp;&nbsp;&nbsp;is_available: Optional[bool],<br>&nbsp;&nbsp;&nbsp;&nbsp;category: Optional[str]<br>} | Update the stock with the stock_id with the content of the payload. |

## Store
| Endpoint | Expected Payload | Description |
|------------|------------|------------|
| POST /Store | {<br>&nbsp;&nbsp;&nbsp;&nbsp;name: str<br>} | Create a new store in the database with the given name of the payload. |
| GET /Store | {<br>&nbsp;&nbsp;&nbsp;&nbsp;id: Optional[int],<br>&nbsp;&nbsp;&nbsp;&nbsp;name: Optional[str]<br>} | Get all the stores given the payload. If no keys are given, it will fetch all stores from the database. |
| DELETE /Store/<store_id> |  | Delete the store given the store_id. |
| PUT /Store/<store_id> | {<br>&nbsp;&nbsp;&nbsp;&nbsp;name: str<br>} | Update the store with the store_id with the content of the payload. |

## Product
| Endpoint | Expected Payload | Description |
|------------|------------|------------|
| POST /Product | {<br>&nbsp;&nbsp;&nbsp;&nbsp;name: str<br>} | Create a new product in the database with the given name of the payload. |
| GET /Product | {<br>&nbsp;&nbsp;&nbsp;&nbsp;id: Optional[int],<br>&nbsp;&nbsp;&nbsp;&nbsp;name: Optional[str]<br>} | Get all the products given the payload. If no keys are given, it will fetch all products from the database. |
| DELETE /Product/<product_id> |  | Delete the product given the product_id. |
| PUT /Product/<product_id> | {<br>&nbsp;&nbsp;&nbsp;&nbsp;name: str<br>} | Update the product with the product_id with the content of the payload. |