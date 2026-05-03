import requests
import json
import re
import os
import logging
from app.services.normalize import normalize_list


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s"
)

logger = logging.getLogger(__name__)


OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5:3b-instruct")

TIMEOUT = 300


def safe_json_extract(text: str):
    logger.info("Parsing LLM response...")

    try:
        return json.loads(text)
    except:
        pass

    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                return json.loads(match.group())
            except:
                pass

    logger.warning("Failed to parse JSON. Returning empty result.")

    return {
        "safety_equipment": [],
        "tools": [],
        "measuring_devices": []
    }


def warmup():
    """
    Просто прогревает модель.
    Никакой логики извлечения тут быть НЕ должно.
    """
    logger.info("Warming up LLM...")

    try:
        requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": "ping",
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0,
                    "num_predict": 1
                }
            },
            timeout=TIMEOUT
        )

        logger.info("Warmup successful")

    except Exception as e:
        logger.warning(f"Warmup failed (non-critical): {e}")


def extract_entities(text: str) -> dict:
    logger.info("Starting entity extraction")

    prompt = f"""
    You are an information extraction system.
    
    TASK:
    Extract 3 categories from the text:
    1. safety_equipment
    2. tools
    3. measuring_devices
    
    STRICT RULES:
    - Output ONLY valid JSON
    - No comments, no explanations
    - Use lowercase
    - Remove duplicates
    - Return empty list if nothing found
    
    EXAMPLES:
    
    Text:
    "Рабочие использовали каски, защитные очки и молоток"
    
    Output:
    {{
      "safety_equipment": ["каски", "защитные очки"],
      "tools": ["молоток"],
      "measuring_devices": []
    }}
    
    ---
    
    TEXT:
    {text}
    """

    try:
        logger.info("LLM request")

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "10m",
                "options": {
                    "temperature": 0,
                    "num_predict": 256
                }
            },
            timeout=TIMEOUT
        )

        response.raise_for_status()

        raw = response.json().get("response", "")

        logger.info(f"LLM raw response: {raw[:300]}...")

        parsed = safe_json_extract(raw)

        result = {
            "safety_equipment": normalize_list(parsed.get("safety_equipment", [])),
            "tools": normalize_list(parsed.get("tools", [])),
            "measuring_devices": normalize_list(parsed.get("measuring_devices", []))
        }

        for key in result:
            result[key] = list(set(result[key]))

        logger.info("Extraction successful")

        return result

    except Exception as e:
        logger.error(f"LLM request failed: {e}")

        return {
            "safety_equipment": [],
            "tools": [],
            "measuring_devices": []
        }