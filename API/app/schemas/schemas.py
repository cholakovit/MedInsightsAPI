from typing import Optional
from pydantic import BaseModel

class ItemSchema(BaseModel):   
    id: Optional[str]
    name: str
    description: str
    metadata: dict

    class Config:
        from_attributes = True

class ResponseSchema(BaseModel):
    id: str
    success: bool
    message: str





