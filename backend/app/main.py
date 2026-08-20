from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging_config import LoggingMiddleware
from app.database.session import engine, Base
from app.api.v1 import (
    auth_routes,
    review_routes,
    fix_routes,
    github_routes,
    rag_routes,
    evaluation_routes,
    dashboard_routes,
    settings_routes
)

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-Grade AI Code Review Assistant with AST, Static Linters, Bandit Security, and RAG Reasoning."
)

# Middleware
app.add_middleware(LoggingMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers with explicit prefixes
pfx = settings.API_V1_STR
app.include_router(auth_routes.router, prefix=f"{pfx}/auth", tags=["Auth"])
app.include_router(review_routes.router, prefix=f"{pfx}/reviews", tags=["Reviews"])
app.include_router(fix_routes.router, prefix=f"{pfx}/fixes", tags=["Fixes"])
app.include_router(github_routes.router, prefix=f"{pfx}/github", tags=["GitHub"])
app.include_router(rag_routes.router, prefix=f"{pfx}/rag", tags=["RAG"])
app.include_router(evaluation_routes.router, prefix=f"{pfx}/evaluation", tags=["Evaluation"])
app.include_router(dashboard_routes.router, prefix=f"{pfx}/dashboard", tags=["Dashboard"])
app.include_router(settings_routes.router, prefix=f"{pfx}/settings", tags=["Settings"])

@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "llm_provider": settings.LLM_PROVIDER
    }
