from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session


async def get_db_transaction(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AsyncGenerator[AsyncSession]:
    try:
        yield session
        await session.commit()
    finally:
        session.close()


TransactionDep = Annotated[AsyncSession, Depends(get_session)]
