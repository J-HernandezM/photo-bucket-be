from pydantic import BaseModel, Field


class UserRead(BaseModel):
    id: str = Field(..., description="User ID")
    username: str = Field(..., description="Username")
    email: str = Field(..., description="User email")
    hash: str = Field(..., description="User password hash")
    salt: str = Field(..., description="User password salt")
