from models.base.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserRole(Base):

    __tablename__ = 'user_roles'

    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)

    users = relationship('User', back_populates='user_role')