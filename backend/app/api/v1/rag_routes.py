from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.session import get_db
from app.models.entities import ProjectRule, User
from app.schemas.schemas import ProjectRuleCreate, ProjectRuleResponse
from app.rag.rag_service import rag_service
from app.services.auth_service import get_current_user

router = APIRouter()

@router.get("/rules", response_model=List[ProjectRuleResponse])
def get_rules(db: Session = Depends(get_db)):
    rules = db.query(ProjectRule).order_by(ProjectRule.created_at.desc()).all()
    if not rules:
        default_seed = [
            ("Database Repository Pattern", "architecture", "All database queries must go through repository classes. Do not invoke cursor.execute directly in views or controllers."),
            ("Role-Based Authorization", "security", "All administrative endpoints must enforce Role-Based Access Control (@require_role('admin'))."),
            ("Zero Plaintext Secrets", "security", "Never commit API keys, passwords, or tokens in source code. Use os.getenv or AWS Secrets Manager."),
            ("Async I/O Concurrency", "performance", "Use async/await for network I/O and external API calls to avoid blocking the event loop."),
            ("Exception Traceback Logging", "reliability", "Always log caught exceptions with exc_info=True instead of swallowing them with bare pass.")
        ]
        for name, r_type, content in default_seed:
            pr = ProjectRule(name=name, rule_type=r_type, content=content, is_active=True)
            db.add(pr)
        db.commit()
        rules = db.query(ProjectRule).all()
    return rules

@router.post("/rules", response_model=ProjectRuleResponse)
def create_rule(
    payload: ProjectRuleCreate,
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user)
):
    rule = ProjectRule(
        user_id=current_user.id if current_user else None,
        repository_id=payload.repository_id,
        name=payload.name,
        rule_type=payload.rule_type,
        content=payload.content,
        description=payload.description,
        is_active=True
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    
    rag_service.add_project_rule(f"rule_{rule.id}", f"{rule.name}: {rule.content}", rule.rule_type)
    return rule

@router.post("/search")
def search_rules(query: str = Query(..., description="Query text to match against vector rules")):
    matches = rag_service.retrieve_relevant_rules(query, top_k=5)
    return {"query": query, "matches": matches}
