from models.base.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4

# Docs:
# https://docs.python-telegram-bot.org/en/stable/telegram.user.html


class User(Base):

    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    telegram_id: Mapped[int] = mapped_column(nullable=False)
    role_id: Mapped[int] = mapped_column(ForeignKey('user_roles.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    user_role = relationship('UserRole', back_populates='users')
