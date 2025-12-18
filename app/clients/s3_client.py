from abc import ABC, abstractmethod
import asyncio
from contextlib import asynccontextmanager

from aioboto3 import Session
from fastapi import UploadFile
from types_aiobotocore_s3 import S3Client

from app.config import settings

logger = settings.logger


class AwsS3ClientInterface(ABC):
    @abstractmethod
    async def upload_file(self, path_to_s3: str, file: UploadFile) -> str:
        """Uploads a file to the s3 bucket and returns it's S3 key"""
        pass

    @abstractmethod
    async def bulk_upload_file(
        self, path_to_s3: str, files: list[UploadFile]
    ) -> list[str]:
        """Uploads a group of files to the s3 bucket and return a list containing the S3 keys or an empty string for failed uploads"""
        pass

    @abstractmethod
    async def get_file_presigned_url(self, key: str) -> str:
        """Fetch a file from the s3 bucket and return a presigned URL"""


class AwsS3Client(AwsS3ClientInterface):
    def __init__(self, session: Session, bucket: str):
        self._session = session
        self._bucket = bucket

    @asynccontextmanager
    async def _get_client(self):
        """Reusable client context manager"""
        async with self._session.client(
            "s3",
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
        ) as client:
            yield client

    async def _upload_file(
        self, path_to_s3: str, file: UploadFile, s3_client: S3Client
    ) -> str:
        prefix = path_to_s3.strip("/")
        key = f"{prefix}/{file.filename}" if prefix else file.filename
        content_type = file.content_type
        file_obj = file.file
        extra = {"ContentType": content_type} if content_type else None

        try:
            logger.info(f"Uploading {key} to bucket: {self._bucket}")

            await s3_client.upload_fileobj(
                Fileobj=file_obj, Bucket=self._bucket, Key=key, ExtraArgs=extra
            )
            logger.info("File uploaded successfully")
        except Exception as e:
            logger.error(
                f"Unable to upload {key} to bucket: {self._bucket} {e} ({type(e)})"
            )
            return ""

        return key

    async def upload_file(self, path_to_s3: str, file: UploadFile) -> str:
        async with self._get_client() as s3_client:
            s3_path = await self._upload_file(
                path_to_s3, file=file, s3_client=s3_client
            )
        return s3_path

    async def bulk_upload_file(
        self, path_to_s3: str, files: list[UploadFile]
    ) -> list[str]:
        async with self._get_client() as s3_client:
            tasks = [
                self._upload_file(path_to_s3=path_to_s3, file=f, s3_client=s3_client)
                for f in files
            ]
            s3_paths = await asyncio.gather(*tasks)

        return s3_paths

    async def get_file_presigned_url(self, key: str, expiration: int = 3600):
        async with self._get_client() as s3_client:
            try:
                url = await s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self._bucket, "Key": key},
                    ExpiresIn=expiration,
                )

                return url
            except Exception as e:
                logger.error(f"Error while getting the object: {key}")
                raise e
