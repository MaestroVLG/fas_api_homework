from fastapi import FastAPI
from app.db import engine, Base
from app.routers import user

app = FastAPI()

# Создание всех таблиц
Base.metadata.create_all(bind=engine)

# Подключите маршруты
app.include_router(user.router)

@app.get("/")
async def welcome():
    return {"message": "Welcome to Taskmanager"}

