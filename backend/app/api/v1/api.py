from fastapi import APIRouter
from app.api.v1 import (
    auth_routes,
    review_routes,
    fix_routes,
    github_routes,
    rag_routes,
    evaluation_routes,
    dashboard_routes
)

api_router = APIRouter()

api_router.include_router(auth_routes.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(review_routes.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(fix_routes.router, prefix="/fixes", tags=["Fixes & Validation"])
api_router.include_router(github_routes.router, prefix="/github", tags=["GitHub Integration"])
api_router.include_router(rag_routes.router, prefix="/rag", tags=["RAG & Guidelines"])
api_router.include_router(evaluation_routes.router, prefix="/evaluation", tags=["Benchmark Evaluation"])
api_router.include_router(dashboard_routes.router, prefix="/dashboard", tags=["Dashboard"])
