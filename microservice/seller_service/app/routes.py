# seller_service/routes.py

from fastapi import APIRouter, HTTPException, Request, Depends
from pymongo import MongoClient
from .models import Item
import jwt

SECRET_KEY = "mysecret"
ALGORITHM = "HS256"

# client = MongoClient("mongodb://mongo:27020/")
client = MongoClient("mongodb://localhost:27017/")
db = client["ms_seller_db"]

seller_router = APIRouter()

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

# Endpoint to create an item with "created_by" information
@seller_router.post("/item")
async def create_item(item: Item, payload=Depends(verify_token)):
    # Extract the username from the token payload
    created_by = payload.get("sub")  # Assuming the username is stored in the "sub" field

    # Add the created_by field to the item data
    item_data = item.dict()
    item_data["created_by"] = created_by  # Add the creator's information

    # Insert the item data into the database
    item_id = db["items"].insert_one(item_data).inserted_id
    return {"message": "Item created", "item_id": str(item_id), "created_by": created_by}
