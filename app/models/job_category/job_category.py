from models.base.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class JobCategory(Base):

    __tablename__ = 'job_categories'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    jobs = relationship('Job', back_populates='job_category')