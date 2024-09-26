from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    # Extract the first error message
    message = exc.errors()[0].get("msg")
    # Return the message only
    return JSONResponse(
        status_code=422,
        content={"message": message}  # Adjust the response structure as needed
    )
