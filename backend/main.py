from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.first import router as first_router
from backend.database import create_db_and_tables

from contextlib import asynccontextmanager



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(first_router, prefix="/api")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)



