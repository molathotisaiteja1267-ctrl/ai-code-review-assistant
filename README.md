

# CodeReviewAI

### AI-Powered Code Quality & Security Platform

CodeReviewAI is a developer-focused platform that combines **AST analysis, static analysis, security scanning, project-aware RAG, and LLM reasoning** to review source code and GitHub Pull Requests.

It identifies security vulnerabilities, bugs, performance issues, code-quality problems, and project-specific coding violations, while also generating and validating suggested fixes.

## ✨ Features

- **Hybrid Code Review** — Combines AST, Ruff, Bandit, security scanning, complexity analysis, and AI reasoning.
- **AST Taint Tracking** — Detects unsafe data flows such as dynamically constructed SQL queries.
- **Security Analysis** — Detects SQL injection, command injection, hardcoded secrets, insecure deserialization, and other risky patterns.
- **Multi-Signal Evidence Fusion** — Combines findings from multiple analyzers and removes duplicate issues.
- **AI Fix Generation** — Generates suggested fixes with explanations.
- **Automated Fix Validation** — Re-analyzes generated fixes for syntax, security, and regressions.
- **Project-Aware RAG** — Uses project documentation and coding guidelines during reviews.
- **GitHub PR Review** — Analyzes changed files and diff hunks from Pull Requests.
- **Monaco Editor** — Provides line-level findings, code navigation, and side-by-side diffs.
- **Review History & Dashboard** — Tracks reviews, findings, quality scores, and risks.
- **Evaluation & Benchmarking** — Compares Static, LLM, and Hybrid analysis approaches.

## 🧠 How It Works

```text
Source Code / GitHub Pull Request
              ↓
        AST Analysis
              ↓
   Static & Security Scanning
              ↓
        Project RAG
              ↓
        LLM Analysis
              ↓
     Evidence Aggregation
              ↓
     Risk & Quality Scoring
              ↓
        Review Results
              ↓
       AI Fix Generation
              ↓
        Fix Validation
````

## 🛠️ Tech Stack

| Layer         | Technologies                                 |
| ------------- | -------------------------------------------- |
| Frontend      | React, TypeScript, Vite, Tailwind CSS        |
| Code Editor   | Monaco Editor                                |
| Backend       | Python, FastAPI, Pydantic, SQLAlchemy        |
| Analysis      | Python AST, Ruff, Bandit, Radon              |
| AI            | LLM provider abstraction, RAG                |
| Database      | SQLite / PostgreSQL-compatible configuration |
| Visualization | Recharts                                     |
| DevOps        | Docker, Docker Compose, GitHub               |

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

### Important

Inside the README, **code snippets like the `text` architecture diagram above should have triple backticks**, but the **entire README must not be wrapped in triple backticks**.

After saving the file, commit the formatting fix:

```powershell
git add README.md
git commit -m "Improve README documentation and formatting"
git push
```

Then refresh GitHub. It should render with proper **headings, bullets, tables, code blocks, and sections**, instead of the black code-editor appearance in your screenshot.
