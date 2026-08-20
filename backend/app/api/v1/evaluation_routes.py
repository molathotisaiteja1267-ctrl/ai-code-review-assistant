from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.entities import EvaluationRun, User
from app.schemas.schemas import EvaluationRequest, EvaluationRunResponse
from app.evaluation.evaluator import BenchmarkEvaluator
from app.services.auth_service import get_current_user

router = APIRouter()

@router.post("/run", response_model=EvaluationRunResponse)
def run_evaluation(
    payload: EvaluationRequest,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    res = BenchmarkEvaluator.run_benchmark(mode=payload.mode)
    run = EvaluationRun(
        user_id=current_user.id if current_user else None,
        run_mode=res["run_mode"],
        total_samples=res["total_samples"],
        true_positives=res["true_positives"],
        false_positives=res["false_positives"],
        false_negatives=res["false_negatives"],
        true_negatives=res["true_negatives"],
        precision=res["precision"],
        recall=res["recall"],
        f1_score=res["f1_score"],
        accuracy=res["accuracy"],
        avg_latency_ms=res["avg_latency_ms"],
        results_json=res["results"]
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run

@router.get("/history", response_model=List[EvaluationRunResponse])
def get_evaluation_history(db: Session = Depends(get_db)):
    return db.query(EvaluationRun).order_by(EvaluationRun.created_at.desc()).limit(20).all()
