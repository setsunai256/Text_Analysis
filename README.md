# Text Analysis API

API для извлечения сущностей из `.docx` документов с использованием LLM (Ollama).

Извлекаются категории:

* `safety_equipment` — средства защиты
* `tools` — инструменты
* `measuring_devices` — измерительные приборы

---

## Быстрый запуск

```bash
git clone <repo-url>
cd <repo>
docker compose up --build
```

API:

```
http://localhost:8000
```

---

## Эндпоинты

* `POST /extract` — все категории
* `POST /extract/safety` — только СИЗ
* `POST /extract/tools` — только инструменты
* `POST /extract/devices` — только приборы

Пример:

```bash
curl -X POST "http://localhost:8000/extract" \
  -F "file=@example.docx"
```

---

## Конфигурация

| Переменная | Значение по умолчанию            |
| ---------- | -------------------------------- |
| OLLAMA_URL | http://ollama:11434/api/generate |
| MODEL_NAME | qwen2.5:3b-instruct              |

---

## Модель и настройка

* Используется `qwen2.5:3b-instruct` (загружается автоматически)
* Можно заменить модель через `MODEL_NAME`
* Prompt можно изменить в `llm_service.py` под свою предметную область

---

## Ограничения

* только `.docx`
* до 5 MB
* качество зависит от модели

---

## Стек

* FastAPI
* Ollama (LLM)
* python-docx
* Docker

---

## Лицензия

MIT
