from typing import List, Union
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base


class DAL:
    # Класс который инкапсулирует взаимодействие с базой данных
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def make_query_and_get_all(self, query) -> Union[Base, None]:
        res = await self.db_session.execute(query)
        row = res.all()
        if row is not None:
            return row     

    async def make_query_and_get_one(self, query) -> Union[Base, None]:
        res = await self.db_session.execute(query)
        row = res.first()
        if row is not None:
            return row[0]
    
    async def add_all(self, rows: List[Base]) -> List[Base]:
        self.db_session.add_all(rows)
        return rows

    async def add_one(self, rows: List[Base]) -> List[Base]:
        self.db_session.add(rows)
        return rows