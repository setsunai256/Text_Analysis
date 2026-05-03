import re


def normalize_item(item: str) -> str:
    item = item.lower().strip()

    item = re.sub(r"\s+", " ", item)

    return item


def normalize_list(items: list[str]) -> list[str]:
    return [normalize_item(i) for i in items]