from typing import Dict, Union
from pydantic import BaseModel, Field


class Category(BaseModel):
    name: str
    parent_name: str


class Part(BaseModel):
    serial_number: str = Field(unique=True)
    name: str
    description: str
    category: str
    quantity: int
    price: float
    location: Dict[str, str] = Field(room="", bookcase="", shelf="", cuvette="", column="", row="")
