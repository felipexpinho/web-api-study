import numbers

from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Dict, Any

from models.store import Store
from models.stock import Stock
from models.product import Product


# ------------ API POST ------------

def create_stock_service(stock_data: dict, db: Session) -> dict:
    """
    Service to create a new stock in the database.

    Args:
        stock_data (dict): A dictionary containing the details of the stock to be created.
            Required key: store_id (int): The id of the store related to the stock.
            Required key: product_id (int): The id of the product related to the stock.
            Required key: price_id (float): The price of the product in that store.
            Required key: is_available (bool): True if the product is in stock/False if not.
            Required key: category (str): The category of the product in that store.
        db (Session): SQLAlchemy session object.

    Returns:
        dict: A dictionary containing the details of the created stock.
            id (int): The unique ID of the created stock.
            store_id (str): The id of the id of the store related to the stock.
            product_id (int): The id of the product related to the stock.
            price_id (float): The price of the product in that store.
            is_available (bool): True if the product is in stock/False if not.
            category (str): The category of the product in that store.
            store (str): The name of the store related to the stock.
            product_name (str): The name of the product related to the stock.

    Raises:
        Exception: If any error occurs during the database transaction, it is rolled back, and the exception is re-raised.
        KeyError: If required fields are missing in the update data.
        TypeError: If the field types are incorrect.
    """
    try:
        required_keys_list = ["store_id", "product_id", "price", "is_available", "category"]
        if not all(key in stock_data for key in required_keys_list):
            missing_keys_list = [key for key in required_keys_list if key not in stock_data]
            raise KeyError(f"Field(s) {', '.join(f'\'{key}\'' for key in missing_keys_list)} not found")

        type_error_list = []
        if not isinstance(stock_data["store_id"], int):
            type_error_list.append(
                {
                    "type": "int_type",
                    "loc": ["body", "store_id"],
                    "msg": "Input should be a valid integer",
                    "input": stock_data["store_id"],
                }
            )
        if not isinstance(stock_data["product_id"], int):
            type_error_list.append(
                {
                    "type": "int_type",
                    "loc": ["body", "product_id"],
                    "msg": "Input should be a valid integer",
                    "input": stock_data["product_id"],
                }
            )
        if not isinstance(stock_data["price"], numbers.Number):
            type_error_list.append(
                {
                    "type": "float_type",
                    "loc": ["body", "price"],
                    "msg": "Input should be a valid number",
                    "input": stock_data["price"],
                }
            )
        if not isinstance(stock_data["is_available"], bool):
            type_error_list.append(
                {
                    "type": "bool_type",
                    "loc": ["body", "is_available"],
                    "msg": "Input should be a valid boolean",
                    "input": stock_data["is_available"],
                }
            )
        if not isinstance(stock_data["category"], str):
            type_error_list.append(
                {
                    "type": "string_type",
                    "loc": ["body", "category"],
                    "msg": "Input should be a valid string",
                    "input": stock_data["category"],
                }
            )

        if type_error_list:
            raise TypeError(type_error_list)

        # Create and save new store
        new_stock = Stock(
            store_id=stock_data["store_id"],
            product_id=stock_data["product_id"],
            price=stock_data["price"],
            is_available=stock_data["is_available"],
            category=stock_data["category"]
        )
        db.add(new_stock)
        db.commit()
        db.refresh(new_stock)

        return new_stock._asdict()
    except Exception as e:
        db.rollback()
        raise e


# ------------ API GET ------------

def get_stocks_service(
    db: Session,
    product_name: Optional[str],
    store_name: Optional[str],
    max_price: Optional[float],
    is_available: Optional[bool],
    category: Optional[str],
) -> List[Dict[str, Any]]:
    """
    Service function to fetch stocks based on optional filters.

    Args:
        db (Session): SQLAlchemy session object.
        product_name (Optional[str]): Name of the product to filter by.
        store_name (Optional[str]): Name of the store to filter by.
        max_price (Optional[float]): Max price to filter by.
        is_available (Optional[bool]): Availability to filter by. True if the product is in stock/False if not.
        category (Optional[str]): Category to filter by.

    Returns:
        List[Dict[str, Any]]: List of stocks with their details.

    Raises:
        ValueError: If no stocks are found.
    """
    query = db.query(Stock).options(joinedload(Stock.product), joinedload(Stock.store))

    # Filter by args provided
    if product_name:
        query = query.filter(Stock.product.has(Product.name.ilike(f"%{product_name}%")))
    if store_name:
        query = query.filter(Stock.store.has(Store.name.ilike(f"%{store_name}%")))
    if max_price is not None:
        query = query.filter(Stock.price <= max_price)
    if is_available is not None:
        query = query.filter(Stock.is_available == is_available)
    if category:
        query = query.filter(Stock.category.ilike(f"%{category}%"))

    stocks = query.all()

    if not stocks:
        raise ValueError("No matching stocks found")

    return [stock._asdict() for stock in stocks]


# ------------ API DELETE ------------

def delete_stock_service(stock_id: int, db: Session) -> dict:
    """
    Service to delete a stock by ID from the database.

    Args:
        stock_id (int): The ID of the stock to delete.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the ID of the deleted store.

    Raises:
        ValueError: If the store with the given ID does not exist.
    """
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    
    if not stock:
        raise ValueError("Stock not found")
    
    # Delete the stock
    db.delete(stock)
    db.commit()
    
    # Return the deleted stock ID as confirmation
    return {"stock_id": stock_id}


# ------------ API UPDATE ------------

def update_stock_service(stock_id: int, stock_update: dict, db: Session) -> dict:
    """
    Service to update a stock by ID.

    Args:
        stock_id (int): The ID of the stock to update.
        stock_update (dict): A dictionary containing the details of the stock to be updated.
            Optional key: price_id (float): The price of the product in that store.
            Optional key: is_available (bool): True if the product is in stock/False if not.
            Optional key: category (str): The category of the product in that store.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary with the updated store details.
        
    Raises:
        ValueError: If the store with the given ID is not found.
        KeyError: If there's no key to update.
        TypeError: If the field types are incorrect.
    """
    if not stock_update:
        raise KeyError(f"No keys in the dict")

    type_error_list = []
    if "price" in stock_update and not isinstance(
        stock_update["price"], numbers.Number
    ):
        type_error_list.append(
            {
                "type": "float_type",
                "loc": ["body", "price"],
                "msg": "Input should be a valid number",
                "input": stock_update["price"],
            }
        )
    if "is_available" in stock_update and not isinstance(
        stock_update["is_available"], bool
    ):
        type_error_list.append(
            {
                "type": "bool_type",
                "loc": ["body", "is_available"],
                "msg": "Input should be a valid boolean",
                "input": stock_update["is_available"],
            }
        )
    if "category" in stock_update and not isinstance(stock_update["category"], str):
        type_error_list.append(
            {
                "type": "string_type",
                "loc": ["body", "category"],
                "msg": "Input should be a valid string",
                "input": stock_update["category"],
            }
        )

    if type_error_list:
        raise TypeError(type_error_list)

    stock = db.query(Stock).filter(Stock.id == stock_id).first()

    if not stock:
        raise ValueError("Stock not found")

    # Update the stock fields
    if "price" in stock_update:
        stock.price = stock_update["price"]
    if "is_available" in stock_update:
        stock.is_available = stock_update["is_available"]
    if "category" in stock_update:
        stock.category = stock_update["category"]

    db.commit()
    db.refresh(stock)

    # Return the updated stock data
    return stock._asdict()
