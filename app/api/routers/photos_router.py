from fastapi import APIRouter


router = APIRouter()


@router.get("/")
async def get_photos():
    return {"response": "hello photos"}
