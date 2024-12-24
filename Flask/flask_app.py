# Import all models to register them with Base.metadata
from models.store import Store
from models.product import Product
from models.stock import Stock

from utils.create_app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=8000)