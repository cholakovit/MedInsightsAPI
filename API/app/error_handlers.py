from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    """Unified exception handling for the entire application."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

    @staticmethod
    async def exception_handler(request: Request, exc: "AppException"):
        """Handles all AppException errors and returns a JSON response."""
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "error": exc.message}
        )

    @classmethod
    def create(cls, message: str, status_code: int = 500):
        """Factory method to dynamically create exceptions with any status code."""
        return cls(message, status_code)
    
