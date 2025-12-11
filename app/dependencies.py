from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.clients.photo_client import PhotoClient, PhotoClientInterface
from app.db import get_session
from app.repositories.photo_repository import PhotoRepository, PhotoRepositoryInterface
from app.services.photo_service import PhotoService


async def get_db_transaction(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[AsyncSession]:
    try:
        yield session
        await session.commit()
    finally:
        await session.close()


TransactionDep = Annotated[AsyncSession, Depends(get_db_transaction)]


async def get_photo_repository(session: TransactionDep) -> PhotoRepositoryInterface:
    return PhotoRepository(session=session)


async def get_photo_service(
    repo: Annotated[PhotoRepositoryInterface, Depends(get_photo_repository)],
) -> PhotoService:
    return PhotoService(photo_repository=repo)


async def get_photo_client(
    service: Annotated[PhotoService, Depends(get_photo_service)],
) -> PhotoClientInterface:
    return PhotoClient(photo_service=service)


PhotoClientDep = Annotated[PhotoClientInterface, Depends(get_photo_client)]
