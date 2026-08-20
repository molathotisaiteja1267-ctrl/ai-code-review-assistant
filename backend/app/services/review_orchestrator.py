import time
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.entities import Review, ReviewIssue, User
from app.schemas.schemas import ReviewCreate
from app.analyzers.ast_analyzer import PythonASTAnalyzer
from app.analyzers.static_analyzer import StaticAnalyzer
from app.analyzers.security_scanner import SecurityScanner
from app.analyzers.complexity_analyzer import ComplexityAnalyzer
from app.analyzers.git_diff_analyzer import GitDiffAnalyzer
from app.analyzers.multi_signal_aggregator import MultiSignalAggregator
from app.analyzers.risk_scorer import RiskScorer
from app.ai.review_engine import AIReviewEngine
from app.rag.rag_service import rag_service

class ReviewOrchestrator:
    @staticmethod
    async def run_review(
        db: Session,
        review_in: ReviewCreate,
        current_user: Optional[User] = None
    ) -> Review:
        start_time = time.time()
        filename = review_in.file_path or "snippet.py"
        source_code = review_in.source_code
        min_conf = review_in.min_confidence or 0.60

        # Step 1 & 2: AST Analysis & Metrics
        ast_findings, metrics, symbols = PythonASTAnalyzer.analyze(source_code, filename)

        # Step 3: Static Analysis (Ruff)
        static_findings = StaticAnalyzer.analyze_python_ruff(source_code, filename)

        # Step 4: Security Analysis (Bandit + Regex)
        security_findings = SecurityScanner.scan_python(source_code, filename)

        # Step 5: Complexity Analysis (Nesting & O(n^2))
        complexity_findings, _ = ComplexityAnalyzer.analyze_metrics(source_code, filename)

        # Step 6: Git Diff Context
        diff_info = None
        if review_in.git_diff:
            diff_info = GitDiffAnalyzer.parse_unified_diff(review_in.git_diff)

        # Step 7: RAG Project Guidelines Retrieval
        rag_rules = []
        if review_in.apply_rag_rules:
            rag_rules = rag_service.retrieve_relevant_rules(source_code, top_k=3)

        # Step 8: Multi-Signal Static Aggregation
        deterministic_findings = ast_findings + static_findings + security_findings + complexity_findings

        # Step 9: LLM Reasoning Engine
        llm_findings = await AIReviewEngine.analyze_with_llm(
            source_code=source_code,
            filename=filename,
            static_findings=deterministic_findings,
            metrics=metrics,
            symbols=symbols,
            rag_rules=rag_rules,
            git_diff=review_in.git_diff
        )

        # Step 10: Multi-Signal Deduplication & Confidence Calibration
        all_raw_findings = deterministic_findings + llm_findings
        aggregated_findings = MultiSignalAggregator.aggregate_and_deduplicate(all_raw_findings, min_confidence=min_conf)

        # Step 11: Multi-Dimensional Risk Scoring
        score_data = RiskScorer.calculate_scores(aggregated_findings, metrics)

        # Step 12: Generate Executive Summary
        exec_summary = (
            f"Review completed in {(time.time() - start_time)*1000:.1f}ms. "
            f"Detected {len(aggregated_findings)} verified findings across security, reliability, and code quality. "
            f"Overall Grade: {score_data['letter_grade']} ({score_data['overall_score']}/100) | Risk: {score_data['risk_level']}."
        )

        # Step 13: Persist Review into Database
        db_review = Review(
            user_id=current_user.id if current_user else None,
            repository_id=review_in.repository_id,
            pull_request_id=review_in.pull_request_id,
            title=review_in.title or f"Review of {filename}",
            language=review_in.language,
            source_type=review_in.source_type,
            file_path=filename,
            source_code=source_code,
            git_diff=review_in.git_diff,
            overall_score=score_data["overall_score"],
            letter_grade=score_data["letter_grade"],
            risk_level=score_data["risk_level"],
            security_score=score_data["security_score"],
            reliability_score=score_data["reliability_score"],
            performance_score=score_data["performance_score"],
            maintainability_score=score_data["maintainability_score"],
            summary=exec_summary,
            metrics_json={
                "cyclomatic_complexity": metrics.cyclomatic_complexity,
                "maintainability_index": metrics.maintainability_index,
                "nesting_depth": metrics.nesting_depth,
                "sloc": metrics.sloc,
                "functions_count": metrics.functions_count,
                "classes_count": metrics.classes_count,
                "functions_details": [f.model_dump() for f in metrics.functions_details]
            },
            status="completed",
            execution_time_ms=round((time.time() - start_time) * 1000, 2)
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)

        # Persist Issues
        for f in aggregated_findings:
            db_issue = ReviewIssue(
                review_id=db_review.id,
                title=f.title,
                category=f.category.value,
                severity=f.severity.value,
                confidence=f.confidence,
                file_path=f.file_path,
                line_start=f.line_start,
                line_end=f.line_end,
                column_start=f.column_start,
                column_end=f.column_end,
                explanation=f.explanation,
                impact=f.impact,
                recommendation=f.recommendation,
                suggested_fix=f.suggested_fix,
                rule_id=f.rule_id,
                evidence_sources=f.evidence_sources,
                is_resolved=False
            )
            db.add(db_issue)
        db.commit()
        db.refresh(db_review)

        return db_review
