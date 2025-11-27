from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select, desc
from ..schemas import ExpressionOut
from ..models import CalculatorLog, Session as SessionModel
from ..database import get_session

router = APIRouter(
    prefix="/history",
    tags=["history"],
)


@router.get("/")
async def get_history(limit: int = 50, db: DBSession = Depends(get_session)) -> list[ExpressionOut]:
    """Retrieve calculator history from database, newest first."""
    # Query database for logs, ordered by newest first
    statement = select(CalculatorLog).order_by(desc(CalculatorLog.timestamp)).limit(limit)
    logs = db.exec(statement).all()
    
    # Convert to ExpressionOut objects
    return [
        ExpressionOut(
            timestamp=log.timestamp,
            expr=log.expr,
            result=log.result,
            ok=log.ok,
            error=log.error
        )
        for log in logs
    ]


@router.delete("/")
async def clear_history(db: DBSession = Depends(get_session)):
    """Clear all history by deleting all sessions (cascades to logs)."""
    # Delete all sessions - this will cascade to calculator logs
    statement = select(SessionModel)
    sessions = db.exec(statement).all()
    
    for session in sessions:
        db.delete(session)
    
    db.commit()
    
    return {"ok": True, "cleared": True}