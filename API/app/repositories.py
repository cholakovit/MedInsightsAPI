from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
from uuid import uuid4

# Initialize Qdrant client
client = QdrantClient(url="http://localhost:6333")

def create_collection():
    """Create the collection if it doesn't exist."""
    try:
        collections = client.get_collections().collections
        collection_names = [collection.name for collection in collections]

        if "medinsights" in collection_names:
            print("Collection `medinsights` already exists. Skipping creation.")
        else:
            client.create_collection(
                collection_name="medinsights",
                vectors_config={"size": 300, "distance": "Cosine"}
            )
            print("Collection `medinsights` created successfully!")
    except Exception as e:
        print(f"Error checking or creating collection: {e}")

def save_vector(id: str, vector: list, payload: dict):
    """Save a vector and its payload to Qdrant."""
    try:
        validated_id = validate_id(id)  # Validate and format ID
        print(f"Validated ID: {validated_id}")
        client.upsert(
            collection_name="medinsights",
            points=[
                PointStruct(
                    id=validated_id,
                    vector=vector,
                    payload=payload
                )
            ]
        )
        print("Vector saved successfully!")
        return True
    except Exception as e:
        print(f"Error saving vector: {e}")
        return False

def validate_id(id):
    """Validate and format the ID as required by Qdrant."""
    try:
        # Try to interpret as an integer
        return int(id)
    except ValueError:
        try:
            # Try to interpret as a UUID
            return str(UUID(id))
        except ValueError:
            raise ValueError("Invalid ID: must be an unsigned integer or a UUID")
        
