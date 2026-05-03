from fastapi import FastAPI
from app.api.routes import router
from app.services.llm_service import warmup


app = FastAPI(
    title="Text Analysis API",
    version="1.0"
)

app.include_router(router)

@app.on_event("startup")
def startup_event():
    warmup()