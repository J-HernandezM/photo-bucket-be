from datetime import datetime
from pydantic import BaseModel, Field


class PhotoRead(BaseModel):
    filename: str = Field(..., description="The original filename of the photo")
    content_type: str = Field(
        ..., description="MIME type of the photo (e.g., 'image/jpeg')"
    )
    size: int = Field(..., gt=0, description="Size of the photo in bytes")
    date_taken: datetime = Field(
        ..., description="The date and time the photo was taken"
    )
    is_public: bool = Field(..., description="Whether the photo is publicly visible")
