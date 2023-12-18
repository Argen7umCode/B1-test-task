from parser_1 import Parser
from db.session import get_db
from db.models import Base, Class, InputBalance, Turnover, Record
from schemas.record import RecordSchema
from typing import Union, List

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from fastapi import Depends, FastAPI, UploadFile
import aiofiles


app = FastAPI()
parser = Parser()

class DAL:
    def __init__(self, db_session: AsyncSession) -> None:
        self.db_session = db_session

    async def make_query_and_get_all(self, query) -> Union[Base, None]:
        res = await self.db_session.execute(query)
        row = res.fetchall()
        if row is not None:
            return row     

    async def make_query_and_get_one(self, query) -> Union[Base, None]:
        res = await self.db_session.execute(query)
        row = res.fetchone()
        if row is not None:
            return row     
    
    async def add_all(self, rows: List[Base]) -> List[Base]:
        await self.db_session.add_all(rows)
        return rows


async def process_class(class_: str, 
                        df: pd.DataFrame, 
                        session: AsyncSession):
    dal = DAL(session)
    
    class_select_query = select(Class).where(Class.description == class_)
    class_ = await dal.make_query_and_get_one(class_select_query)

    to_add = []
    for row in df[['unid', 'active', 'passive', 'debit', 'credit']].to_numpy():
        unid, active, passive, debit, credit = row
        input_balance = InputBalance(active, 
                                     passive) 
        turnover = Turnover(debit, 
                            credit)
        record = Record(unid=unid, 
                        input_balance=input_balance, 
                        tunrover=turnover, 
                        class_=class_)
        to_add.extend([input_balance, turnover, record])
    await dal.add_all(to_add)
    return to_add[2::3]


@app.post("/file/upload-file")
async def upload_file(file: UploadFile, session: AsyncSession = Depends(get_db)):
    file_path = f'files/{file.filename}'
    async with aiofiles.open(file_path, 'wb') as saved_file:
        content = await file.read()
        await saved_file.write(content)
    
    classes = parser.get_classes_from_excel_file(file_path)

    try:
        pass      
    except Exception as e:
        print(e)
        return None
    
    for class_, df in classes.items():
        await process_class(class_, df, session)
        break
