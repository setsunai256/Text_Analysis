from fastapi import APIRouter
from app.schemas.request import ExtractRequest
from app.services.extractor import extract_simple

router = APIRouter()

@router.post("/extract")
def extract(req: ExtractRequest):
    return extract_simple(req.text)