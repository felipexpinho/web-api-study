# web-api-study
A simple project to create APIs that access a sql database with Flask and FastAPI

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