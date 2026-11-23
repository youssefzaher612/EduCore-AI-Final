# Integration boundary with the EduCore .NET Backend

This repository remains the Python AI service. The .NET Backend repository is a separate application and is not copied or modified here.

## Existing .NET contracts verified in the supplied Backend source

- `POST /api/v1/ai/exams` accepts `CreateAiExamRequest` (`GroupId`, `Subject`, `Topic`, `QuestionCount`, `TotalMarks`, `Instructions`) and queues a draft exam.
- `GET /api/v1/ai/jobs` and `GET /api/v1/ai/jobs/{id}` list/read jobs.
- `POST /api/v1/ai/jobs/{id}/review` accepts `ReviewAiJobRequest` (`Approve`, `Notes`).
- `POST /api/v1/files/uploads` accepts `CreateFileUploadRequest` (`FileName`, `ContentType`, `SizeBytes`, `GroupId`, `IsVideo`); `POST /api/v1/files/{id}/complete` finalizes the upload.

These are .NET Backend endpoints, not endpoints implemented by this Python project. The Python service currently exposes its own routes (see `educore/api/routes.py`) for document ingestion, RAG chat, student AI and teacher AI. The supplied .NET contracts do not expose an equivalent general-purpose RAG chat/document-indexing contract. Therefore this reorganization deliberately does **not** pretend the two APIs are already wired together.

## Safe integration approach

1. Keep the .NET Backend as the system of record for identity, tenants, groups, permissions and business workflows.
2. Keep this Python service responsible for AI/RAG processing until a versioned service-to-service contract is agreed.
3. Have the .NET Backend call a dedicated authenticated Python AI endpoint through a future adapter; do not make the browser call the Python service with privileged credentials.
4. Map identifiers and authorization explicitly (tenant/user/group/file IDs), and define upload handoff, status callbacks, error mapping, retries and timeouts before enabling production traffic.
5. Do not share the two projects' database schemas or run one project's migrations against the other's database.

No .NET source files are included in this package.
