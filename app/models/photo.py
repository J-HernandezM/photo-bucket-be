from app.db import Base
from sqlalchemy import String, DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column


class Photo(Base):
    __tablename__ = "photo"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    filename: Mapped[str] = mapped_column(String(128), nullable=False)
    content_type: Mapped[str] = mapped_column(String(32), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    date_taken: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return (
            f"Photo(id={self.id}, filename='{self.filename}', "
            f"content_type='{self.content_type}', size={self.size}, "
            f"date_taken='{self.date_taken}', is_public={self.is_public})"
        )
