from pydantic import EmailStr
from sqlalchemy import BigInteger, Boolean, CheckConstraint, ForeignKey, Identity, String
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True, cycle=True), primary_key=True
    )

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}s'


class User(Base):
    email: Mapped[EmailStr] = mapped_column(
        String(100),
        CheckConstraint("email ~ ''^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$''"),
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


class UserRelationMixin:
    _user_id_nullable: bool = False
    _user_id_unique: bool = False
    _user_back_populates: str | None = None

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            ForeignKey('users.id'),
            unique=cls._user_id_unique,
            nullable=cls._user_id_nullable,
        )

    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship(
            'User',
            back_populates=cls._user_back_populates,
        )


class Profile(Base, UserRelationMixin):
    _user_id_unique: bool = True
    _user_id_nullable: bool = False
    _user_back_populates: str = 'profile'

    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
