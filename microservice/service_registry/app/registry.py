# service_registry/registry.py

from fastapi import FastAPI

app = FastAPI()

# Dictionary of services and their base paths
services = {
    "auth_service": {"url": "http://0.0.0.0:8001", "base_path": "/auth"},
    "seller_service": {"url": "http://0.0.0.0:8002", "base_path": "/seller"},
    "task_service": {"url": "http://0.0.0.0:8004", "base_path": "/task"}
}

@app.get("/services")
async def get_services():
    return services
