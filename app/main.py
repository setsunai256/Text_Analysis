from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Text Analysis API",
    description="API для извлечения сущностей из текста",
    version="1.0"
)

app.include_router(router)