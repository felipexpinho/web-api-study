from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from schemas.store import StoreCreate, StoreResponse, StoreUpdate
from schemas.stock import StockCreate, StockResponse, StockUpdate

from models.product import Product
from models.store import Store
from models.stock import Stock

# ------------ API POST ------------

def create_stock_service(stock: StockCreate, db: Session) -> dict:
    """
    Service to create a new stock in the database.

    Args:
        stock (StockCreate): The schema containing the details of the stock to be created.
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
        ValueError: If no Store or Product is found.
    """
    # Check if the store exists
    store = db.query(Store).filter(Store.id == stock.store_id).first()
    if not store:
        raise ValueError("Store not found")

    # Check if the product exists
    product = db.query(Product).filter(Product.id == stock.product_id).first()
    if not product:
        raise ValueError("Product not found")

    # Create the new stock
    new_stock = Stock(
        store_id=stock.store_id,
        product_id=stock.product_id,
        price=stock.price,
        is_available=stock.is_available,
        category=stock.category
    )

    # Add the new stock to both the product and store stock lists
    store.stock.append(new_stock)
    product.stock.append(new_stock)

    db.add(new_stock)
    db.commit()
    db.refresh(new_stock)  # Refresh to get the ID

    return new_stock._asdict()


# ------------ API GET ------------

def get_stocks_service(
    db: Session, 
    product_name: Optional[str], 
    store_name: Optional[str], 
    max_price: Optional[float], 
    is_available: Optional[bool], 
    category: Optional[str]
) -> List[StockResponse]:
    """
    Service function to fetch stocks based on optional filters.

    Args:
        db (Session): SQLAlchemy session object.
        product_name (Optional[str]): Name of the product to filter by.
        store_name (Optional[str]): Name of the store to filter by.
        max_price (float): Max price to filter by.
        is_available (bool): Availability to filter by. True if the product is in stock/False if not.
        category (str): Category to filter by.

    Returns:
        List[StockResponse]: List of stocks with their details.

    Raises:
        ValueError: If no stocks are found.
    """
    query = db.query(Stock).options(joinedload(Stock.product), joinedload(Stock.store))

    # Apply filters based on provided parameters
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

    # Execute the query and get all results
    stocks = query.all()

    # If no stocks found, raise an exception
    if not stocks:
        raise ValueError("No matching stocks found")
    
    stock_responses = [
        StockResponse(
            id=stock.id,
            store_id=stock.store_id,
            product_id=stock.product_id,
            price=stock.price,
            is_available=stock.is_available,
            category=stock.category,
            product_name=stock.product.name,
            store_name=stock.store.name
        ).model_dump()  # Serialize using model_dump() here
        for stock in stocks
    ]

    return stock_responses


# ------------ API DELETE ------------

def delete_stock_service(stock_id: int, db: Session) -> dict:
    """
    Service to delete a stock by ID from the database.

    Args:
        stock_id (int): The ID of the stock to delete.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the ID of the deleted store.
    """
    stock = db.query(Stock).filter(Stock.id == stock_id).first()
    
    if not stock:
        raise ValueError("Stock not found")
    
    # Delete the stock
    db.delete(stock)
    db.commit()

    # Return the deleted product ID as confirmation
    return {"stock_id": stock_id}


# ------------ API UPDATE ------------

def update_stock_service(
    db: Session, 
    stock_id: int, 
    stock_update: StockUpdate
) -> Stock:
    """
    Service to update a stock by ID.

    Args:
        db (Session): The SQLAlchemy session.
        stock_id (int): The ID of the stock to update.
        stock_update (StockUpdate): The schema containing the details of the stock to be updated.

    Returns:
        Stock: The schema of the updated store details.
        
    Raises:
        ValueError: If the store with the given ID is not found or if there's nothing to update.
    """
    # Fetch the stock to update
    stock = db.query(Stock).filter(Stock.id == stock_id).first()

    if not stock:
        raise ValueError("Stock not found")

    # Check if any field is provided for update
    updated = False

    if stock_update.price is not None:
        stock.price = stock_update.price
        updated = True
    if stock_update.is_available is not None:
        stock.is_available = stock_update.is_available
        updated = True
    if stock_update.category is not None:
        stock.category = stock_update.category
        updated = True

    # If no fields are provided, raise an error
    if not updated:
        raise ValueError("Nothing to update")

    db.commit()
    db.refresh(stock)  # Refresh the stock to get the updated data
    
    return stock._asdict()