from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated

PyObjectId = Annotated[str, BeforeValidator(str)]


class Category(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    parent_name: str
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "name": "string",
                "parent_name": "string",
            }
        },
    )


class Part(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    serial_number: str = Field(unique=True)
    name: str
    description: str
    category: str
    quantity: int
    price: float
    location: Dict[str, str] = Field(room="", bookcase="", shelf="", cuvette="", column="", row="")
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "serial_number": "string",
                "name": "string",
                "description": "string",
                "category": "string",
                "quantity": 0,
                "price": 0,
                "location": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                }
            }
        },
    )
