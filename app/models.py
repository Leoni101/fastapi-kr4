from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    description = Column(String, nullable=False, default="")  # Добавлено позже
    
    def __repr__(self):
        return f"<Product(id={self.id}, title='{self.title}', price={self.price}, count={self.count})>"