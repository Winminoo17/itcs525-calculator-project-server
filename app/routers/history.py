from fastapi import APIRouter
from ..dependencies import history, HISTORY_MAX
from ..schemas import ExpressionOut 

router = APIRouter(
    prefix="/history",
    tags=["history"],
)

@router.get("/")
async def get_history(limit: int = 50) -> list[ExpressionOut]:
            return list(history)[: max(0, min(limit, HISTORY_MAX))] 

@router.delete("/")
async def clear_history():
        history.clear()
        return {"ok": True, "cleared": True}