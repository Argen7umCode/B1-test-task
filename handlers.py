from fastapi.routing import APIRouter
from fastapi import UploadFile, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import aiofiles

from db.session import get_db
from utils.actions import process_class, get_records_from_db
from config import parser, grouper


file_router = APIRouter(prefix='/file', tags=['file'])

@file_router.post("/upload")
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


record_router = APIRouter(prefix='/record', tags=['record'])

@record_router.get("/get")
async def get_records(session: AsyncSession = Depends(get_db)):
    return await get_records_from_db(session)


