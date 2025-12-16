from abc import ABC, abstractmethod
from pathlib import Path

from aioboto3 import Session

from app.config import settings

logger = settings.logger


class AwsS3ClientInterface(ABC):
    @abstractmethod
    async def upload_file(self, path_to_s3: str, file: Path) -> str:
        """Uploads a file to the s3 bucket and returns it's URI"""
        pass

    @abstractmethod
    async def bulk_upload_file(self, path_to_s3: str, files: list[Path]) -> list[str]:
        """Uploads a group of files to the s3 bucket and return their URI"""
        pass

    @abstractmethod
    async def get_file(self, path_to_s3: str, filename: str) -> str:
        """Fetch a file from the s3 bucket and return it's URI"""


class AwsS3Client(AwsS3ClientInterface):
    def __init__(self, session: Session, bucket: str):
        self._session = session
        self._bucket = bucket

    async def upload_file(self, path_to_s3: str, file: Path):
        prefix = path_to_s3.strip("/")
        key = f"{prefix}/{file.name}" if prefix else file.name

        async with self._session.client(
            "s3",
            endpoint_url=settings.aws_endpoint_url,
            region_name=settings.aws_region,
        ) as s3_client:
            try:
                logger.info(f"Uploading {key} to bucket: {self._bucket}")

                with file.open("rb") as f:
                    await s3_client.upload_fileobj(
                        Fileobj=f, Bucket=self._bucket, Key=key
                    )
                    logger.info("File uploaded successfully")
            except Exception as e:
                logger.error(
                    f"Unable to upload {key} to bucket: {self._bucket} {e} ({type(e)})"
                )
                return ""
        return f"s3://{self._bucket}/{key}"

    async def bulk_upload_file(self, path_to_s3, files):
        return await super().bulk_upload_file(path_to_s3, files)

    async def get_file(self, path_to_s3, filename):
        return await super().get_file(path_to_s3, filename)
