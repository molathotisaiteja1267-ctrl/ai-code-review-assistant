from fastapi import APIRouter
from app.core.config import settings
from app.schemas.schemas import SettingsResponse, SettingsUpdate

router = APIRouter()

_runtime_settings = {
    "llm_provider": settings.LLM_PROVIDER,
    "llm_model": settings.LLM_MODEL,
    "llm_api_key": settings.LLM_API_KEY,
    "min_confidence": settings.MIN_CONFIDENCE,
    "github_token": settings.GITHUB_TOKEN,
}

@router.get("", response_model=SettingsResponse)
@router.get("/", response_model=SettingsResponse)
def get_settings():
    raw_key = _runtime_settings.get("llm_api_key") or ""
    raw_gh = _runtime_settings.get("github_token") or ""
    
    masked_key = f"{raw_key[:3]}••••••••{raw_key[-2:]}" if len(raw_key) > 6 else ("••••••••" if raw_key else "Not Configured")
    masked_gh = f"{raw_gh[:3]}••••••••{raw_gh[-2:]}" if len(raw_gh) > 6 else ("••••••••" if raw_gh else "Not Configured")
    
    return SettingsResponse(
        llm_provider=_runtime_settings["llm_provider"],
        llm_model=_runtime_settings["llm_model"],
        has_llm_key=bool(raw_key),
        masked_llm_key=masked_key,
        min_confidence=_runtime_settings["min_confidence"],
        has_github_token=bool(raw_gh),
        masked_github_token=masked_gh,
    )

@router.post("", response_model=SettingsResponse)
@router.post("/", response_model=SettingsResponse)
def update_settings(payload: SettingsUpdate):
    if payload.llm_provider is not None:
        _runtime_settings["llm_provider"] = payload.llm_provider
    if payload.llm_model is not None:
        _runtime_settings["llm_model"] = payload.llm_model
    if payload.llm_api_key is not None and not payload.llm_api_key.startswith("•"):
        _runtime_settings["llm_api_key"] = payload.llm_api_key
    if payload.min_confidence is not None:
        _runtime_settings["min_confidence"] = payload.min_confidence
    if payload.github_token is not None and not payload.github_token.startswith("•"):
        _runtime_settings["github_token"] = payload.github_token
        
    return get_settings()
