from fastapi import FastAPI
from app.routers import validation, audit

app = FastAPI(
    title="Prism Utils API",
    description="A microservice for data validation and analytics computation.",
    version="1.0.0"
)

app.include_router(validation.router)
app.include_router(audit.router)