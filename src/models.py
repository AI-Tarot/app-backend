from pydantic import BaseModel
from typing import Optional


# User model to store user information
class User(BaseModel):
    username: str
    sex: str
    age: int
    custom_info: str

# Tarot card model
class TarotCard(BaseModel):
    name: str
    description: str
    image_url: str

# Request model for the tarot reading
class TarotReadingRequest(BaseModel):
    question: str

# Response model for the tarot reading
class TarotReadingResponse(BaseModel):
    reading: str
    card: TarotCard
    additional_info: Optional[str] = None