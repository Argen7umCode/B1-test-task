from parser_1 import Parser

from fastapi import FastAPI, UploadFile
import aiofiles

app = FastAPI()
parser = Parser()


@app.post("/file/upload-file")
async def upload_file(file: UploadFile):
    file_path = f'files/{file.filename}'
    async with aiofiles.open(file_path, 'wb') as saved_file:
        content = await file.read()
        await saved_file.write(content)

    dfs = parser.get_classes_from_excel_file(file_path)
    print(dfs[0])