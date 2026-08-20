from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.entities import Review, ReviewIssue, ReviewFix
from app.schemas.schemas import FixRequest, FixResponse
from app.ai.fix_generator import FixGenerator
from app.ai.fix_validator import FixValidator
from app.analyzers.base import RawFinding, Category, Severity

router = APIRouter()

@router.post("/generate", response_model=FixResponse)
def generate_and_validate_fix(payload: FixRequest, db: Session = Depends(get_db)):
    issue = db.query(ReviewIssue).filter(ReviewIssue.id == payload.issue_id).first()
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found.")
    
    review = db.query(Review).filter(Review.id == issue.review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Associated review not found.")

    raw_f = RawFinding(
        title=issue.title,
        category=Category(issue.category),
        severity=Severity(issue.severity),
        confidence=issue.confidence,
        file_path=issue.file_path,
        line_start=issue.line_start,
        line_end=issue.line_end,
        explanation=issue.explanation,
        impact=issue.impact,
        recommendation=issue.recommendation,
        suggested_fix=issue.suggested_fix
    )

    # 1. Generate Fix
    fix_data = FixGenerator.generate_fix(review.source_code, raw_f)

    # 2. Automatically Run Safety & Regression Validation Loop
    validation = FixValidator.validate_fix(
        original_code=review.source_code,
        patched_code=fix_data["full_patched_code"],
        target_issue_title=issue.title,
        filename=issue.file_path
    )

    # 3. Store / Update Fix in DB
    existing_fix = db.query(ReviewFix).filter(ReviewFix.issue_id == issue.id).first()
    if existing_fix:
        existing_fix.original_snippet = fix_data["original_snippet"]
        existing_fix.patched_snippet = fix_data["patched_snippet"]
        existing_fix.full_patched_code = fix_data["full_patched_code"]
        existing_fix.diff_content = fix_data["diff_content"]
        existing_fix.what_changed = fix_data["what_changed"]
        existing_fix.why_safer = fix_data["why_safer"]
        existing_fix.validation_results = validation
        db.commit()
        db.refresh(existing_fix)
        return existing_fix

    new_fix = ReviewFix(
        issue_id=issue.id,
        review_id=review.id,
        original_snippet=fix_data["original_snippet"],
        patched_snippet=fix_data["patched_snippet"],
        full_patched_code=fix_data["full_patched_code"],
        diff_content=fix_data["diff_content"],
        what_changed=fix_data["what_changed"],
        why_safer=fix_data["why_safer"],
        validation_results=validation,
        is_applied=False
    )
    db.add(new_fix)
    db.commit()
    db.refresh(new_fix)
    return new_fix

@router.post("/{fix_id}/apply")
def apply_fix(fix_id: int, db: Session = Depends(get_db)):
    fix = db.query(ReviewFix).filter(ReviewFix.id == fix_id).first()
    if not fix:
        raise HTTPException(status_code=404, detail="Fix not found.")
    
    review = db.query(Review).filter(Review.id == fix.review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found.")

    if fix.full_patched_code:
        review.source_code = fix.full_patched_code
    
    fix.is_applied = True
    issue = db.query(ReviewIssue).filter(ReviewIssue.id == fix.issue_id).first()
    if issue:
        issue.is_resolved = True

    db.commit()
    return {"status": "applied", "fix_id": fix_id, "updated_source_code": review.source_code}
