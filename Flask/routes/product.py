from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from services.product import *

product_blueprint = Blueprint("product", __name__)

# ------------ API POST ------------

@product_blueprint.route("/", methods=["POST"])
def create_product():
    db = g.db  # Get the database session created in `@before_request`
    try:
        product_data = request.get_json()

        if "name" not in product_data:
            return jsonify({"error": "Field required"}), 422

        if not isinstance(product_data["name"], str) or not product_data["name"]:
            return jsonify({"error": "Input should be a valid string"}), 422

        new_product = create_product_service(product_data=product_data, db=db)
        return jsonify({
            "status": "success",
            "message": "Product created successfully",
            "data": new_product
        }), 201
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Bad request", "details": str(e)}), 400

# ------------ API GET ------------

@product_blueprint.route("/", methods=["GET"])
def get_products():
    db = g.db  # Get the database session created in `@before_request`
    try:
        product_id = request.args.get("id", type=int)
        name = request.args.get("name", type=str)

        products = get_products_service(db=db, product_id=product_id, name=name)

        return jsonify({
            "status": "success",
            "message": "Products fetched successfully",
            "data": products
        }), 200

    except ValueError as e:
        return jsonify({"error": "Product not found", "details": str(e)}), 404
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Bad request", "details": str(e)}), 400

# ------------ API DELETE ------------

@product_blueprint.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        result = delete_product_service(product_id, db)

        return jsonify({
            "status_code": 200,
            "message": "Product deleted successfully",
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

@product_blueprint.route("/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        product_data = request.get_json()

        if "name" not in product_data:
            return jsonify({"error": "Field required"}), 422

        if not isinstance(product_data["name"], str) or not product_data["name"]:
            return jsonify({"error": "Input should be a valid string"}), 422

        updated_product = update_product_service(product_id=product_id, product_update=product_data, db=db)

        return jsonify({
            "status": "success",
            "message": "Product updated successfully",
            "data": updated_product
        }), 200

    except ValueError as e:
        return jsonify({"error": "Not Found", "message": str(e)}), 404
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "Bad Request", "details": str(e)}), 400