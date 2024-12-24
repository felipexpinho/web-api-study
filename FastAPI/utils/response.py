from typing import Optional, Any
from fastapi.responses import JSONResponse

def create_response(status_code: int, message: str, data: Optional[Any] = None) -> JSONResponse:
    """
    Standardized response format for the API.

    Args:
        status_code (int): HTTP status code for the response.
        message (str): Message describing the result (e.g., success or error).
        data (Optional[Any]): Data to be included in the response body.

    Returns:
        JSONResponse: A JSON response object containing the status code, message, 
                      and optional data in the response body.
    """
    response_content = {"message": message}
    if data is not None:
        response_content["data"] = data
    
    return JSONResponse(status_code=status_code, content=response_content)