from sqlalchemy.orm import Session, joinedload
from typing import List, Optional

from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from schemas.stock import StockResponse

from models.product import Product
from models.stock import Stock

# ------------ API POST ------------

def create_product_service(product: ProductCreate, db: Session) -> dict:
    # Create the new product
    new_product = Product(name=product.name)
    db.add(new_product)
    db.commit()
    db.refresh(new_product)  # Refresh to get the ID

    return new_product._asdict()


# ------------ API GET ------------

def get_products_service(id: Optional[int], name: Optional[str], db: Session):
    query = db.query(Product).options(joinedload(Product.stock).joinedload(Stock.store))  # Join stock and product

    # Filter by product id or name if provided
    if id:
        query = query.filter(Product.id == id)
    if name:
        query = query.filter(Product.name.ilike(f"%{name}%"))

    products = query.all()

    if not products:
        raise ValueError("Product not found")  # Raise a generic exception to signal the controller

    product_responses = [
        ProductResponse(
            id=product.id,
            name=product.name,
            stock=[
                StockResponse(
                    id=stock.id,
                    store_id=stock.store_id,
                    product_id=stock.product_id,
                    price=stock.price,
                    is_available=stock.is_available,
                    category=stock.category,
                    product_name=stock.product.name,
                    store_name=stock.store.name
                )
                for stock in product.stock
            ]
        ).model_dump()  # Use model_dump() to serialize the ProductResponse instance
        for product in products
    ]

    return product_responses


# ------------ API DELETE ------------

def delete_product_service(product_id: int, db: Session) -> dict:
    # Query the product by ID
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

def update_product_service(product_id: int, product_update: ProductUpdate, db: Session) -> dict:
    # Query the product by ID
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise ValueError("Product not found")
    
    # Update the product data
    product.name = product_update.name
    db.commit()
    db.refresh(product)
    
    # Return the updated product data
    return product._asdict()