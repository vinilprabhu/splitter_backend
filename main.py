from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from src.auth import get_current_user
from src.models.init import init_db

# Include routers
from src.routers import user, group, expense, settlement

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown (optional cleanup)

app = FastAPI(
    title="Splitter",
    summary="A FastAPI backend for a Splitwise-like expense sharing app",
    description="Splitter helps users track shared expenses, manage groups, and settle debts easily.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(user.router)
app.include_router(group.router)
app.include_router(expense.router)
app.include_router(settlement.router)
