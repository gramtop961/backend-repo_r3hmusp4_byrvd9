"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field
from typing import Optional, List

# Example schemas (kept for reference):

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product" (lowercase of class name)
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")

# Coffee shop app schemas

class MenuItem(BaseModel):
    """
    Coffee shop menu items
    Collection: "menuitem"
    """
    name: str
    description: Optional[str] = None
    price: float = Field(..., ge=0)
    category: str = Field(..., description="e.g., Coffee, Tea, Pastry")
    image: Optional[str] = Field(None, description="Image URL")
    available: bool = True

class CateringRequest(BaseModel):
    """
    Catering reservation requests
    Collection: "cateringrequest"
    """
    name: str
    email: str
    phone: str
    event_date: str = Field(..., description="ISO date string")
    guests: int = Field(..., ge=1, le=1000)
    notes: Optional[str] = None

class OrderItem(BaseModel):
    item_id: str = Field(..., description="MenuItem document _id as string")
    name: str
    quantity: int = Field(..., ge=1)
    price: float = Field(..., ge=0)

class Order(BaseModel):
    """
    Pickup orders
    Collection: "order"
    """
    customer_name: str
    phone: str
    items: List[OrderItem]
    subtotal: float = Field(..., ge=0)
    tax: float = Field(..., ge=0)
    total: float = Field(..., ge=0)
    pickup_time: Optional[str] = Field(None, description="ISO time string or short text like 'ASAP'")
