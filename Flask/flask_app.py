from flask import Flask, g
from routes.store import store_blueprint
from database.session import Base, engine, SessionLocal

# Import all models to register them with Base.metadata
from models.store import Store
from models.product import Product
from models.stock import Stock

app = Flask(__name__)

# Register blueprints
app.register_blueprint(store_blueprint, url_prefix="/store")

@app.before_request
def create_db_session():
    """Create a new database session before each request."""
    g.db = SessionLocal()

@app.teardown_request
def close_db_session(exception=None):
    """Close the database session after each request."""
    db = g.pop("db", None)
    if db:
        db.close()

if __name__ == "__main__":
    # Create all tables
    Base.metadata.create_all(bind=engine)

    app.run(debug=True, port=8000)