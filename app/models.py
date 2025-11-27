from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Session(SQLModel, table=True):
    """Session model to group calculator logs."""
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(default="")
    started_at: datetime = Field(default_factory=datetime.now)
    ended_at: Optional[datetime] = None
    
    # Relationship to CalculatorLog
    logs: List["CalculatorLog"] = Relationship(
        back_populates="session",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class CalculatorLog(SQLModel, table=True):
    """Model for storing calculation history in database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime = Field(default_factory=datetime.now)
    expr: str
    result: Optional[float] = None
    ok: bool = True
    error: str = ""
    
    # Foreign key to Session
    session_id: Optional[int] = Field(default=None, foreign_key="session.id")
    
    # Relationship to Session
    session: Optional[Session] = Relationship(back_populates="logs")