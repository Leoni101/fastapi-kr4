from pydantic import BaseModel, EmailStr, conint, constr, Field
from typing import Optional

# Схемы для Product (Задание 9.1)
class ProductBase(BaseModel):
    title: str
    price: float
    count: int

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    description: str

class ProductResponse(ProductBase):
    id: int
    description: str
    
    class Config:
        from_attributes = True

# Схема для валидации пользователя (Задание 10.2)
class User(BaseModel):
    username: str
    age: conint(gt=18)  # greater than 18
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "age": 25,
                "email": "john@example.com",
                "password": "securepass123",
                "phone": "+1234567890"
            }
        }