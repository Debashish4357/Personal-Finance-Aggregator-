from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine
from schema import models
import uvicorn
import os
from dotenv import load_dotenv

from routes import UserRoutes, BankRoutes, BudgetRoutes, TransactionRoutes, RegisteredAccountRoutes, LoginRoutes, AlertRoutes
from services.scheduler import start_scheduler, stop_scheduler
import atexit

# Load environment variables
load_dotenv()

app = FastAPI(title="PFA - Personal Finance App")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(UserRoutes.router)
app.include_router(BankRoutes.router)
app.include_router(BudgetRoutes.router)
app.include_router(TransactionRoutes.router)
app.include_router(RegisteredAccountRoutes.router)
app.include_router(LoginRoutes.router)
app.include_router(AlertRoutes.router)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Start scheduler on app startup
@app.on_event("startup")
def startup_event():
    # Start scheduler with 1-hour interval (can be configured)
    start_scheduler(sync_interval_hours=1)

@app.on_event("shutdown")
def shutdown_event():
    stop_scheduler()

# Register shutdown handler
atexit.register(stop_scheduler)
    
@app.get("/")
def read_root():
    return {"message": "server is up and running"}


if __name__ == "__main__":
    # Get port from environment variable (Railway provides this)
    port = 8000
    host = os.getenv("HOST", "0.0.0.0")
    
    uvicorn.run(
        "server:app",
        host=host,
        port=port,
        reload=True if os.getenv("RAILWAY_ENVIRONMENT") != "production" else False
    )

