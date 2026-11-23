# EduCore AI module map

## Student side
- `educore/student_ai/analytics.py`: Bayesian Knowledge Tracing mastery calculations and weekly study-plan helpers.
- `educore/student_ai/schemas.py`: validated Pydantic output contracts for topics, study plans and generated exams.
- `educore/services/student_service.py`: Student application workflows (RAG-grounded exam generation, attempts, analytics and related operations).
- `educore/student_ai_schemas.py`: backward-compatible import shim; new code should import from `educore.student_ai.schemas`.

## Teacher side
- `educore/teacher_ai/modules/lesson_preparation/`: lesson preparation and verification.
- `educore/teacher_ai/modules/assessment_generator/`: teacher assessment generation.
- `educore/teacher_ai/modules/grading_feedback/`: grading and feedback.
- `educore/teacher_ai/modules/student_analytics/`: teacher-facing student analytics (not the Student AI package).
- `educore/teacher_ai/modules/reports_communication/`: reports and communication.

## Shared infrastructure
- `educore/rag/`: retrieval-augmented generation pipeline.
- `educore/api/`: FastAPI routes and dependencies.
- `educore/database/`: SQLAlchemy models, connection and repositories.
- `educore/tasks/`: Celery background jobs.
- `educore/services/`: application services shared across API workflows.

The Student package split preserves old import paths. No backend repository files are included or changed.
