from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from app.database.session import get_db
from app.models.entities import Review
from app.schemas.schemas import DashboardStatsResponse, ReviewResponse

router = APIRouter()

@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    days: str = Query("30", description="Time range: '7', '30', '90', or 'all'"),
    db: Session = Depends(get_db)
):
    query = db.query(Review)
    if days != "all":
        try:
            num_days = int(days)
            cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(days=num_days)
            query = query.filter(Review.created_at >= cutoff)
        except ValueError:
            pass

    reviews = query.order_by(Review.created_at.desc()).all()
    all_reviews_count = db.query(Review).count()

    total_reviews = len(reviews)
    recent_reviews = reviews[:10]

    all_issues = []
    for r in reviews:
        all_issues.extend(r.issues)

    total_issues = len(all_issues)
    critical_issues = sum(1 for i in all_issues if i.severity == "critical")
    high_issues = sum(1 for i in all_issues if i.severity == "high")
    medium_issues = sum(1 for i in all_issues if i.severity == "medium")
    low_issues = sum(1 for i in all_issues if i.severity == "low")
    security_issues = sum(1 for i in all_issues if i.category == "security")

    avg_quality = (sum(r.overall_score for r in reviews) / total_reviews) if total_reviews > 0 else 100.0
    
    risk_weights = {"CRITICAL": 9.5, "HIGH": 7.0, "MEDIUM": 4.0, "LOW": 1.0}
    avg_risk = (sum(risk_weights.get(r.risk_level, 1.0) for r in reviews) / total_reviews) if total_reviews > 0 else 1.0

    severity_dist = {
        "Critical": critical_issues,
        "High": high_issues,
        "Medium": medium_issues,
        "Low": low_issues
    }

    category_dist = {
        "Security": security_issues,
        "Bugs": sum(1 for i in all_issues if i.category == "bug"),
        "Performance": sum(1 for i in all_issues if i.category == "performance"),
        "Code Quality": sum(1 for i in all_issues if i.category == "code_quality"),
        "Complexity": sum(1 for i in all_issues if i.category == "complexity"),
    }

    trends_map = {}
    for r in reversed(reviews):
        date_str = r.created_at.strftime("%b %d")
        if date_str not in trends_map:
            trends_map[date_str] = {"date": date_str, "score_sum": 0, "count": 0, "issues": 0}
        trends_map[date_str]["score_sum"] += r.overall_score
        trends_map[date_str]["count"] += 1
        trends_map[date_str]["issues"] += len(r.issues)

    quality_trends = [
        {
            "date": v["date"],
            "score": round(v["score_sum"] / v["count"], 1),
            "issues": v["issues"]
        }
        for v in trends_map.values()
    ]

    recent_responses = []
    for r in recent_reviews:
        item = ReviewResponse.model_validate(r)
        item.issues_count = len(r.issues)
        recent_responses.append(item)

    return DashboardStatsResponse(
        total_reviews=total_reviews if days != "all" else all_reviews_count,
        total_issues=total_issues,
        critical_issues=critical_issues,
        high_issues=high_issues,
        medium_issues=medium_issues,
        low_issues=low_issues,
        security_issues=security_issues,
        average_code_quality=round(avg_quality, 1),
        average_risk_score=round(avg_risk, 1),
        recent_reviews=recent_responses,
        severity_distribution=severity_dist,
        category_distribution=category_dist,
        quality_trends=quality_trends
    )
