from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import Database


class BaseSQLAlchemyPostegres:
    def __init__(
        self,
    ):
        super().__init__()
        self.session: AsyncSession = Depends(Database().get_session)
