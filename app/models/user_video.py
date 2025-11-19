from app.db import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column


class UserVideo(Base):
    __tablename__ = "user_video"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"))

    def __repr__(self):
        return f"UserV1ideo(id={self.id} user_id='{self.user_id}' video_id='{self.video_id}')"
