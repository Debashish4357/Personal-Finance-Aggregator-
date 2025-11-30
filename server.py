from fastapi import FastAPI
from db.database import engine
from schema import models
import uvicorn

from routes import UserRoutes, BankRoutes, BudgetRoutes, TransactionRoutes, RegisteredAccountRoutes

app = FastAPI(title="PFA - Personal Finance App")

app.include_router(UserRoutes.router)
app.include_router(BankRoutes.router)
app.include_router(BudgetRoutes.router)
app.include_router(TransactionRoutes.router)
app.include_router(RegisteredAccountRoutes.router)
# Create database tables
models.Base.metadata.create_all(bind=engine)
    
@app.get("/")
def read_root():
    return {"message": "server is up and running"}


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
