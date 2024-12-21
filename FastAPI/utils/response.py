from typing import Any
from fastapi.responses import JSONResponse

def create_response(status_code: int, message: str, data: Any = None):
    """
    Standardized response format for the API.
    Args:
        status_code: HTTP status code for the response
        message: Message describing the result (e.g., success or error)
        data: Data to be included in the response body (optional)
    """
    response_content = {"message": message}
    if data is not None:
        response_content["data"] = data
    
    return JSONResponse(status_code=status_code, content=response_content)