from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Game(BaseModel):
    title: str
    description: str
    price: float
    genre: str
    platform: str
    image_url: Optional[str] = None
    stock: int = 0

class CartItem(BaseModel):
    game_id: str
    quantity: int = 1

class OrderItem(BaseModel):
    game_id: str
    title: str
    price: float
    quantity: int

class Order(BaseModel):
    user_id: str
    items: List[OrderItem]
    total: float
    status: str = "pending"
    created_at: datetime = Field(default_factory=datetime.utcnow)
