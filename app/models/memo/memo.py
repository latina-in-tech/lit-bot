from models.base.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4


class Memo(Base):

    __tablename__ = 'memos'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    body: Mapped[str] = mapped_column(nullable=False)
    notes: Mapped[str] = mapped_column(nullable=True)
    original_poster: Mapped[int] = mapped_column(nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    user = relationship(argument='User', back_populates='memos', lazy='joined')
    