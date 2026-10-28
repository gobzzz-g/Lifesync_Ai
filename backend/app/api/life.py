from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.planner import LifeStateResponse, LifeBalanceResponse, CrossDomainInsightResponse
from app.services.cross_domain_engine import CrossDomainEngine, LifeBalanceEngine, CorrelationEngine, CrossDomainInsightEngine

router = APIRouter(prefix="/api/life", tags=["life"])

@router.get("/state", response_model=LifeStateResponse)
def get_life_state(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CrossDomainEngine.get_life_state(db, current_user.id)

@router.get("/balance", response_model=LifeBalanceResponse)
def get_life_balance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return LifeBalanceEngine.calculate_balance_score(db, current_user.id)

@router.get("/insights", response_model=CrossDomainInsightResponse)
def get_insights(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CrossDomainInsightEngine.generate_insight(db, current_user.id)

@router.get("/correlations", response_model=List[str])
def get_correlations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return CorrelationEngine.get_correlations(db, current_user.id)
