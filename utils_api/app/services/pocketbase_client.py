import os
from functools import lru_cache
from typing import Any, Dict, List
import httpx
from fastapi import HTTPException
import asyncio


class PocketBaseClient:
    """
    A client for interacting with the PocketBase data vault.
    Handles authentication and provides cached methods for fetching reference data.
    """

    def __init__(self):
        self.pb_url = os.getenv("POCKETBASE_URL", "http://127.0.0.1:8090")
        self.admin_email = os.getenv("POCKETBASE_ADMIN_EMAIL")
        self.admin_password = os.getenv("POCKETBASE_ADMIN_PASSWORD")
        self.token: str | None = None
        self.client = httpx.AsyncClient(base_url=self.pb_url, timeout=10.0)
        # In a real-world async app, authentication might be better handled
        # during app startup events rather than a synchronous __init__.
        # For this refactoring, we'll authenticate on first use.

    async def _authenticate(self):
        """Authenticates with the PocketBase admin account."""
        if self.token:
            return  # Already authenticated

        if not self.admin_email or not self.admin_password:
            print("WARNING: PocketBase admin credentials are not set. Client will be unauthenticated.")
            return

        try:
            auth_url = "/api/collections/_superusers/auth-with-password"
            payload = {"identity": self.admin_email, "password": self.admin_password}
            response = await self.client.post(auth_url, json=payload)
            response.raise_for_status()
            self.token = response.json().get("token")
            print("Successfully authenticated with PocketBase.")
        except httpx.HTTPStatusError as e:
            print(f"FATAL: Could not authenticate with PocketBase at {self.pb_url}. Error: {e}")
            raise HTTPException(status_code=503, detail=f"Could not connect to data vault: {e}")
        except httpx.RequestError as e:
            print(f"FATAL: Network error while authenticating with PocketBase at {self.pb_url}. Error: {e}")
            raise HTTPException(status_code=503, detail=f"Network error connecting to data vault: {e}")

    async def _get_full_list(self, collection_name: str) -> List[Dict[str, Any]]:
        """Fetches all records from a collection."""
        await self._authenticate()
        headers = {"Authorization": f"Bearer {self.token}"} if self.token else {}
        try:
            response = await self.client.get(f"/api/collections/{collection_name}/records", headers=headers, params={"perPage": 500})
            response.raise_for_status()
            return response.json().get("items", [])
        except httpx.HTTPStatusError as e:
            print(f"Error fetching collection '{collection_name}': {e}")
            return []
        except httpx.RequestError as e:
            print(f"Network error fetching collection '{collection_name}': {e}")
            return []

    @lru_cache(maxsize=1)
    async def get_moral_weights(self) -> Dict[str, float]:
        """Fetches and caches moral weights, mapping species_key to weight."""
        records = await self._get_full_list("ref_moral_weights")
        return {record.get("species_key"): record.get("weight") for record in records}

    @lru_cache(maxsize=1)
    async def get_evidence_discounts(self) -> Dict[str, float]:
        """Fetches and caches evidence discounts, mapping evidence_key to multiplier."""
        records = await self._get_full_list("ref_evidence_discounts")
        return {record.get("evidence_key"): record.get("multiplier") for record in records}

    @lru_cache(maxsize=1)
    async def get_intervention_baselines(self) -> Dict[str, float]:
        """Fetches and caches intervention baselines, mapping intervention_key to probability."""
        records = await self._get_full_list("ref_intervention_baselines")
        return {record.get("intervention_key"): record.get("baseline_probability") for record in records}


# Create a singleton instance to be used across the application
pb_client = PocketBaseClient()

# To manage the async client lifecycle properly with FastAPI
from fastapi import FastAPI

def setup_pocketbase_client_events(app: FastAPI):
    @app.on_event("shutdown")
    async def shutdown_event():
        await pb_client.client.aclose()