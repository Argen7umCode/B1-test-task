from parser_1 import Parser
from db.session import init_db, get_db
from db.models import Class

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, FastAPI, UploadFile
import aiofiles

app = FastAPI()
parser = Parser()



@app.post("/file/upload-file")
async def upload_file(file: UploadFile, db: AsyncSession = Depends(get_db)):
    print(db)
    file_path = f'files/{file.filename}'
    async with aiofiles.open(file_path, 'wb') as saved_file:
        content = await file.read()
        await saved_file.write(content)
    try:
        dfs = parser.get_classes_from_excel_file(file_path)
    except :
        pass
    print(dfs[0])