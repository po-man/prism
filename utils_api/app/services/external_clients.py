import httpx
from fastapi import FastAPI

from app.services.worldbank_client import WorldBankClient
from app.services.faostat_client import FaostatClient


class ExternalAPIClients:
    """
    A container for all external API clients, managing a shared httpx.AsyncClient.
    """

    def __init__(self):
        self.http_client = httpx.AsyncClient(timeout=15.0, follow_redirects=True)
        self.worldbank = WorldBankClient(self.http_client)
        self.faostat = FaostatClient(self.http_client)


# Create a singleton instance to be used across the application
external_clients = ExternalAPIClients()


# To manage the async client lifecycle properly with FastAPI
def setup_external_clients_events(app: FastAPI):
    @app.on_event("shutdown")
    async def shutdown_event():
        await external_clients.http_client.aclose()