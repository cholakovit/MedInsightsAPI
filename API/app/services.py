import numpy as np
from .repositories import save_vector
from uuid import uuid4
from .repositories import fetch_all_records

def generate_vector(description: str) -> list:
    vector = [ord(char) / 255.0 for char in description][:300]
    if len(vector) < 300:  # Pad vector to match the required size
        vector += [0.0] * (300 - len(vector))
    print(f"Generated vector (length: {len(vector)}): {vector[:5]}...")
    return np.array(vector, dtype=np.float32).tolist()

def process_item(item):
    vector = generate_vector(item.description)
    item_id = item.id or str(uuid4())  # Use provided id or generate a new UUID
    success = save_vector(item_id, vector, item.dict())
    return success

def generate_id():
    return str(uuid.uuid4())

def get_all_records_service():
    """Service function to retrieve records from the repository."""
    records = fetch_all_records() # Exception is automatically handled by decorators
    return { "success": True, "records": records }