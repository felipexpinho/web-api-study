from flask import Blueprint, request, jsonify, g
from sqlalchemy.exc import SQLAlchemyError
from services.product import *

product_blueprint = Blueprint("product", __name__)

# ------------ API POST ------------

@product_blueprint.route("/", methods=["POST"], strict_slashes=False)
def create_product_endpoint():
    db = g.db  # Get the database session created in `@before_request`
    try:
        product_data = request.get_json()

        new_product = create_product_service(product_data=product_data, db=db)

        return jsonify({
            "status": "success",
            "message": "Product created successfully",
            "data": new_product
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

@product_blueprint.route("/", methods=["GET"], strict_slashes=False)
def get_products_endpoint():
    db = g.db  # Get the database session created in `@before_request`
    try:
        # Extract query parameters
        product_id = request.args.get("id", type=int, default=None)
        name = request.args.get("name", type=str, default=None)

        products = get_products_service(db=db, product_id=product_id, name=name)

        return jsonify({
            "status": "success",
            "message": "Products fetched successfully",
            "data": products
        }), 200

    except ValueError as e:
        return jsonify({"detail": [{"msg": "Product not found", "error": str(e)}]}), 404
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400

# ------------ API DELETE ------------

@product_blueprint.route("/<int:product_id>", methods=["DELETE"])
def delete_product_endpoint(product_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        result = delete_product_service(product_id, db)

        return jsonify({
            "status_code": 200,
            "message": "Product deleted successfully",
            "data": result
        }), 200

    except ValueError as e:
        return jsonify({"detail": [{"msg": "Product not found", "error": str(e)}]}), 404
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400

# ------------ API UPDATE ------------

@product_blueprint.route("/<int:product_id>", methods=["PUT"])
def update_product_endpoint(product_id):
    db = g.db  # Get the database session created in `@before_request`
    try:
        product_data = request.get_json()

        updated_product = update_product_service(product_id=product_id, product_update=product_data, db=db)

        return jsonify({
            "status": "success",
            "message": "Product updated successfully",
            "data": updated_product
        }), 200

    except KeyError as e:
        return jsonify({"detail": [{"msg": "Field required", "error": str(e)}]}), 422
    
    except TypeError as e:
        return jsonify({"detail": [{"msg": "Invalid type", "error": str(e)}]}), 422
    
    except ValueError as e:
        return jsonify({"detail": [{"msg": "Product not found", "error": str(e)}]}), 404
    
    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Database error", "error": str(e)}]}), 500
    
    except Exception as e:
        db.rollback()
        return jsonify({"detail": [{"msg": "Bad request", "error": str(e)}]}), 400