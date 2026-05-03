import requests
import json
import os

URL = "http://127.0.0.1:8000/extract"

BASE_DIR = os.path.dirname(__file__)
file_path = os.path.join(BASE_DIR, "test_data.json")


def compare(expected, actual):
    score = 0
    total = 0

    for key in expected:
        exp = set(expected[key])
        act = set(actual.get(key, []))

        if exp:
            score += len(exp & act) / len(exp)
            total += 1

    return score / total if total else 1


with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

total = 0

for i, case in enumerate(data):
    print(f"\n[TEST {i+1}] START")

    try:
        r = requests.post(URL, json={"text": case["text"]}, timeout=30)
        res = r.json()

        score = compare(case["expected"], res)
        total += score

        print("[RESULT]:", res)
        print("[SCORE]:", round(score, 2))

    except Exception as e:
        print("[TEST ERROR]:", e)

print("\n[FINAL SCORE]:", round(total / len(data), 2))