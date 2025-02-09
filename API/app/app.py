from fastapi import FastAPI, HTTPException
from .schemas import ItemSchema, ResponseSchema
from .services import process_item, get_all_records_service
from .repositories import client
from .error_handlers import AppException
from .decorators import handle_exceptions  # Import the decorator

app = FastAPI()

# Register exception handler
app.add_exception_handler(AppException, AppException.exception_handler)

@app.get("/test")
def test_route():
    """A simple test route to verify the server is running."""
    return {"success": True, "message": "Test success!"}

@app.post("/upload/", response_model=ResponseSchema)
@handle_exceptions(500)  # Apply the decorator to wrap all route functions
def upload_item(item: ItemSchema):
    success = process_item(item)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to save vector")
    return ResponseSchema(success=True, message="Item saved successfully", id=item.id or "generated-id")

@app.get("/records/")
@handle_exceptions(500)  # Apply the decorator to wrap all route functions
def get_all_records():
    """API endpoint to get all records."""
    return get_all_records_service()