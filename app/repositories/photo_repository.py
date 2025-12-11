from abc import ABC, abstractmethod
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.photo import Photo
from app.models.user_photo import UserPhoto


class PhotoRepositoryInterface(ABC):

    @abstractmethod
    async def create_photo(self, photo: Photo, user_id: int) -> None:
        """Creates a new photo"""
        pass

    @abstractmethod
    async def get_photo_by_id(self, id: int) -> Photo:
        """Get a photo by its id"""
        pass

    @abstractmethod
    async def get_deleted_photo_by_id(self, id: int) -> Photo:
        """Gets any photo by its id even if deleted"""
        pass

    @abstractmethod
    async def get_user_photo_relation(self, photo_id: int, user_id: int) -> UserPhoto:
        """Gets a user_photo relation by both photo_id and user_id"""
        pass

    @abstractmethod
    async def get_user_photos(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Photo], int]:
        """Gets a list of photos for a given user"""
        pass

    @abstractmethod
    async def soft_delete_toggle(self, id: int, deleting: bool) -> None:
        """Toggles the is_deleted property of a photo"""
        pass

    @abstractmethod
    async def hard_delete_photo(self, id: int) -> None:
        """Deletes a photo"""
        pass


class PhotoRepository(PhotoRepositoryInterface):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _create_user_photo(self, photo_id: int, user_id: int) -> None:
        user_photo = UserPhoto(photo_id=photo_id, user_id=user_id)
        self.session.add(user_photo)
        await self.session.flush()

    async def create_photo(self, photo: Photo, user_id: int) -> None:
        self.session.add(photo)
        await self.session.flush()
        await self._create_user_photo(photo_id=photo.id, user_id=user_id)

    async def get_photo_by_id(self, id: int) -> Photo:
        stmt = select(Photo).where(
            Photo.id == id,
            Photo.is_public == True,  # NOQA: E712
            Photo.is_deleted == False,  # NOQA: E712
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_deleted_photo_by_id(self, id: int) -> Photo:
        stmt = select(Photo).where(
            Photo.id == id,
        )
        result = await self.session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_user_photo_relation(self, photo_id: int, user_id: int) -> UserPhoto:
        stmt = select(UserPhoto).where(
            UserPhoto.photo_id == photo_id, UserPhoto.user_id == user_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_photos(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> tuple[list[Photo], int]:
        data_stmt = (
            select(Photo)
            .join(UserPhoto, UserPhoto.photo_id == Photo.id)
            .where(
                UserPhoto.user_id == user_id, Photo.is_deleted == False  # NOQA: E712
            )
            .offset(skip)
            .limit(limit)
        )
        data_result = await self.session.execute(data_stmt)
        photos = list(data_result.scalars().all())

        count_stmt = (
            select(func.count())
            .select_from(Photo)
            .join(UserPhoto, UserPhoto.photo_id == Photo.id)
            .where(
                UserPhoto.user_id == user_id, Photo.is_deleted == False  # NOQA: E712
            )
        )
        total_result = await self.session.execute(count_stmt)
        total = total_result.scalar_one_or_none()

        return photos, total

    async def soft_delete_toggle(self, id: int, deleting: bool) -> None:
        stmt = update(Photo).values(is_deleted=deleting).where(Photo.id == id)
        await self.session.execute(stmt)

    async def hard_delete_photo(self, id: int) -> None:
        stmt_1 = delete(UserPhoto).where(UserPhoto.photo_id == id)
        stmt_2 = delete(Photo).where(Photo.id == id)
        await self.session.execute(stmt_1)
        await self.session.execute(stmt_2)
