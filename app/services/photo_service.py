from fastapi import UploadFile
from app.clients.s3_client import AwsS3ClientInterface
from app.exceptions import ForbiddenError, PhotoNotFound
from app.models.photo import Photo
from app.repositories.photo_repository import PhotoRepositoryInterface
from app.schemas.photo import PhotoCreate, PhotoRead, UserPhotosResponse


class PhotoService:
    def __init__(
        self,
        photo_repository: PhotoRepositoryInterface,
        s3_client: AwsS3ClientInterface,
    ):
        self.photo_repository = photo_repository
        self.s3_client = s3_client

    async def _get_photo_model_by_id(self, id: int) -> Photo:
        photo = await self.photo_repository.get_photo_by_id(id)

        if not photo:
            raise PhotoNotFound()

        return photo

    async def _get_deleted_photo_model_by_id(self, id: int) -> Photo:
        photo = await self.photo_repository.get_deleted_photo_by_id(id)

        if not photo:
            raise PhotoNotFound()

        return photo

    async def _check_user_photo(self, photo_id: int, user_id: int) -> None:
        user_photo = await self.photo_repository.get_user_photo_relation(
            photo_id, user_id
        )
        if not user_photo:
            raise ForbiddenError(
                detail="The requested photo does not belongs to the user"
            )

    async def create_photo(
        self, photo: PhotoCreate, user_id: int, file: UploadFile
    ) -> None:
        # TODO: add user validation later
        path = "mocked/path"  # TODO: define path, probably use user identifier as main folder
        s3_key = await self.s3_client.upload_file(path, file)
        photo_model = Photo(**photo.model_dump(), s3_key=s3_key)

        return await self.photo_repository.create_photo(
            photo=photo_model, user_id=user_id
        )

    async def get_photo_by_id(self, id: int) -> PhotoRead:
        photo = await self._get_photo_model_by_id(id)
        return PhotoRead.model_validate(photo, from_attributes=True)

    async def get_user_photos(
        self, user_id: int, skip: int = 0, limit: int = 10
    ) -> UserPhotosResponse:
        # TODO: add user validation later
        photos, total = await self.photo_repository.get_user_photos(
            user_id=user_id, skip=skip, limit=limit
        )

        if not photos:
            raise PhotoNotFound(
                extra_details=f"No photos were found for user {user_id}"
            )

        photos_schema = [
            PhotoRead.model_validate(photo, from_attributes=True) for photo in photos
        ]

        return UserPhotosResponse(
            photos=photos_schema, total=total, skip=skip, limit=limit
        )

    async def soft_delete_toggle(self, id: int, deleting: bool, user_id: int) -> None:
        photo = await self._get_deleted_photo_model_by_id(id)

        if photo.is_deleted == deleting:
            return

        await self._check_user_photo(id, user_id)
        await self.photo_repository.soft_delete_toggle(id=id, deleting=deleting)

    async def hard_delete_photo(self, id: int, user_id: int) -> None:
        await self._get_deleted_photo_model_by_id(id)
        await self._check_user_photo(id, user_id)
        await self.photo_repository.hard_delete_photo(id)
