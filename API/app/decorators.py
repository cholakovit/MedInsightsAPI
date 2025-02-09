import logging
from functools import wraps
from .error_handlers import AppException

# Ensure the error.log file exists
open("error.log", "a").close()

# Test logging directly
logging.basicConfig(
    filename="app/error.log",  # Explicitly specify path inside `app/`
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

#logger.error("🚀 Test: Logging is working!")

#print("🚀 Test: Logging is working!")  # This should print to console

def handle_exceptions(default_status_code=500):
    """Global Decorator to catch & log all exceptions in FastAPI routes."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = f"\n❌ ERROR in {func.__name__}:\n🔹 STATUS CODE: {default_status_code}\n🔹 MESSAGE: {str(e)}"
                
                # Log the error
                logger.error(error_message, exc_info=True)

                # Print to terminal in readable format
                print("\n======================== ERROR LOG ========================")
                print(error_message)
                print("==========================================================\n")

                raise AppException.create(error_message, default_status_code)
        return wrapper
    return decorator

def auto_handle_exceptions(default_status_code: int = 500):
    """ Automatically applies exception handling and logging to all methods of a class. """
    def class_decorator(cls):
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value) and not attr_name.startswith("__"):
                setattr(cls, attr_name, handle_exceptions(default_status_code)(attr_value))
        return cls
    return class_decorator