from models.base.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class ContractType(Base):

    __tablename__ = 'contract_types'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    jobs = relationship('Job', back_populates='contract_type')