from fastapi import FastAPI
from app.db import engine, Base
from app.models import User, Task

app = FastAPI()

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}
