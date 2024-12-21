from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from database.session import Base

class Stock(Base):
    __tablename__ = "stock"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    is_available: Mapped[bool] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    store: Mapped["Store"] = relationship(back_populates="stock")
    product: Mapped["Product"] = relationship(back_populates="stock")  # Use forward reference

    def _asdict(self):
        from models.product import Product  # Import here to avoid circular import
        return {
            "id": self.id,
            "store_id": self.store_id,
            "product_id": self.product_id,
            "price": self.price,
            "is_available": self.is_available,
            "category": self.category,
            "store": self.store.name,
            "product_name": self.product.name,
        }

    def _getPrice(self):
        return self.price

    def getId(self):
        return self.id