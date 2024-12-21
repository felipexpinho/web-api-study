from flask import Flask, request, jsonify
from sqlalchemy.orm import Session
from database.session import SessionLocal, Base, engine
from models.store import Store

# Create all tables
Base.metadata.create_all(bind=engine)

app = Flask(__name__)

@app.route("/store", methods=["POST"])
def create_store():
    db: Session = SessionLocal()
    try:
        data = request.get_json()
        if "name" not in data:
            return jsonify({"error": "Missing parameter 'name'"}), 400

        new_store = Store(name=data["name"])
        db.add(new_store)
        db.commit()
        db.refresh(new_store)  # Refresh to get the ID
        return jsonify(new_store._asdict()), 201
    except Exception as e:
        db.rollback() # Undo anything that has been done inside the Try
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()