from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware 
from app.routers import history, calculator

app = FastAPI(title="Mini calculator API")

app.include_router(calculator.router)
app.include_router(history.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


