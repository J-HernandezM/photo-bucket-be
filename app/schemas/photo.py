from datetime import datetime
from pydantic import BaseModel, Field


class BasePhotoRequest(BaseModel):
    filename: str = Field(..., description="The original filename of the photo")
    content_type: str = Field(
        ..., description="MIME type of the photo (e.g., 'image/jpeg')"
    )
    size: int = Field(..., gt=0, description="Size of the photo in bytes")
    date_taken: datetime = Field(
        ..., description="The date and time the photo was taken"
    )
    is_public: bool = Field(..., description="Whether the photo is publicly visible")


class PhotoRead(BasePhotoRequest):
    pass


class PhotoCreate(BasePhotoRequest):
    pass


class UserPhotosResponse(BaseModel):
    photos: list[PhotoRead] = Field(
        ..., description="List of photos in the current page"
    )
    total: int = Field(..., description="Total number of photos available")
    skip: int = Field(..., description="Offset used for pagination")
    limit: int = Field(..., description="Number of photos per page")


class PhotoResponse(BaseModel):
    description: str = Field(..., description="Result of the photo operation")


class PhotoCreateResponse(PhotoResponse):
    pass


class PhotoDeleteResponse(PhotoResponse):
    pass


class PhotoDeleteSoft(BaseModel):
    deleting: bool = Field(
        ..., description="Wether the photo is going to be marked as is_deleted or not"
    )
