from models.base.base import Base
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4


class Job(Base):

    __tablename__ = 'jobs'

    id: Mapped[UUID] = mapped_column(primary_key=True, nullable=False, default=uuid4)
    contract_type_id: Mapped[int] = mapped_column(ForeignKey('contract_types.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('job_categories.id'), nullable=False)
    position: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    link: Mapped[str] = mapped_column(nullable=True)
    ral: Mapped[int] = mapped_column(nullable=True)
    created_by: Mapped[UUID] = mapped_column(ForeignKey('users.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(nullable=True)

    contract_type = relationship('ContractType', back_populates='jobs')
    job_category = relationship('JobCategory', back_populates='jobs')
    user = relationship(argument='User', back_populates='jobs', lazy='joined')
    