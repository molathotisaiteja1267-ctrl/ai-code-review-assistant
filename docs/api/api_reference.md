# REST API Reference

Base URL: `/api/v1`

## 1. Authentication
- `POST /auth/register` - Create new developer account (Email, username, password). Returns JWT token.
- `POST /auth/login` - Authenticate with email/password. Returns JWT token.
- `GET /auth/me` - Get profile of authenticated user.

## 2. Code Reviews
- `POST /reviews` - Execute full review pipeline on code snippet or diff.
- `POST /reviews/multi-file` - Execute batch review across multiple uploaded source files.
- `GET /reviews` - List historical reviews with issue counts and score metrics.
- `GET /reviews/{id}` - Fetch review details, line markers, detected issues, and fixes.
- `DELETE /reviews/{id}` - Delete review record.
- `GET /reviews/{id}/export/markdown` - Download executive Markdown review report.

## 3. Fixes & Safety Validation
- `POST /fixes/generate` - Generate secure replacement patch with what changed, why safer, and automated AST validation.
- `POST /fixes/{id}/apply` - Apply verified patch to review source buffer.

## 4. GitHub PR Integration
- `GET /github/repositories` - List connected/sandbox GitHub repositories.
- `GET /github/repositories/{repo}/pulls` - List open Pull Requests with changed files and diffs.
- `POST /github/reviews/pr` - Execute line-level review on Pull Request diff.

## 5. Project Rules & RAG
- `GET /rag/rules` - List active project coding guidelines.
- `POST /rag/rules` - Add new guideline to vector knowledge base.
- `POST /rag/search` - Test semantic vector search against guidelines.

## 6. Evaluation & Benchmarks
- `POST /evaluation/run` - Execute benchmark suite across ground truth dataset (`mode: 'hybrid' | 'static_only' | 'llm_only'`).
- `GET /evaluation/history` - Retrieve historical benchmark runs and accuracy metrics.

## 7. Dashboard Telemetry
- `GET /dashboard/stats` - Retrieve aggregate reviews count, critical findings, severity distribution, and quality trends.
