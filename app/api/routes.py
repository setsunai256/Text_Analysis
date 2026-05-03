from fastapi import APIRouter, UploadFile, File
from app.services.docx_service import extract_text_from_docx
from app.services.llm_service import extract_entities
from fastapi import HTTPException
from app.schemas.response import ExtractResponse, SafetyResponse, ToolsResponse, DevicesResponse

router = APIRouter()

def validate_file(file: UploadFile):
    # Проверка расширения
    if not file.filename.endswith(".docx"):
        raise HTTPException(
            status_code=400,
            detail="Only .docx files are allowed"
        )

    # Проверка размера
    file.file.seek(0, 2)
    size = file.file.tell()
    file.file.seek(0)

    MAX_SIZE = 5 * 1024 * 1024

    if size > MAX_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File too large (max 5MB)"
        )


def process(file: UploadFile):
    validate_file(file)

    text = extract_text_from_docx(file)
    result = extract_entities(text)

    return {
        "safety_equipment": result.get("safety_equipment", []),
        "tools": result.get("tools", []),
        "measuring_devices": result.get("measuring_devices", [])
    }


@router.post("/extract", response_model=ExtractResponse)
def extract(file: UploadFile = File(...)):
    return process(file)


@router.post("/extract/safety", response_model=SafetyResponse)
def safety(file: UploadFile = File(...)):
    result = process(file)
    return {"safety_equipment": result["safety_equipment"]}


@router.post("/extract/tools", response_model=ToolsResponse)
def tools(file: UploadFile = File(...)):
    result = process(file)
    return {"tools": result["tools"]}


@router.post("/extract/devices", response_model=DevicesResponse)
def devices(file: UploadFile = File(...)):
    result = process(file)
    return {"measuring_devices": result["measuring_devices"]}