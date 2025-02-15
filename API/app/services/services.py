import numpy as np
from ..repositories.repositories import save_vector
from uuid import uuid4
from ..repositories.repositories import fetch_all_records
from sentence_transformers import SentenceTransformer

# Load MPNet model once (global variable to avoid reloading on every request)
mpnet_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def generate_vector(description: str) -> list:
    """
    Generate a semantic embedding vector using MPNet.
    """
    vector = mpnet_model.encode(description)  # Generates a 768-dim vector
    print(f"Generated vector (length: {len(vector)}): {vector[:5]}...")  # Print first 5 values
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