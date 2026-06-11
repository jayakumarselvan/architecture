from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import Optional

import jwt

from app.models.tasks.pydantic_model import TaskCreateUpdateRequest, TaskPatchUpdateRequest
from app.services.tasks.task import TaskService

router = APIRouter()

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

# Function to verify the token and extract the user information
async def verify_token(request: Request):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        # Decode the JWT token
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # This will contain the user's information (e.g., username)
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")


@router.get("/")
def home():
    return {"message": "Welcome to Task Management Portal"}


@router.post('/add-or-update', status_code=201)
@router.post('/add-or-update/{user_id}', status_code=200)
async def add_or_update(request: TaskCreateUpdateRequest, task_id: Optional[str] = None, payload=Depends(verify_token)):
    try:
        requester_id = payload.get("sub")
        task_data = request.model_dump()
        task_service = TaskService()
        result = task_service.add_or_update(task_data, task_id, requester_id)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


@router.get('/list')
async def list_user(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), payload=Depends(verify_token)):
    try:
        task_service = TaskService()
        result = task_service.list_task(skip=skip, limit=limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


@router.patch("/patch-update/{task_id}", status_code=200)
async def patch_update(task_id, update_data: dict, payload=Depends(verify_token)):
    try:
        requester_id = payload.get("sub")
        task_service = TaskService()
        result = task_service.patch_update(str(task_id), update_data, requester_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))


@router.delete('/{task_id}')
async def delete_user(task_id: str, payload=Depends(verify_token)):
    try:
        task_service = TaskService()
        result = task_service.delete_task(task_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="An unexpected error occurred: " + str(e))
