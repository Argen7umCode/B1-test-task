import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter
from fastapi.middleware.cors import CORSMiddleware

from handlers import file_router, record_router


router = APIRouter(prefix="/api")
router.include_router(file_router)
router.include_router(record_router)

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(router)

    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)