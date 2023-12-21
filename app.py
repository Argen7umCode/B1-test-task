import uvicorn
from fastapi import FastAPI

from handlers import file_router, record_router


app = FastAPI()
app.include_router(file_router)
app.include_router(record_router)


    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)