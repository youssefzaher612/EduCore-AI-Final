# EduCore AI Service

Python AI service for EduCore: FastAPI, RAG, PostgreSQL + pgvector, Celery/RabbitMQ, Redis, Ollama (default provider), and optional Streamlit UI. The .NET Backend is a separate repository and is not modified by this package.

## Folder layout

```text
eduCore-ai-main/
├── educore/                 # Runtime Python package; import paths preserved
│   ├── api/                 # FastAPI routes and dependencies
│   ├── database/            # SQLAlchemy models, sessions, repositories
│   ├── rag/                 # Extraction, chunking, embeddings, retrieval, generation
│   ├── student_ai/          # Student analytics and Pydantic response schemas
│   ├── services/            # Student, teacher, chat and ingestion services
│   ├── tasks/               # Celery background tasks
│   └── teacher_ai/          # Teacher AI modules
├── tests/                   # Tests and diagnostic scripts
├── docs/                    # Architecture, setup, model and audit documentation
├── legacy/                  # Preserved backup implementation (reference only)
├── scripts/                 # Setup helpers
├── alembic/                 # Python-service database migrations
├── streamlit_app.py         # Optional local UI
├── docker-compose.yml       # Local PostgreSQL, RabbitMQ and Redis only
├── Dockerfile
├── pyproject.toml
└── .env.example
```

## Windows setup (PowerShell)

Prerequisites: Python 3.10+ (3.11 recommended), Docker Desktop, and Ollama.

1. Extract this ZIP. Open PowerShell in the `eduCore-ai-main` folder.
2. Create and activate a virtual environment:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[streamlit,dev]"
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal and activate again.

3. Create `.env` and edit keys/settings as needed:

```powershell
Copy-Item .env.example .env
```

Default local AI uses Ollama. Install/start Ollama, then pull the configured model (the default is `qwen3-vl:2b-instruct-q4_K_M`):

```powershell
ollama pull qwen3-vl:2b-instruct-q4_K_M
```

4. Start only this AI service's infrastructure (PostgreSQL, RabbitMQ, Redis):

```powershell
docker compose up -d
docker compose ps
```

5. Apply this Python service's migrations:

```powershell
alembic upgrade head
```

6. Run each process in its own PowerShell window, all opened in the project root and with `.venv` activated:

```powershell
# Window 1 — API
python -m uvicorn educore.main:app --host 127.0.0.1 --port 8000 --reload
```

```powershell
# Window 2 — background ingestion worker
python -m celery -A educore.celery_app worker --loglevel=info -Q educore.process --pool=solo
```

```powershell
# Window 3 — optional Streamlit UI
streamlit run streamlit_app.py
```

`--pool=solo` is the Windows-friendly Celery worker pool. On Linux/macOS you may omit it.

## URLs and checks

- FastAPI: http://127.0.0.1:8000/
- OpenAPI docs: http://127.0.0.1:8000/docs
- Streamlit: http://localhost:8501
- RabbitMQ management: http://localhost:15672 (local compose defaults: guest / guest)

Check API startup at `/` and `/docs`. Check services with `docker compose ps`. Check the worker terminal for successful broker connection and task consumption.

## Stop / restart

Stop API, worker and Streamlit with `Ctrl+C` in their terminals. Stop containers but preserve their data with:

```powershell
docker compose stop
```

Start them again with `docker compose start`. To remove containers but preserve named volumes, use `docker compose down`. **Do not use `docker compose down -v`** unless you intentionally want to delete the local database and queue data.

## Troubleshooting

- `psycopg` missing during Alembic: run `pip install "psycopg[binary]"` in the active venv.
- API cannot connect to DB/broker: verify `docker compose ps`, then compare `.env` URLs with `docker-compose.yml`.
- Worker does not process uploads: make sure the worker is running and subscribed to `educore.process`.
- Ollama connection/model error: verify Ollama is running and `ollama list` shows the configured model.
- Scanned PDF OCR on Windows: run `powershell -ExecutionPolicy Bypass -File .\scripts\setup_ocr.ps1` and set `TESSERACT_CMD` / `TESSDATA_DIR` in `.env` if auto-detection fails.

## Student and Teacher modules

- `educore/student_ai/`: Student mastery analytics, study-plan helpers and Student AI schemas.
- `educore/services/student_service.py`: Student-facing application/service workflows; it stays in `services` to preserve existing imports.
- `educore/teacher_ai/modules/`: Teacher modules (`lesson_preparation`, `assessment_generator`, `grading_feedback`, `student_analytics`, `reports_communication`).
- `educore/teacher_ai/modules/student_analytics/` is teacher-side student analytics, distinct from the Student-facing `educore/student_ai/` package.

Compatibility: `educore.student_ai_schemas` remains as a shim so existing imports continue to work.

## Backend integration

See [`docs/BACKEND_INTEGRATION.md`](docs/BACKEND_INTEGRATION.md). The Python API and .NET Backend contracts are not interchangeable; agree on an authenticated adapter contract before connecting production traffic.

## Tests

```powershell
python -m compileall educore
python -m pytest tests -q
```

Some tests need database, broker, model or API credentials; the test suite is not guaranteed to pass without those services.
