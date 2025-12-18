from typing import Optional
from fastapi import APIRouter, Body, File, Path, Query, UploadFile

from app.dependencies import PhotoClientDep
from app.schemas.photo import (
    PhotoCreate,
    PhotoCreateResponse,
    PhotoDeleteResponse,
    PhotoDeleteSoft,
    PhotoRead,
    UserPhotosResponse,
)


router = APIRouter()


@router.post("/", response_model=PhotoCreateResponse)
async def create_photo(
    photo_client: PhotoClientDep,
    payload: PhotoCreate = Body(...),
    file: UploadFile = File(...),
):
    user_id = 1  # TODO: update mocked user id
    await photo_client.create_photo(photo=payload, user_id=user_id, file=file)
    return PhotoCreateResponse(description="Photo created successfully")


@router.get("/", response_model=UserPhotosResponse)
async def get_user_photos(
    photo_client: PhotoClientDep,
    skip: Optional[int] = Query(0, description="Offset used for pagination"),
    limit: Optional[int] = Query(10, description="Number of photos per page"),
):
    user_id = 1  # TODO: update mocked user id
    response = await photo_client.get_user_photos(
        user_id=user_id, skip=skip, limit=limit
    )
    return response


@router.get("/{id}", response_model=PhotoRead)
async def get_photo_by_id(
    photo_client: PhotoClientDep, id: int = Path(..., description="Photo ID")
):
    photo = await photo_client.get_photo_by_id(id=id)
    return photo


@router.patch("/{id}/soft", response_model=PhotoDeleteResponse)
async def soft_delete_toggle(
    photo_client: PhotoClientDep,
    id: int = Path(..., description="Photo ID"),
    payload: PhotoDeleteSoft = Body(...),
):
    user_id = 1  # TODO: update mocked user id
    deleting = payload.deleting
    await photo_client.soft_delete_toggle(id=id, deleting=deleting, user_id=user_id)
    return PhotoDeleteResponse(
        description=f"Photo {"un" if not deleting else ""}marked for deletion successfully"
    )


@router.delete("/{id}/hard", response_model=PhotoDeleteResponse)
async def hard_delete_photo(
    photo_client: PhotoClientDep, id: int = Path(..., description="Photo ID")
):
    user_id = 1  # TODO: update mocked user id
    await photo_client.hard_delete_photo(id=id, user_id=user_id)
    return PhotoDeleteResponse(description="Photo permanently deleted")
