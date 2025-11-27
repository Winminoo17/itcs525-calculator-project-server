from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware 
from app.routers import history, calculator
from app.database import create_db_and_tables


app = FastAPI(title="Mini calculator API")

app.include_router(calculator.router)
app.include_router(history.router)

# Add this event handler after creating the app
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


