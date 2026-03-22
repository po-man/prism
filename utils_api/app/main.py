from fastapi import FastAPI
from app.routers import validation, audit, url_resolver, provenance
from app.services.pocketbase_client import setup_pocketbase_client_events
from app.services.external_clients import setup_external_clients_events

app = FastAPI(
    title="Prism Utils API",
    description="A microservice for data validation and analytics computation.",
    version="1.0.0",
)
# Setup client lifecycle events
setup_pocketbase_client_events(app)
setup_external_clients_events(app)

# Include API routers
app.include_router(validation.router)
app.include_router(audit.router)
app.include_router(url_resolver.router)
app.include_router(provenance.router)