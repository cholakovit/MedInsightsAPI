from fastapi import FastAPI, HTTPException
from .schemas import ItemSchema, ResponseSchema
from .services import process_item
from .repositories import client

app = FastAPI()

@app.get("/test")
def test_route():
    """A simple test route to verify the server is running."""
    return {"success": True, "message": "Test success!"}

@app.post("/upload/", response_model=ResponseSchema)
def upload_item(item: ItemSchema):
    success = process_item(item)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save vector")
    return ResponseSchema(success=True, message="Item saved successfully", id=item.id or "generated-id")

@app.get("/records/")
def get_all_records():
    """Retrieve all records from the Qdrant collection."""
    try:
        results = client.scroll(
            collection_name="medinsights",
            with_payload=True,
            with_vectors=True,
            limit=100  # Adjust limit as needed
        )
        return {"success": True, "records": results[0]}  # results[0] contains the points
    except Exception as e:
        return {"success": False, "error": str(e)}
    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)