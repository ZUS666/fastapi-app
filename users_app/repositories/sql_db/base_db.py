from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from users_app.repositories.sql_db.session import Database


class BaseSQLAlchemyPostegres:
    def __init__(
        self,
    ):
        super().__init__()
        self.session: AsyncSession = Depends(Database().get_session)
