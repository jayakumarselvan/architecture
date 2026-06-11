```bash

python3 -m venv .venv

source .venv/bin/activate

pip install -r api_gateway/requirements.txt \
            -r auth_service/requirements.txt \
            -r seller_service/requirements.txt \
            -r service_registry/requirements.txt \
            -r task_service/requirements.txt
```

api_gateway
```
cd api_gateway
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
service_registry

```
cd service_registry
uvicorn app.registry:app --host 0.0.0.0 --port 8003
```

auth_service
```
cd auth_service
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

seller_service
```
cd seller_service
uvicorn app.main:app --host 0.0.0.0 --port 8002
```


task-service
```
cd task_service
uvicorn app.main:app --host 0.0.0.0 --port 8004
```