from abc import ABC, abstractmethod

from app.schemas.photo import PhotoCreate, PhotoRead, UserPhotosResponse
from app.services.photo_service import PhotoService


class PhotoClientInterface(ABC):
    @abstractmethod
    async def create_photo(self, photo: PhotoCreate, user_id: int) -> None:
        """Creates a photo in the database"""
        pass

    @abstractmethod
    async def get_photo_by_id(self, id: int) -> PhotoRead:
        """Gets a photo by its id"""
        pass

    @abstractmethod
    async def get_user_photos(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> UserPhotosResponse:
        """Get all the photos from an user"""
        pass

    @abstractmethod
    async def soft_delete_toggle(self, id: int, deleting: bool, user_id: int) -> None:
        """Mark a photo as to be deleted"""
        pass

    @abstractmethod
    async def hard_delete_photo(self, id: int, user_id: int) -> None:
        """Deletes a photo from the database"""
        pass


class PhotoClient(PhotoClientInterface):
    def __init__(self, photo_service: PhotoService):
        self.photo_service = photo_service

    async def create_photo(self, photo: PhotoCreate, user_id: int) -> None:
        return await self.photo_service.create_photo(photo=photo, user_id=user_id)

    async def get_photo_by_id(self, id: int) -> PhotoRead:
        return await self.photo_service.get_photo_by_id(id=id)

    async def get_user_photos(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> UserPhotosResponse:
        return await self.photo_service.get_user_photos(
            user_id=user_id, skip=skip, limit=limit
        )

    async def soft_delete_toggle(self, id: int, deleting: bool, user_id: int) -> None:
        return await self.photo_service.soft_delete_toggle(
            id=id, deleting=deleting, user_id=user_id
        )

    async def hard_delete_photo(self, id: int, user_id: int) -> None:
        return await self.photo_service.hard_delete_photo(id=id, user_id=user_id)
