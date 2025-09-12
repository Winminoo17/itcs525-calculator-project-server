import math
from collections import deque

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from asteval import Interpreter
from calculator import expand_percent

app = FastAPI(title="Mini calculator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

aeval = Interpreter(minimal=True, usersyms={"pi": math.pi, "e": math.e})

HISTORY_MAX = 1000
history = deque(maxlen=HISTORY_MAX)

def add_to_history(expr: str, result, ok: bool, error: str = ""):
    history_item = {
        "expr": expr,
        "result": result,
        "ok": ok,
        "error": error
    }
    history.append(history_item) 

@app.post("/calculator")
def calculate(expr: str):
    try:
        clean_expr = expr.replace("×", "*").replace("÷", "/").replace("−", "-")
        code = expand_percent(clean_expr)
        result = aeval(code)
        
        if aeval.error:
            msg = ";".join(str(e.get_error()) for e in aeval.error)
            aeval.error.clear()
            add_to_history(expr, None, False, msg)
            return {"ok": False, "expr": expr, "result": result, "error": msg}
        
        
        add_to_history(expr, result, True)
        return {"ok": True, "expr": expr, "result": result, "error": ""}
        
    except Exception as e:
        error_msg = str(e)
        # Add failed calculation to history
        add_to_history(expr, None, False, error_msg)
        return {"ok": False, "expr": expr, "error": error_msg}

@app.get("/history")
def get_history(limit: int = 50):
    """Get calculation history with limit."""
    actual_limit = min(limit, len(history), HISTORY_MAX)
    if actual_limit <= 0:
        return []
    history_list = list(history)
    return history_list[-actual_limit:]

@app.delete("/history")
def clear_history():
    history.clear()
    return {"ok": True}