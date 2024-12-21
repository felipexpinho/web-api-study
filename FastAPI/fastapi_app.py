import uvicorn

from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Optional

from schemas.product import ProductCreate, ProductResponse, ProductUpdate
from schemas.store import StoreCreate, StoreResponse, StoreUpdate
from schemas.stock import StockCreate, StockResponse, StockUpdate

from services.product import *
from services.store import *
from services.stock import *

from database.session import Base, engine, get_db

from utils.response import create_response

app = FastAPI()

# ------------ API POST ------------

@app.post("/store", response_model=StoreResponse)
def create_store_endpoint(store: StoreCreate, db: Session = Depends(get_db)):
    try:
        new_store = create_store_service(store, db)
        
        return create_response(
            status_code=status.HTTP_201_CREATED,
            message="Store created successfully",
            data=new_store
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

@app.post("/product", response_model=ProductResponse)
def create_product_endpoint(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        new_product = create_product_service(product, db)

        return create_response(
            status_code=status.HTTP_201_CREATED,
            message="Product created successfully",
            data=new_product
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.post("/stock", response_model=StockResponse)
def create_stock_endpoint(stock: StockCreate, db: Session = Depends(get_db)):
    try:
        new_stock = create_stock_service(stock, db)

        return create_response(
            status_code=status.HTTP_201_CREATED,
            message="Stock created successfully",
            data=new_stock
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    

# ------------ API GET ------------

@app.get("/stores", response_model=List[StoreResponse])
def get_stores_endpoint(
    id: Optional[int] = None, name: Optional[str] = None, db: Session = Depends(get_db)
):
    try:
        stores = get_stores_service(id=id, name=name, db=db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Stores fetched successfully",
            data=stores
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/products", response_model=List[ProductResponse])
def get_products_endpoint(id: Optional[int] = None, name: Optional[str] = None, db: Session = Depends(get_db)):
    try:
        products = get_products_service(id=id, name=name, db=db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Products fetched successfully",
            data=products
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/stocks", response_model=List[StockResponse])
def get_stocks_endpoint(
    product_name: Optional[str] = None,
    store_name: Optional[str] = None,
    max_price: Optional[float] = None,
    is_available: Optional[bool] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    try:
        stocks = get_stocks_service(
            db=db,
            product_name=product_name,
            store_name=store_name,
            max_price=max_price,
            is_available=is_available,
            category=category
        )
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Stocks fetched successfully",
            data=stocks
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ------------ API DELETE ------------

@app.delete("/store/{store_id}", status_code=status.HTTP_200_OK)
def delete_store_endpoint(store_id: int, db: Session = Depends(get_db)):
    try:
        result = delete_store(store_id, db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Store deleted successfully",
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/product/{product_id}", status_code=status.HTTP_200_OK)
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    try:
        result = delete_product_service(product_id, db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Product deleted successfully",
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/stock/{stock_id}", status_code=status.HTTP_200_OK)
def delete_stock_endpoint(stock_id: int, db: Session = Depends(get_db)):
    try:
        result = delete_stock_service(stock_id, db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Stock deleted successfully",
            data=result
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


# ------------ API UPDATE ------------

@app.put("/store/{store_id}", response_model=StoreResponse)
def update_store_endpoint(store_id: int, store_update: StoreUpdate, db: Session = Depends(get_db)):
    try:
        store_data = update_store_service(store_id, store_update, db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Store updated successfully",
            data=store_data
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/product/{product_id}", response_model=ProductResponse)
def update_product_endpoint(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
    try:
        product_data = update_product_service(product_id, product_update, db)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Product updated successfully",
            data=product_data
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.put("/stock/{stock_id}", response_model=StockResponse)
def update_stock_endpoint(stock_id: int, stock_update: StockUpdate, db: Session = Depends(get_db)):
    try:
        updated_stock = update_stock_service(db, stock_id, stock_update)
        return create_response(
            status_code=status.HTTP_200_OK,
            message="Stock updated successfully",
            data=updated_stock
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    uvicorn.run(app, host="127.0.0.1", port=8000)