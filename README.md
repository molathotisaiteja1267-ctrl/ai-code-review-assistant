# CodeReviewAI

### AI-Powered Code Quality & Security Platform

CodeReviewAI is a developer tool that combines **AST analysis, static analysis, security scanning, project-aware context, and AI reasoning** to review source code and GitHub Pull Requests.

It detects bugs, security vulnerabilities, performance issues, code-quality problems, and project-specific rule violations, while also generating and validating fixes.

## Features

- **Hybrid Code Review** — Combines static analysis with AI reasoning for deeper code reviews.
- **AST Taint Tracking** — Detects unsafe data flows such as dynamically constructed SQL queries.
- **Security Analysis** — Identifies SQL injection, command injection, hardcoded secrets, insecure deserialization, and other security risks.
- **Multi-Signal Detection** — Combines findings from multiple analysis methods and reduces duplicate issues.
- **AI Fix Generation** — Generates suggested fixes with clear explanations.
- **Fix Validation** — Re-checks generated fixes for syntax and security issues.
- **Project-Aware Review** — Uses project documentation and coding guidelines during analysis.
- **GitHub PR Review** — Reviews Pull Request changes and highlights issues in modified code.
- **Interactive Code Editor** — Provides line-level issue highlighting and code comparison.
- **Review History & Dashboard** — Tracks reviews, findings, risks, and quality scores.
- **Benchmarking** — Compares different review approaches using a test dataset.

  
## How It Works

```text
┌──────────────────────────────┐
│   Source Code / GitHub PR    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        Code Analysis         │
│    AST + Static Analysis     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Security & Quality Checks  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Project Context        │
│          RAG / Rules         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│          AI Review           │
│      Contextual Reasoning    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│   Issue Detection & Scoring  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Review Results         │
│   Bugs • Security • Quality  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│      AI Fix Generation       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Fix Validation         │
│  Syntax • Security • Checks  │
└──────────────────────────────┘
 ```                                



### 4. Tech Stack


## Tech Stack

- **Frontend:** React, TypeScript
- **Backend:** Python, FastAPI
- **AI:** LLMs, RAG
- **Analysis:** AST, static analysis, security scanning
- **Database:** SQLite / PostgreSQL
- **Tools:** Docker, GitHub

  
## 📊 Benchmark

The current local benchmark compares three analysis approaches:

| Pipeline          | Precision |   Recall | F1 Score |
| ----------------- | --------: | -------: | -------: |
| **Hybrid Engine** |  **100%** | **100%** | **100%** |
| Static Only       |      100% |    71.4% |    83.3% |
| LLM Only          |      100% |    71.4% |    83.3% |

> Results are based on the project's current local benchmark dataset and should not be interpreted as general performance on arbitrary production repositories.

## 🚀 Getting Started

### Prerequisites

* Python 3.13+
* Node.js 18+
* npm
* Git
* Docker Desktop *(optional)*

### Backend

```bash
cd backend
python -m venv venv
```

Windows:

```powershell
.\venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload --port 8000
```

API:

`http://localhost:8000`

Swagger documentation:

`http://localhost:8000/docs`

### Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Application:

`http://localhost:5173`

### Docker

```bash
docker compose up --build
```

## 🔐 Environment Configuration

Create your local environment configuration from `.env.example`.

Typical variables include:

```text
DATABASE_URL=
SECRET_KEY=
LLM_PROVIDER=
OPENAI_API_KEY=
GITHUB_CLIENT_ID=
GITHUB_CLIENT_SECRET=
```

Never commit real API keys, tokens, passwords, or secrets.

## 🧪 Testing

Run the backend test suite:

```bash
cd backend
pytest tests/ -v
```

Tests cover:

* AST analysis
* security scanning
* risk scoring
* evidence aggregation
* fix validation
* API endpoints

## 📁 Project Structure

```text
ai-code-review-assistant/
│
├── backend/
│   ├── app/
│   │   ├── ai/
│   │   ├── analyzers/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── evaluation/
│   │   ├── github/
│   │   ├── models/
│   │   ├── rag/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── context/
│   │   ├── pages/
│   │   ├── services/
│   │   └── types/
│   │
│   └── package.json
│
├── docker/
├── docs/
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 🔒 Security

CodeReviewAI is designed to perform code analysis without directly executing arbitrary submitted source code on the host.

The system uses:

* AST parsing
* Static analysis
* Security scanners
* In-memory fix validation
* Protected environment variables

Production deployments should use secure secret management, HTTPS, proper authentication configuration, and a production database.

## 🗺️ Roadmap

* Multi-language deterministic analysis
* Dense embedding-based RAG
* Background job processing
* GitHub App/webhook automation
* Advanced observability
* Production-scale repository analysis

## 👨‍💻 Author

**Sai Teja**
IIT (BHU) Varanasi

Interested in **Software Engineering, AI/ML, LLM Applications, and Developer Tools**.

---

