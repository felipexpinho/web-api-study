from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError

from services.store import *

store_blueprint = Blueprint("store", __name__)


# ------------ API POST ------------

@store_blueprint.route("/", methods=["POST"])
def create_store():
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Parse request JSON
        store_data = request.get_json()

        if "name" not in store_data:
            return jsonify({"error": "Field required"}), 422
        
        if not isinstance(store_data["name"], str) or not store_data["name"]:
            return jsonify({"error": "Input should be a valid string"}), 422

        # Call service to create store
        new_store = create_store_service(store_data=store_data, db=db)  # Pass the session explicitly
        return jsonify({
            "status": "success",
            "message": "Store created successfully",
            "data": new_store
        }), 201
    except SQLAlchemyError as e:
        db.rollback()  # Roll back the transaction on SQLAlchemy errors
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.rollback()  # Roll back the transaction on other exceptions
        return jsonify({"error": "Bad request", "details": str(e)}), 400


# ------------ API GET ------------

@store_blueprint.route("/", methods=["GET"])
def get_stores():
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Extract query parameters
        store_id = request.args.get("id", type=int)
        name = request.args.get("name", type=str)

        # Call the service to fetch store data
        stores = get_stores_service(db=db, store_id=store_id, name=name)

        return jsonify({
            "status": "success",
            "message": "Stores fetched successfully",
            "data": stores
        }), 200

    except ValueError as e:
        return jsonify({"error": "Store not found", "details": str(e)}), 404
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Bad request", "details": str(e)}), 400
    

# ------------ API DELETE ------------

@store_blueprint.route("/<int:store_id>", methods=["DELETE"])
def delete_store_endpoint(store_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Call the service to delete store data
        result = delete_store_service(store_id, db)

        return jsonify({
            "status_code": 200,
            "message": "Store deleted successfully",
            "data": result
        }), 200
    
    except ValueError as e:
        return jsonify({"error": "Not Found", "message": str(e)}), 404
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "Internal Server Error", "message": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Bad Request", "message": str(e)}), 400
    

# ------------ API UPDATE ------------

@store_blueprint.route("/<int:store_id>", methods=["PUT"])
def update_store_endpoint(store_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Parse request JSON
        store_data = request.get_json()

        if "name" not in store_data:
            return jsonify({"error": "Field required"}), 422
        
        if not isinstance(store_data["name"], str) or not store_data["name"]:
            return jsonify({"error": "Input should be a valid string"}), 422

        # Call the service to update the store
        updated_store = update_store_service(store_id=store_id, store_update=store_data, db=db)

        return jsonify({
            "status": "success",
            "message": "Store updated successfully",
            "data": updated_store
        }), 200

    except ValueError as e:
        return jsonify({"error": "Not Found", "message": str(e)}), 404
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400