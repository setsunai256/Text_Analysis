from app.services.normalizer import normalize_word

SAFETY = ["каска", "перчатка", "респиратор"]
TOOLS = ["молоток", "дрель", "отвертка"]
DEVICES = ["мультиметр", "термометр", "газоанализатор"]


def extract_simple(text: str):
    text = text.lower()

    words = text.replace(",", " ").split()
    words = [normalize_word(w) for w in words]

    return {
        "safety_equipment": [w for w in SAFETY if w in words],
        "tools": [w for w in TOOLS if w in words],
        "measuring_devices": [w for w in DEVICES if w in words]
    }