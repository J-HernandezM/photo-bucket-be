from datetime import datetime
from fastapi import APIRouter

from app.schemas.photo import PhotoRead


router = APIRouter()


@router.get(
    "/",
    response_model=PhotoRead,
)
async def get_photos():
    dummy_photo = PhotoRead(
        filename="test_file.jpg",
        content_type="jpg",
        size=500,
        date_taken=datetime.now(),
        is_public=True,
    )
    return dummy_photo
