from fastapi import FastAPI, UploadFile, File

app = FastAPI()


@app.post("/file/upload-bytes")
def upload_file_bytes(file_bytes: bytes = File()):
    return {'file_bytes': str(file_bytes)}


@app.post("/file/upload-file")
def upload_file(file: UploadFile):
    return file