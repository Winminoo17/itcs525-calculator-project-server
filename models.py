from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from calculator import expand_percent

class Expression(BaseModel):
    expr: str

    def expand_percent(self) -> str:
        """Expand percent expressions into valid math code."""
        return expand_percent(self.expr)

class CalculatorLog(BaseModel):
    """Model for returning calculation results and logging history."""
    timestamp: datetime
    expr: str
    result: Optional[float] = None
    ok: bool = True
    error: str = ""

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
