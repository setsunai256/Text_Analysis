Text Analysis API

Простой API для извлечения сущностей из .docx документов с использованием LLM (через Ollama).

Что извлекается:

* safety_equipment — средства защиты
* tools — инструменты
* measuring_devices — измерительные приборы

Запуск:

git clone <repo-url>
cd <repo>
docker compose up --build

Эндпоинты:

* POST /extract — все категории
* POST /extract/safety — только СИЗ
* POST /extract/tools — только инструменты
* POST /extract/devices — только приборы

Конфигурация:

OLLAMA_URL = http://ollama:11434/api/generate
MODEL_NAME = qwen2.5:3b-instruct

Модель и настройка:

Используется модель qwen2.5:3b-instruct (загружается автоматически).
При необходимости можно:

* заменить модель на более мощную через MODEL_NAME
* изменить prompt в llm_service.py

Ограничения:

* только .docx
* качество зависит от модели

Стек:

FastAPI
Ollama
python-docx
Docker

Лицензия:

MIT
