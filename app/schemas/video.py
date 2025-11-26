from datetime import datetime
from pydantic import BaseModel, Field


class VideoRead(BaseModel):
    filename: str = Field(..., description="The original filename of the video")
    duration: int = Field(..., gt=0, description="Duration of the video in seconds")
    size: int = Field(..., gt=0, description="Size of the video in bytes")
    date_taken: datetime = Field(
        ..., description="The date and time the video was taken"
    )
    is_public: bool = Field(..., description="Whether the video is publicly visible")
