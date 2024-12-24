from sqlalchemy.orm import Session, joinedload
from typing import Optional, List, Dict, Any

from models.store import Store
from models.stock import Stock


# ------------ API POST ------------

def create_store_service(store_data: dict, db: Session) -> dict:
    """
    Service to create a new store in the database.

    Args:
        store_data (dict): A dictionary containing the details of the store to be created.
            - Required key: "name" (str): The name of the store.
        db (Session): SQLAlchemy session object.

    Returns:
        dict: A dictionary containing the details of the created store.
            - Keys:
                - "id" (int): The unique ID of the created store.
                - "name" (str): The name of the created store.

    Raises:
        Exception: If any error occurs during the database transaction, it is rolled back, 
                   and the exception is re-raised.
    """
    try:
        # Create and save new store
        new_store = Store(name=store_data["name"])
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        
        return new_store._asdict_no_stock()
    except Exception as e:
        db.rollback()
        raise e


# ------------ API GET ------------

def get_stores_service(db: Session, store_id: Optional[int] = None, name: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Service function to fetch stores based on optional filters.

    Args:
        store_id (Optional[int]): ID of the store to filter by.
        name (Optional[str]): Name of the store to filter by.
        db (Session): SQLAlchemy session object.

    Returns:
        List[Dict[str, Any]]: List of stores with their details.

    Raises:
        ValueError: If no stores are found.
        RuntimeError: If db is None.
    """
    query = db.query(Store).options(joinedload(Store.stock).joinedload(Stock.product))

    # Filter by store ID or name if provided
    if store_id is not None:
        query = query.filter(Store.id == store_id)
    if name:
        query = query.filter(Store.name.ilike(f"%{name}%"))

    stores = query.all()

    if not stores:
        raise ValueError("Store not found")

    return [store._asdict() for store in stores]


# ------------ API DELETE ------------

def delete_store_service(store_id: int, db: Session) -> dict:
    """
    Service to delete a store by ID from the database.

    Args:
        store_id (int): The ID of the store to delete.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary containing the ID of the deleted store.

    Raises:
        ValueError: If the store with the given ID does not exist.
    """
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise ValueError("Store not found")
    
    # Delete associated stocks
    for stock in store.stock:
        db.delete(stock)
    
    # Delete the store itself
    db.delete(store)
    db.commit()
    
    # Return the deleted store ID as confirmation
    return {"store_id": store_id}


# ------------ API UPDATE ------------

def update_store_service(store_id: int, store_update: dict, db: Session) -> dict:
    """
    Service to update a store by ID.

    Args:
        store_id (int): The ID of the store to update.
        store_update (dict): Dictionary containing the updated store data.
        db (Session): The SQLAlchemy session.

    Returns:
        dict: A dictionary with the updated store details.
        
    Raises:
        ValueError: If the store with the given ID is not found.
        KeyError: If required fields are missing in the update data.
        TypeError: If the field types are incorrect.
    """
    store = db.query(Store).filter(Store.id == store_id).first()
    
    if not store:
        raise ValueError("Store not found")

    # Update the store fields
    store.name = store_update["name"]

    db.commit()
    db.refresh(store)

    # Return the updated store data
    return store._asdict_no_stock()