
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from database.session import Base
from models.stock import Stock

class Store(Base):
    __tablename__ = "stores"
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    stock: Mapped[List[Stock]] = relationship(back_populates="store")

    def _asdict(self):
        return {
            "id": self.id,
            "name": self.name,
        }

    def getId(self):
        return self.id