from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

from app.api.routers import photos_router, users_router, videos_router
from app.config import settings

app = FastAPI()

app.include_router(users_router.router, prefix="/users", tags=["users"])
app.include_router(photos_router.router, prefix="/photos", tags=["photos"])
app.include_router(videos_router.router, prefix="/videos", tags=["videos"])


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


@app.get("/")
async def read_root_test():
    return {"Hello": "World"}


@app.get("/info")
async def get_info():
    return {
        "1": settings.database_url,
        "2": settings.pg_dbname,
        "3": settings.pg_password,
        "4": settings.pg_user,
    }
    pass


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
