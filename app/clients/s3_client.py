from abc import ABC, abstractmethod
import asyncio
from pathlib import Path

from aioboto3 import Session
from types_aiobotocore_s3 import S3Client

from app.config import settings

logger = settings.logger


class AwsS3ClientInterface(ABC):
    @abstractmethod
    async def upload_file(self, path_to_s3: str, file: Path) -> str:
        """Uploads a file to the s3 bucket and returns it's URI"""
        pass

    @abstractmethod
    async def bulk_upload_file(self, path_to_s3: str, files: list[Path]) -> list[str]:
        """Uploads a group of files to the s3 bucket and return a list containing the UIR or an empty string for failed uploads"""
        pass

    @abstractmethod
    async def get_file_presigned_url(self, path_to_s3: str, filename: str) -> str:
        """Fetch a file from the s3 bucket and return it's URI"""


class AwsS3Client(AwsS3ClientInterface):
    def __init__(
        self, session: Session, bucket: str, presigned_expiration_in_seconds: int = 3600
    ):
        self._session = session
        self._bucket = bucket
        self._expiration = presigned_expiration_in_seconds

    async def _upload_file(
        self, path_to_s3: str, file: Path, s3_client: S3Client
    ) -> str:
        prefix = path_to_s3.strip("/")
        key = f"{prefix}/{file.name}" if prefix else file.name

        try:
            logger.info(f"Uploading {key} to bucket: {self._bucket}")

            with file.open("rb") as f:
                await s3_client.upload_fileobj(Fileobj=f, Bucket=self._bucket, Key=key)
                logger.info("File uploaded successfully")
        except Exception as e:
            logger.error(
                f"Unable to upload {key} to bucket: {self._bucket} {e} ({type(e)})"
            )
            return ""

        return f"s3://{self._bucket}/{key}"

    async def upload_file(self, path_to_s3: str, file: Path) -> str:
        async with self._session.client(
            "s3",
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
        ) as s3_client:
            urn = await self._upload_file(path_to_s3, file=file, s3_client=s3_client)
        return urn

    async def bulk_upload_file(self, path_to_s3: str, files: list[Path]) -> list[str]:
        async with self._session.client(
            "s3",
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
        ) as s3_client:
            tasks = [
                self._upload_file(path_to_s3=path_to_s3, file=f, s3_client=s3_client)
                for f in files
            ]
            uris = await asyncio.gather(*tasks)

        return uris

    async def get_file_presigned_url(self, path_to_s3: str, filename: str):
        prefix = path_to_s3.strip("/")
        key = f"{prefix}/{filename}" if prefix else filename

        async with self._session.client(
            "s3",
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
        ) as s3_client:
            try:
                url = await s3_client.generate_presigned_url(
                    "get_object",
                    Params={"Bucket": self._bucket, "Key": key},
                    ExpiresIn=self._expiration,
                )

                return url
            except Exception as e:
                logger.error(f"Error while getting the object: {key}")
                raise e
