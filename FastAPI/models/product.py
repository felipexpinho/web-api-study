from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from database.session import Base

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    stock: Mapped[List["Stock"]] = relationship(back_populates="product")  # Use forward reference

    def __repr__(self) -> str:
        return f"""<Product
        id: {self.id}
        name: {self.name}
        """  

    def _asdict(self):
        from models.stock import Stock  # Import here to avoid circular import
        return {
            "id": self.id,
            "name": self.name,
            "stock": self._getProductStock(),
        }

    def _getProductStock(self):
        return [stock._asdict() for stock in self.stock]

    def getId(self):
        return self.id