from models.store import Store
from sqlalchemy.orm import Session

def create_store_service(store_data: dict, db: Session) -> dict:
    """
    Service to create a new store in the database.
    :param store_data: Dictionary containing store details.
    :param db: The SQLAlchemy session.
    :return: Dictionary with the created store's details.
    """
    try:
        # Create and save new store
        new_store = Store(name=store_data["name"])
        db.add(new_store)
        db.commit()
        db.refresh(new_store)
        
        return {"id": new_store.id, "name": new_store.name}
    except Exception as e:
        db.rollback()
        raise e