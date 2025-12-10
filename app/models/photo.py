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
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False, server_default="false"
    )

    def __repr__(self):
        return (
            f"Photo(id={self.id}, filename='{self.filename}', "
            f"content_type='{self.content_type}', size={self.size}, "
            f"date_taken='{self.date_taken}', is_public={self.is_public})"
        )

    def to_dict(self):
        nullable_fields = []
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
            and key
            and (value is not None or key in nullable_fields)
        }

    @classmethod
    def from_dict(cls, data: dict):
        instance = cls()
        for key, value in data.items():
            if value is not None and hasattr(cls, key):
                setattr(instance, key, value)
        return instance
