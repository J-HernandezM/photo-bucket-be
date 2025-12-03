from fastapi import APIRouter

from app.dependencies import TransactionDep
from app.models.photo import Photo
from app.schemas.photo import PhotoRead


router = APIRouter()


@router.get(
    "/",
    response_model=PhotoRead,
)
async def get_photos(db: TransactionDep):
    result = await db.get(Photo, 3)
    return result
