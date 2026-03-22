import httpx
from functools import lru_cache
from typing import Optional, Dict


class FaostatClient:
    """
    An asynchronous client for interacting with the FAOSTAT API.
    Provides methods for fetching agricultural data like animal populations.
    """

    # FAO M49 country codes are used by FAOSTAT.
    # This is a partial mapping from ISO3 to M49. A more comprehensive mapping
    # would be needed for global coverage.
    ISO3_TO_M49 = {
        "USA": "840",
        "CHN": "156",
        "IND": "356",
        # Add other relevant countries here
    }

    def __init__(self, client: httpx.AsyncClient):
        self.base_url = "https://fenixservices.fao.org/faostat/api/v1/en/data"
        self.client = client

    @lru_cache(maxsize=256)
    async def get_animal_population(
        self, country_iso3: str, item_code: str, year: int
    ) -> Optional[int]:
        """
        Fetches the population for a specific livestock item code from FAOSTAT.
        Uses the 'QCL' (Live Animals) dataset.

        Args:
            country_iso3: The ISO 3166-1 alpha-3 country code.
            item_code: The FAOSTAT item code for the animal species.
            year: The year for which to fetch the data.

        Returns:
            The animal population as an integer, or None if not found.
        """
        country_m49 = self.ISO3_TO_M49.get(country_iso3.upper())
        if not country_m49:
            print(f"Warning: No M49 code mapping for country {country_iso3}.")
            return None

        url = f"{self.base_url}/QCL"  # QCL is the domain for Live Animals
        params = {
            "area": country_m49,
            "item": item_code,
            "element": "5111",  # 5111 = Stocks
            "year": str(year),
            "fmt": "json",
        }

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if data and data.get("data") and data["data"][0].get("Value"):
                return int(data["data"][0]["Value"])
            return None
        except (httpx.RequestError, IndexError, KeyError, ValueError) as e:
            print(f"Error fetching/parsing FAOSTAT data for {country_iso3}, item {item_code}, {year}: {e}")
            return None