# api_gateway/main.py

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.security import HTTPBearer
import httpx
import jwt  # Ensure PyJWT is installed
from jwt import PyJWTError

app = FastAPI()

SERVICE_REGISTRY_URL = "http://localhost:8003/services"
SECRET_KEY = "mysecret"  # Replace with a secure key
ALGORITHM = "HS256"
WHITELISTED_PATHS = ["/auth/login", "/auth/register"]

# Bearer token dependency
security = HTTPBearer()

# Fetch services dynamically from the registry
async def fetch_services():
    async with httpx.AsyncClient() as client:
        response = await client.get(SERVICE_REGISTRY_URL)
        return response.json()

async def authorize(request: Request):
    if any(request.url.path.startswith(path) for path in WHITELISTED_PATHS):
        return None

    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=401, detail="Token missing")

    try:
        payload = jwt.decode(token.split(" ")[1], SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Token invalid or expired")

@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy(full_path: str, request: Request, payload=Depends(authorize)):
    print(f"full_path: {full_path}")
    print(f"request.url.path: {request.url.path}")
    services = await fetch_services()
    print(f"services: {services}")
    # Determine the service based on the URL path
    matched_service = None
    for service in services.values():
        if request.url.path.startswith(service["base_path"]):
            matched_service = service["url"]
            break
    
    print(f"matched_service: {matched_service}")

    if not matched_service:
        raise HTTPException(status_code=404, detail="Service not found")

    # Forward the request to the matched service
    # target_url = f"{matched_service}/{full_path}"
    # print(f"target_url: {target_url}")

    stripped_path = "/".join(full_path.split("/")[1:])

    # Build the target URL
    target_url = f"{matched_service}/{stripped_path}"
    print(f"target_url: {target_url}")

    print(f"request.method: {request.method}")

    headers = {key.decode(): value.decode() for key, value in request.headers.raw}
    headers.pop("content-length", None)

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.query_params,
            # json=await request.json()
            json=await request.json() if request.method in ["POST", "PUT"] else None,
        )
    return response.json()
