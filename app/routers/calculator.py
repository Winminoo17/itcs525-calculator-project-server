from fastapi import APIRouter
from datetime import datetime
from ..dependencies import expand_percent, history
from asteval import Interpreter
from ..schemas import ExpressionIn, ExpressionOut 
import math

router = APIRouter(
    prefix="/calculator",
    tags=["calculator"],
)
aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

@router.post("/")
async def calculate(expr: str):
    try:
        expr_in = ExpressionIn(expr=expr)
        code = expr_in.expand_percent()
        code = code.replace('÷', '/').replace('×', '*')
        result = aeval(code)
        if aeval.error:
            msg = "; ".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            return ExpressionOut(
                timestamp=datetime.now(),
                ok=False,
                expr=expr,
                result=None,
                error=msg
            )
        history.appendleft(ExpressionOut(
            timestamp=datetime.now(),
            expr=expr,
            result=result
        ))
        return ExpressionOut(
            timestamp=datetime.now(),
            ok=True,
            expr=expr,
            result=result,
            error=""
        )
    except Exception as e:
        return ExpressionOut(
            timestamp=datetime.now(),
            ok=False,
            expr=expr,
            result=None,
            error=str(e)
        )