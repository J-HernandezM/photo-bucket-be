from app.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserPhoto(Base):
    __tablename__ = "user_photo"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    photo_id: Mapped[int] = mapped_column(ForeignKey("photo.id"))

    def __repr__(self):
        return f"UserPhoto(id={self.id} user_id='{self.user_id}' photo_id='{self.photo_id}')"
