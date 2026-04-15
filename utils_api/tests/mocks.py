"""
This module contains mock objects for testing purposes, allowing for the simulation
of external services like the PocketBase client.
"""

from typing import Any, Dict


class MockPocketBaseClient:
    """
    A mock of the PocketBaseClient that returns predefined data for testing
    without making actual HTTP requests.
    """

    def __init__(self):
        pass

    async def get_moral_weights(self) -> Dict[str, float]:
        """Returns mock moral weights."""
        return {
            "chicken": 1.0,
            "dog": 0.5,
            "songbird": 0.1,
            "generic_companion": 0.5,
            "generic_farmed": 0.5,
            "generic_wild": 0.1,
            "generic_unspecified": 0.1,
        }

    async def get_evidence_discounts(self) -> Dict[str, float]:
        """Returns mock evidence discounts."""
        return {"RCT/Meta-Analysis": 1.0, "Quasi-Experimental": 0.8, "Pre-Post": 0.6, "Anecdotal": 0.3, "None": 0.0}

    async def get_intervention_baselines(self) -> Dict[str, float]:
        """Returns mock intervention baselines."""
        return {
            "corporate_welfare_campaigns": 0.8,
            "individual_rescue_and_sanctuary": 0.2,
            "high_volume_spay_neuter": 0.9,
        }