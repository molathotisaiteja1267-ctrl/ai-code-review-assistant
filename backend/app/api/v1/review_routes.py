from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.entities import Review, ReviewIssue, User
from app.schemas.schemas import ReviewCreate, ReviewResponse, ReviewDetailResponse, MultiFileReviewCreate
from app.services.review_orchestrator import ReviewOrchestrator
from app.services.auth_service import get_current_user
from app.services.report_exporter import ReportExporter

router = APIRouter()

@router.post("", response_model=ReviewDetailResponse)
async def create_review(
    review_in: ReviewCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    review = await ReviewOrchestrator.run_review(db, review_in, current_user)
    return review

@router.post("/multi-file", response_model=List[ReviewDetailResponse])
async def create_multi_file_review(
    payload: MultiFileReviewCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    results = []
    for f in payload.files:
        single_req = ReviewCreate(
            title=f"{payload.title} - {f.file_path}",
            file_path=f.file_path,
            source_code=f.content,
            source_type="upload",
            repository_id=payload.repository_id,
            min_confidence=payload.min_confidence
        )
        rev = await ReviewOrchestrator.run_review(db, single_req, current_user)
        results.append(rev)
    return results

@router.get("", response_model=List[ReviewResponse])
def list_reviews(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 50,
    current_user: Optional[User] = Depends(get_current_user)
):
    query = db.query(Review).order_by(Review.created_at.desc())
    if current_user:
        query = query.filter((Review.user_id == current_user.id) | (Review.user_id == None))
    reviews = query.offset(skip).limit(limit).all()
    
    # Attach issue counts
    results = []
    for r in reviews:
        res = ReviewResponse.model_validate(r)
        res.issues_count = len(r.issues)
        res.critical_count = sum(1 for i in r.issues if i.severity == "critical")
        res.high_count = sum(1 for i in r.issues if i.severity == "high")
        res.medium_count = sum(1 for i in r.issues if i.severity == "medium")
        res.low_count = sum(1 for i in r.issues if i.severity == "low")
        results.append(res)
    return results

@router.get("/{review_id}", response_model=ReviewDetailResponse)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    return review

@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    db.delete(review)
    db.commit()
    return {"status": "deleted", "id": review_id}

@router.get("/{review_id}/export/markdown")
def export_markdown(review_id: int, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")
    content = ReportExporter.generate_markdown(review)
    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename=review_report_{review_id}.md"}
    )
