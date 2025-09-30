from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(min_length=6)


class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    title: str
    description: Optional[str]
    category: Optional[str]
    tags: Optional[str]


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class RatingBase(BaseModel):
    item_id: int
    score: float = Field(ge=0, le=5)


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    user_id: int
    created_at: datetime
    item: Item

    class Config:
        orm_mode = True


class Recommendation(BaseModel):
    item: Item
    score: float
    strategy: str


class RecommendationResponse(BaseModel):
    recommendations: List[Recommendation]
    generated_at: datetime


class RecommendationLog(BaseModel):
    id: int
    strategy: str
    recommended_items: str
    created_at: datetime

    class Config:
        orm_mode = True
