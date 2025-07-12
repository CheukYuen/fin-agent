from fastapi import FastAPI
from app.api_router import router

app = FastAPI()
app.include_router(router)
