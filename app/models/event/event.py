from models.base.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4


class Event(Base):

    __tablename__ = 'events'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)
    start_time: Mapped[str] = mapped_column(nullable=False)
    end_time: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=False)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    user = relationship(argument='User', back_populates='events')
    