# Reorganization notes

- The `educore/` package and its internal paths were kept in place to preserve imports used by Uvicorn, Celery, Alembic and Streamlit.
- Root-level documentation was moved to `docs/`.
- Root-level test/diagnostic scripts were moved into `tests/`.
- `EduCore_backup/` was moved to `legacy/EduCore_backup/`; it is not used by the active app.
- Runtime settings, route handlers, database models, migrations, Docker Compose services and dependency declarations were not rewritten.
- The .NET Backend archive was inspected only to document the existing API contract; it was not copied or modified.
