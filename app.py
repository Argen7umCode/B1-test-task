from pydantic import BaseModel
import uvicorn
from parser_1 import Parser
from db.session import get_db
from db.models import Base, PaymentClass, Record

from typing import Union, List
from pprint import pprint
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select
from fastapi import Depends, FastAPI, UploadFile
import aiofiles


app = FastAPI()
parser = Parser()


class RecordSchema(BaseModel):
    class_name: str
    unid: int
    active_balance: float
    passive_balance: float
    debit: float
    credit: float



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
            return row[0]  
    
    async def add_all(self, rows: List[Base]) -> List[Base]:
        self.db_session.add_all(rows)
        return rows

    async def add_one(self, rows: List[Base]) -> List[Base]:
        self.db_session.add(rows)
        return rows


async def process_class(payment_class_description: str, 
                        df: pd.DataFrame, 
                        session: AsyncSession) -> List[RecordSchema]:
    async with session.begin():
        dal = DAL(session)

        payment_class_select_query = select(PaymentClass)\
                .where(PaymentClass.description == payment_class_description)
        payment_class = await dal.make_query_and_get_one(payment_class_select_query)
        
        if payment_class is None:
            payment_class = PaymentClass(description=payment_class_description)
            await dal.add_one(payment_class)
        
        to_return = []
        to_add = []
        for row in df[['unid', 'active', 'passive', 'debit', 'credit']].to_numpy():
            unid, active, passive, debit, credit = row
            record = Record(
                        unid=int(unid), 
                        active=active,
                        passive=passive,
                        debit=debit,
                        credit=credit,
                        payment_class=payment_class
                    )
            to_add.append(record)
            to_return.append(
                RecordSchema(
                    class_name=payment_class_description,
                    unid=int(unid),
                    active_balance=active,
                    passive_balance=passive,
                    debit=debit,
                    credit=credit,
                )
            )
        await dal.add_all(to_add)
    return to_return


@app.post("/file/upload-file")
async def upload_file(file: UploadFile, session: AsyncSession = Depends(get_db)):
    file_path = f'files/{file.filename}'
    async with aiofiles.open(file_path, 'wb') as saved_file:
        content = await file.read()
        await saved_file.write(content)
    
    classes = parser.get_classes_from_excel_file(file_path)
    
    added = []
    for payment_class, df in classes.items():
        print(payment_class)
        result = await process_class(payment_class, df, session)
        added.extend(result)
    return added
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)