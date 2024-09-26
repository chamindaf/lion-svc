from pydantic import BaseModel

class AppInfo(BaseModel):
    application_name: str
    version: str
    description: str