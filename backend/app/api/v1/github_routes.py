from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.entities import Review, User
from app.schemas.schemas import GitHubRepoResponse, GitHubPRResponse, GitHubPRReviewRequest, ReviewDetailResponse, ReviewCreate
from app.github.github_service import GitHubService
from app.services.review_orchestrator import ReviewOrchestrator
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/repositories", response_model=List[GitHubRepoResponse])
def list_repositories():
    return GitHubService.get_demo_repositories()

@router.get("/repositories/{repo_name:path}/pulls", response_model=List[GitHubPRResponse])
def list_pull_requests(repo_name: str):
    return GitHubService.get_demo_pull_requests(repo_name)

@router.post("/reviews/pr", response_model=ReviewDetailResponse)
async def review_pull_request(
    payload: GitHubPRReviewRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    prs = GitHubService.get_demo_pull_requests(payload.repo_full_name)
    target_pr = next((p for p in prs if p["number"] == payload.pr_number), None)
    if not target_pr:
        raise HTTPException(status_code=404, detail=f"Pull Request #{payload.pr_number} not found in {payload.repo_full_name}")

    diff_content = target_pr.get("diff_content", "")
    code_lines = []
    for line in diff_content.splitlines():
        if line.startswith("+") and not line.startswith("+++"):
            code_lines.append(line[1:])
        elif not line.startswith("-") and not line.startswith("@@") and not line.startswith("diff"):
            code_lines.append(line)
            
    source_snippet = "\n".join(code_lines) if code_lines else diff_content

    review_create = ReviewCreate(
        title=f"PR #{target_pr['number']}: {target_pr['title']}",
        language="python",
        source_type="github_pr",
        file_path="pr_diff.py",
        source_code=source_snippet,
        git_diff=diff_content,
        min_confidence=0.60
    )

    review = await ReviewOrchestrator.run_review(db, review_create, current_user)
    return review
