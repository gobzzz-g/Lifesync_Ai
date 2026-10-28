from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import get_db
from app.models.user import User, UserProfile
from app.schemas.user import UserCreate, UserResponse, TokenResponse, UserLogin
from app.core.security import get_password_hash, verify_password, create_access_token
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user:
        hashed_password = get_password_hash(user.password or "password")
        db_user = User(
            name=user.name,
            email=user.email,
            hashed_password=hashed_password,
            age=user.age
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        # Create empty profile for new user
        new_profile = UserProfile(user_id=db_user.id)
        db.add(new_profile)
        db.commit()

    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=TokenResponse)
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    # Any email and any password can log in (bypass strict password/db check)
    user = db.query(User).filter(User.email == user_credentials.email).first()
    if not user:
        name = user_credentials.email.split("@")[0].capitalize()
        hashed_password = get_password_hash(user_credentials.password or "password")
        user = User(
            name=name if name else "User",
            email=user_credentials.email,
            hashed_password=hashed_password,
            age=25
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        # Create empty profile for new user
        new_profile = UserProfile(user_id=user.id)
        db.add(new_profile)
        db.commit()
    
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/logout")
def logout():
    return {"message": "Successfully logged out"}
