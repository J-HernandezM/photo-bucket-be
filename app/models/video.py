from app.db import Base
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Video(Base):
    __tablename__ = "video"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(128), nullable=False)
    duration: Mapped[int] = mapped_column(Integer, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    date_taken: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return (
            f"Video(id={self.id}, filename='{self.filename}', "
            f"duration='{self.duration}', size={self.size}, "
            f"date_taken='{self.date_taken}', is_public={self.is_public})"
        )
