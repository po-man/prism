import httpx
from functools import lru_cache
from typing import Optional


class WorldBankClient:
    """
    An asynchronous client for interacting with the World Bank API.
    Provides methods for fetching macroeconomic data like PPP.
    """

    def __init__(self, client: httpx.AsyncClient):
        self.base_url = "https://api.worldbank.org/v2"
        self.client = client

    @lru_cache(maxsize=128)
    async def get_ppp_conversion_factor(
        self, country_code: str, year: int
    ) -> Optional[float]:
        """
        Fetches the Purchasing Power Parity (PPP) conversion factor for a given country and year.
        The indicator 'PA.NUS.PPP' is the PPP conversion factor, LCU per international $.

        Args:
            country_code: The ISO 3166-1 alpha-3 country code.
            year: The year for which to fetch the data.

        Returns:
            The PPP conversion factor as a float, or None if not found.
        """
        url = f"{self.base_url}/country/{country_code}/indicator/PA.NUS.PPP"
        params = {"format": "json", "date": str(year)}

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if not data or len(data) < 2 or not data[1]:
                print(f"Warning: No PPP data found for {country_code} in {year}.")
                return None

            # The first element is metadata, the second contains the data records
            for record in data[1]:
                if record.get("value") is not None:
                    return float(record["value"])

            return None
        except httpx.HTTPStatusError as e:
            print(f"Error fetching PPP data from World Bank for {country_code}, {year}: {e}")
            return None
        except (ValueError, TypeError, IndexError) as e:
            print(f"Error parsing PPP data for {country_code}, {year}: {e}")
            return None