from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Dict, Any

from models.product import Product
from models.stock import Stock

# ------------ API POST ------------

def create_product_service(product_data: dict, db: Session) -> dict:
    """
    Service to create a new product in the database.

    Args:
        product_data (dict): A dictionary containing the details of the product to be created.
            Required key: "name" (str): The name of the product.
        db (Session): SQLAlchemy session object.

    Returns:
        dict: A dictionary containing the details of the created product.
            "id" (int): The unique ID of the created product.
            "name" (str): The name of the created product.

    Raises:
        Exception: If any error occurs during the database transaction, it is rolled back, and the exception is re-raised.
    """
    try:
        new_product = Product(name=product_data["name"])
        db.add(new_product)
        db.commit()
        db.refresh(new_product)

        return new_product._asdict_no_stock()
    except Exception as e:
        db.rollback()
        raise e

# ------------ API GET ------------

def get_products_service(db: Session, product_id: Optional[int] = None, name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Service function to fetch products based on optional filters.

    Args:
        product_id (Optional[int]): ID of the product to filter by.
        name (Optional[str]): Name of the product to filter by.
        db (Session): SQLAlchemy session object.

    Returns:
        List[Dict[str, Any]]: List of products with their details.

    Raises:
        ValueError: If no products are found.
    """
    query = db.query(Product).options(joinedload(Product.stock).joinedload(Stock.store))

    # Filter by product ID or name if provided
    if product_id is not None:
        query = query.filter(Product.id == product_id)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    products = query.all()

    if not products:
        raise ValueError("Product not found")

    return [product._asdict() for product in products]

# ------------ API DELETE ------------

def delete_product_service(product_id: int, db: Session) -> dict:
    """
    Service to delete a product by ID from the database.

    Args:
        product_id (int): The ID of the product to delete.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the ID of the deleted product.

    Raises:
        ValueError: If the product with the given ID does not exist.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise ValueError("Product not found")

    # Delete associated stocks
    for stock in product.stock:
        db.delete(stock)

    # Delete the product itself
    db.delete(product)
    db.commit()
    
    # Return the deleted product ID as confirmation
    return {"product_id": product_id}

# ------------ API UPDATE ------------

def update_product_service(product_id: int, product_update: dict, db: Session) -> dict:
    """
    Service to update a product by ID.

    Args:
        product_id (int): The ID of the product to update.
        product_update (dict): Dictionary containing the updated product data.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary with the updated product details.
        
    Raises:
        ValueError: If the product with the given ID is not found.
    """
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise ValueError("Product not found")

    # Update the product fields
    product.name = product_update["name"]

    db.commit()
    db.refresh(product)

    return product._asdict_no_stock()