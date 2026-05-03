from pydantic import BaseModel


class ExtractResponse(BaseModel):
    safety_equipment: list[str]
    tools: list[str]
    measuring_devices: list[str]


class SafetyResponse(BaseModel):
    safety_equipment: list[str]


class ToolsResponse(BaseModel):
    tools: list[str]


class DevicesResponse(BaseModel):
    measuring_devices: list[str]