from pydantic import BaseModel
from typing import List, Dict

class Item(BaseModel):
    id: str
    name: str
    description: str
    metadata: Dict[str, str]

    class Config:
        from_attributes = True  

class VectorData(BaseModel):
    id: str
    vector: List[float]

    class Config:
        from_attributes = True