from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from backend.db_depends import get_db
from typing import Annotated
from app.models import User
from app.schemas import CreateUser, UpdateUser
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])

from app.models import Task

@router.get("/{user_id}/tasks")
async def tasks_by_user_id(user_id: int, db: Annotated[Session, Depends(get_db)]):
    """Возвращает все задачи конкретного пользователя по user_id."""
    tasks = db.execute(select(Task).where(Task.user_id == user_id)).scalars().all()
    return tasks

@router.delete("/delete/{user_id}")
async def delete_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    """Удаляет пользователя по user_id и все связанные задачи."""
    # Сначала удаляем все задачи пользователя
    db.execute(delete(Task).where(Task.user_id == user_id))
    db.commit()

    # Теперь удаляем пользователя
    stmt = delete(User).where(User.id == user_id)
    result = db.execute(stmt)
    db.commit()

    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="User was not found")

    return {'status_code': status.HTTP_200_OK, 'transaction': 'User deleted successfully!'}

