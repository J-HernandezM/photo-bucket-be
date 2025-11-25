from app.db import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), nullable=False)
    hash: Mapped[str] = mapped_column(String(256), nullable=False)
    salt: Mapped[str] = mapped_column(String(256), nullable=False)

    def __repr__(self):
        return f"User(id={self.id} username='{self.username}' email='{self.email}' hash='{self.hash}' salt='{self.salt}')"

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
