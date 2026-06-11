# auth_service/routes.py

from typing import Collection
from fastapi import APIRouter, Depends, HTTPException, Query, status
from passlib.hash import bcrypt
from pydantic import BaseModel, EmailStr
from pymongo import MongoClient
from .models import User
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# client = MongoClient("mongodb://mongo:27020/")
client = MongoClient("mongodb://localhost:27017/")
db = client["ms_auth_db"]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
auth_router = APIRouter()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@auth_router.post("/login")
async def login(user: User):
    user_data = db["users"].find_one({"username": user.username})
    if user_data and bcrypt.verify(user.password, user_data["password"]):
        token = create_access_token(data={"sub": user.username})
        return {"access_token": token, "token_type": "bearer"}
    raise HTTPException(status_code=401, detail="Invalid credentials")


# Pydantic models
class UserRegister(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: str
    username: str
    email: EmailStr

# Utility functions
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def is_email_registered(email: str) -> bool:
    return db["users"].find_one({"email": email}) is not None


# Register route
@auth_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister):
    # Check if email is already registered
    if is_email_registered(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Insert user into the database
    new_user = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
    }
    result = db["users"].insert_one(new_user)

    # Return response
    return UserResponse(
        id=str(result.inserted_id),
        username=user.username,
        email=user.email,
    )


@staticmethod
def serialize_document(document):
    """ Convert MongoDB document to serializable format """
    if '_id' in document:
        document['_id'] = str(document['_id'])
    return document

@auth_router.get("/list", summary="Get the list of users")
async def get_users():

    cursor = db["users"].find()

    result = [serialize_document(doc) for doc in cursor]
    return result
    

    # # Serialize ObjectId to string
    # for user in users:
    #     user["_id"] = str(user["_id"])
    # return {"users": users, "count": len(users)}
