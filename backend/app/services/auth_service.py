from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Optional
from app.database.session import get_db
from app.models.entities import User
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token
from app.schemas.schemas import UserCreate, UserLogin

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)

class AuthService:
    @staticmethod
    def register_user(db: Session, user_in: UserCreate) -> User:
        existing = db.query(User).filter((User.email == user_in.email) | (User.username == user_in.username)).first()
        if existing:
            raise HTTPException(status_code=400, detail="User with this email or username already exists.")
        
        user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            is_active=True,
            is_superuser=False
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> User:
        user = db.query(User).filter(User.email == login_data.email).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password.")
        if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user account.")
        return user

def get_current_user(token: Optional[str] = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Optional[User]:
    if not token:
        # Return default dev demo user for ease of local testing if no token provided
        user = db.query(User).first()
        if not user:
            user = User(
                email="lead.reviewer@corp.dev",
                username="lead_reviewer",
                hashed_password=get_password_hash("password123"),
                is_active=True,
                is_superuser=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token.")
    
    user_id = int(payload["sub"])
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found.")
    return user
