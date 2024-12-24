from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError

from services.stock import *

stock_blueprint = Blueprint("stock", __name__)


# ------------ API POST ------------

@stock_blueprint.route("/", methods=["POST"], strict_slashes=False)
def create_stock_endpoint():
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Parse request JSON
        stock_data = request.get_json()

        # Call service to create store
        new_stock = create_stock_service(stock_data=stock_data, db=db)

        return jsonify({
            "status": "success",
            "message": "Stock created successfully",
            "data": new_stock
        }), 201
    
    except KeyError as e:
        return jsonify({"detail": [{"msg": "Field required", "error": str(e)}]}), 422
    
    except TypeError as e:
        return jsonify({"detail": [{"msg": "Invalid type", "error": str(e)}]}), 422
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400


# ------------ API GET ------------

@stock_blueprint.route("/", methods=["GET"], strict_slashes=False)
def get_stocks_endpoint():
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Extract query parameters
        product_name = request.args.get("product_name", type=str, default=None)
        store_name = request.args.get("store_name", type=str, default=None)
        max_price = request.args.get("max_price", type=float, default=None)
        is_available = request.args.get("is_available", type=bool, default=None)
        category = request.args.get("category", type=str, default=None)

        # Call the service to fetch store data
        stocks = get_stocks_service(
            db=db,
            product_name=product_name,
            store_name=store_name,
            max_price=max_price,
            is_available=is_available,
            category=category,
        )

        return jsonify({
            "status": "success",
            "message": "Stocks fetched successfully",
            "data": stocks
        }), 200

    except ValueError as e:
        return jsonify({"detail": [{"msg": "Stock not found", "error": str(e)}]}), 404
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400


# ------------ API DELETE ------------

@stock_blueprint.route("/<int:stock_id>", methods=["DELETE"])
def delete_stock_endpoint(stock_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Call the service to delete stock data
        result = delete_stock_service(stock_id, db)

        return jsonify({
            "status_code": 200,
            "message": "Stock deleted successfully",
            "data": result
        }), 200
    
    except ValueError as e:
        return jsonify({"detail": [{"msg": "Stock not found", "error": str(e)}]}), 404
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400


# ------------ API UPDATE ------------

@stock_blueprint.route("/<int:stock_id>", methods=["PUT"])
def update_stock_endpoint(stock_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Parse request JSON
        stock_data = request.get_json()

        # Call the service to update the stock
        updated_stock = update_stock_service(stock_id=stock_id, stock_update=stock_data, db=db)

        return jsonify({
            "status": "success",
            "message": "Stock updated successfully",
            "data": updated_stock
        }), 200

    except KeyError as e:
        return jsonify({"detail": [{"msg": "Nothing to update", "error": str(e)}]}), 404
    
    except TypeError as e:
        return jsonify({"detail": [{"msg": "Invalid type", "error": str(e)}]}), 422
    
    except ValueError as e:
        return jsonify({"detail": [{"msg": "Stock not found", "error": str(e)}]}), 404
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400
