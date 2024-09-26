from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api_v1.endpoints import auth, user, default, lookup, req_branding_elements_type, request_type, branding_elements_type, request, branding_element
from app.logging_config import setup_logging
from fastapi.exceptions import RequestValidationError
from app.exceptions.exception_handlers import validation_exception_handler

# API description
description=    """
This FastAPI-based Python application serves as the backend for the Lion Brewery (Ceylon) PLC Outlet System, enabling seamless 
management of outlet data. It offers a set of CRUD (Create, Read, Update, Delete) operations that interact with an MS SQL database to 
handle essential tasks related to brewery outlets. The API allows users to perform a range of operations, including but not limited to 
adding new outlets, retrieving outlet details, updating information, and managing users, ensuring efficient and secure data management.

## Authentication

This API uses JSON Web Token (JWT) authentication to ensure secure access to the Lion Brewery (Ceylon) PLC Outlet System. Users must 
provide valid credentials to obtain a JWT, which will be sent to their registered email. This token is then used to authenticate 
subsequent API requests, passed in the Authorization header as a Bearer token. JWT authentication provides a secure and reliable method 
to verify user identity and manage access to protected resources, ensuring that only authorized users can perform the relevant actions.

## Errors

The Lion Brewery (Ceylon) PLC Outlet System API uses conventional HTTP response codes to indicate the success or failure of an API request. In general:

- Codes in the **2xx** range indicate success.
- Codes in the **4xx** range indicate an error due to issues with the information provided (e.g., missing parameters or invalid authentication).
- Codes in the **5xx** range indicate an error with the server.

Some **4xx** errors may include additional information to help identify and resolve specific issues.

Below are the error codes that may be encountered when using the API:

| HTTP Status Code | Summary                            | Description                             |
| ---------------- | ---------------------------------- | --------------------------------------- |
| **200**          | OK                                 | Everything worked as expected.          |
| **400**          | Bad Request                        | The request was unacceptable, often due to missing a required parameter. |
| **401**          | Unauthorized                       | No valid API key provided.              |
| **403**          | Forbidden                          | The API key doesn’t have permissions to perform the request. |
| **404**          | Not Found                          | The requested resource doesn’t exist.   |
| **500**          | Internal Server Error              | Something went wrong on the server end. |
"""

tags_metadata = [
    {
        "name": "Default",
        "description": """Covers general management operations within the API. This tag includes endpoints and functionalities for 
        handling everyday tasks related to the system's core operations.""",
    },
    {
        "name": "Authentication",
        "description": """Encompasses operations related to user authentication. This tag includes endpoints for login and other 
        authentication processes, ensuring secure access and session management for users.""",
    },
    {
        "name": "User",
        "description": """Contains operations specifically related to user management. This tag covers endpoints for creating, 
        updating, and retrieving user accounts, as well as other user-specific functionalities.""",
    },
    {
        "name": "Lookup",
        "description": """Contains operations related to lookup data management. This tag covers endpoints for creating, 
        updating, and retrieving lookup data.""",
    },
    {
        "name": "Request Branding Elements Type",
        "description": """Contains operations related to request branding elements type data management. This tag covers endpoints for 
        creating, updating, and retrieving request branding elements type data.""",
    },
    {
        "name": "Request Type",
        "description": """Contains operations related to request type data management. This tag covers endpoints for 
        creating, updating, and retrieving request type data.""",
    },
    {
        "name": "Branding Elements Type",
        "description": """Contains operations related to branding elements type data management. This tag covers endpoints for 
        creating, updating, and retrieving branding elements type data.""",
    },
    {
        "name": "Request",
        "description": """Contains operations related to request data management. This tag covers endpoints for 
        creating, updating, and retrieving request data.""",
    },
    {
        "name": "Branding Element",
        "description": """Contains operations related to branding element data management. This tag covers endpoints for 
        creating, updating, and retrieving branding element data.""",
    },
]

# Initialize FastAPI application
app = FastAPI(
    title="Lion Brewery (Ceylon) PLC Outlet System API Endpoints",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Lowcode Minds Technology Pvt Ltd",
        "email": "contact@lowcodeminds.com",
    }
)

# Add CORS (Cross-Origin Resource Sharing) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",  # Replace with specific domain(s) for security in production
        "https://<FLUTTERFLOW_APP>.com",
        "https://<POWERAPPS>.com"
    ],
    allow_credentials=True,  # Allows cookies and authentication headers
    allow_methods=["GET", "POST", "PUT"],  # Specifies allowed HTTP methods
    allow_headers=["Authorization"],  # Specifies allowed headers
)

# Register the custom exception handler
app.add_exception_handler(RequestValidationError, validation_exception_handler)

# Set up logging configuration
setup_logging()

# Include API routers for different modules
app.include_router(default.router, tags=["Default"])
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])
app.include_router(user.router, prefix="/api/v1/user", tags=["User"])
app.include_router(lookup.router, prefix="/api/v1/lookup", tags=["Lookup"])
app.include_router(req_branding_elements_type.router, prefix="/api/v1/req_branding_elements_type", tags=["Request Branding Elements Type"])
app.include_router(request_type.router, prefix="/api/v1/request_type", tags=["Request Type"])
app.include_router(branding_elements_type.router, prefix="/api/v1/branding_elements_type", tags=["Branding Elements Type"])
app.include_router(request.router, prefix="/api/v1/request", tags=["Request"])
app.include_router(branding_element.router, prefix="/api/v1/branding_element", tags=["Branding Element"])