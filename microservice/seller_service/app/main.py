# seller_service/main.py

from fastapi import FastAPI
from .routes import seller_router

app = FastAPI()

app.include_router(seller_router)
