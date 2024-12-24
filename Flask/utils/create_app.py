from flask import Flask, g

from routes.store import store_blueprint
from routes.stock import stock_blueprint
from routes.product import product_blueprint
from database.session import Base, engine, SessionLocal
import database.test_session as test_session

def create_app(config_name="default"):
    app = Flask(__name__)
    
    if config_name == "testing":
        app.config.update({
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///./test.db",  # Use test.db for testing
            "DEBUG": False
        })

        # Database session management
        @app.before_request
        def create_db_session():
            """Create a new database session before each request."""
            g.db = test_session.SessionLocal()

        @app.teardown_request
        def close_db_session(exception=None):
            """Close the database session after each request."""
            db = g.pop("db", None)
            if db:
                db.close()
    else:
        # Create all tables
        Base.metadata.create_all(bind=engine)

        # Database session management
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

    # Register blueprints
    app.register_blueprint(store_blueprint, url_prefix="/store")
    app.register_blueprint(stock_blueprint, url_prefix="/stock")
    app.register_blueprint(product_blueprint, url_prefix="/product")

    return app