from pydantic import EmailStr
from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Identity, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)

from .core_types import UIDType


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'


class User(Base):
    user_id: Mapped[UIDType] = mapped_column(BigInteger, Identity(always=True, cycle=True), primary_key=True)
    email: Mapped[EmailStr] = mapped_column(
        String(100),
        CheckConstraint("email ~ ''^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+.[A-Z|a-z]{2,}$''"),
        unique=True,
        comment='User email',
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='User is active status',
    )
    is_admin: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        comment='User is admin status',
    )
    password: Mapped[str] = mapped_column(
        String(256),
        comment='User password',
    )

    profile: Mapped['Profile'] = relationship(
        'Profile', uselist=False, back_populates='user'
    )


class Profile(Base):
    user_id: Mapped[UIDType] = mapped_column(
        ForeignKey('users.user_id', ondelete='CASCADE'),
        primary_key=True
    )    
    first_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    last_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )
    user: Mapped['User'] = relationship(
        'User',
        back_populates='profile'
    )
