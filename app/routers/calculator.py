from fastapi import APIRouter, Depends
from sqlmodel import Session as DBSession, select, desc
from datetime import datetime, timedelta
from asteval import Interpreter
from ..dependencies import expand_percent
from ..schemas import ExpressionIn, ExpressionOut
from ..models import CalculatorLog, Session as SessionModel
from ..database import get_session
import math

router = APIRouter(
    prefix="/calculator",
    tags=["calculator"],
)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

SESSION_TIMEOUT_SECONDS = 10


@router.post("/")
async def calculate(expr: str, db: DBSession = Depends(get_session)):
    try:
        expr_in = ExpressionIn(expr=expr)
        code = expr_in.expand_percent()
        code = code.replace('÷', '/').replace('×', '*')
        result = aeval(code)
        
        # Handle evaluation errors
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            
            response = ExpressionOut(
                timestamp=datetime.now(),
                ok=False,
                expr=expr,
                result=None,
                error=msg
            )
            
            # Still log errors to database
            current_session = get_or_create_session(db, response.timestamp)
            log = CalculatorLog(
                timestamp=response.timestamp,
                expr=response.expr,
                result=response.result,
                ok=response.ok,
                error=response.error,
                session_id=current_session.id
            )
            db.add(log)
            db.commit()
            
            return response
        
        # Success case
        response = ExpressionOut(
            timestamp=datetime.now(),
            ok=True,
            expr=expr,
            result=result,
            error=""
        )
        
        # Session management and database insert
        current_session = get_or_create_session(db, response.timestamp)
        
        log = CalculatorLog(
            timestamp=response.timestamp,
            expr=response.expr,
            result=response.result,
            ok=response.ok,
            error=response.error,
            session_id=current_session.id
        )
        
        db.add(log)
        db.commit()
        db.refresh(log)
        
        return response
        
    except Exception as e:
        response = ExpressionOut(
            timestamp=datetime.now(),
            ok=False,
            expr=expr,
            result=None,
            error=str(e)
        )
        
        # Log exception to database
        current_session = get_or_create_session(db, response.timestamp)
        log = CalculatorLog(
            timestamp=response.timestamp,
            expr=response.expr,
            result=response.result,
            ok=response.ok,
            error=response.error,
            session_id=current_session.id
        )
        db.add(log)
        db.commit()
        
        return response


def get_or_create_session(db: DBSession, current_time: datetime) -> SessionModel:
    """Get existing session or create new one based on timeout."""
    # Get the latest session
    statement = select(SessionModel).order_by(desc(SessionModel.started_at)).limit(1)
    latest_session = db.exec(statement).first()
    
    if latest_session is None:
        # No session exists, create first one
        new_session = SessionModel(
            name=f"Session {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
            started_at=current_time
        )
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        return new_session
    else:
        # Check time difference
        time_diff = (current_time - latest_session.started_at).total_seconds()
        
        if time_diff > SESSION_TIMEOUT_SECONDS:
            # Update old session's ended_at
            latest_session.ended_at = current_time
            db.add(latest_session)
            
            # Create new session
            new_session = SessionModel(
                name=f"Session {current_time.strftime('%Y-%m-%d %H:%M:%S')}",
                started_at=current_time
            )
            db.add(new_session)
            db.commit()
            db.refresh(new_session)
            return new_session
        else:
            # Use existing session
            return latest_session