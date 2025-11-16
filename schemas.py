"""
Database Schemas for Eddy & Ink

Each Pydantic model represents a collection in MongoDB.
Collection name is the lowercase of the class name.
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Literal


class Book(BaseModel):
    """Books for sale/download"""
    title: str = Field(..., description="Book title")
    subtitle: Optional[str] = Field(None, description="Optional subtitle")
    description: Optional[str] = Field(None, description="Short marketing description")
    category: Literal[
        "cookbook",
        "coloring",
        "children",
        "story",
        "guide",
        "poetry",
        "other",
    ] = Field("other", description="Category of the book")
    price: float = Field(0.0, ge=0, description="Price in USD (0 for free)")
    cover_url: Optional[str] = Field(None, description="URL to the cover image")
    sample_url: Optional[str] = Field(None, description="Public sample PDF URL")
    download_url: Optional[str] = Field(None, description="Full book file URL (protected in real app)")
    featured: bool = Field(False, description="Whether to show on the homepage")


class Subscriber(BaseModel):
    """Newsletter subscribers"""
    name: Optional[str] = Field(None, description="Subscriber name")
    email: EmailStr = Field(..., description="Subscriber email")
    source: Optional[str] = Field("website", description="Where the subscriber signed up")


# Example existing schemas kept for reference/compatibility
class User(BaseModel):
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")


class Product(BaseModel):
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category")
    in_stock: bool = Field(True, description="Whether product is in stock")
