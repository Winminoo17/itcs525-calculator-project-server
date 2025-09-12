from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Expression(BaseModel):
    expr: str
    def expand_percent(self) -> str:
        from calculator import expand_percent 
        return expand_percent(self.expr)
    
class CalculatorLog(BaseModel):
    """Response model for logging calculations."""
    timestamp : datetime
    expr : str
    result : Optional[float] = None 
    ok : bool = True
    error : str = ""
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(), 
        }