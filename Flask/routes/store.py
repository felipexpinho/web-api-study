from flask import Blueprint, request, jsonify, g
from services.store import create_store_service
from sqlalchemy.exc import SQLAlchemyError

store_blueprint = Blueprint("store", __name__)

@store_blueprint.route("/", methods=["POST"])
def create_store():
    """Route to create a new store."""
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Parse request JSON
        store_data = request.get_json()
        if "name" not in store_data:
            return jsonify({"error": "Field required"}), 422
        
        if not isinstance(store_data["name"], str) or not store_data["name"]:
            return jsonify({"error": "Input should be a valid string"}), 422

        # Call service to create store
        new_store = create_store_service(store_data, db)  # Pass the session explicitly
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