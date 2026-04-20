"""
Blockchain API client.

Provides helper functions to fetch blockchain data from public APIs.
"""

import requests

BASE_URL = "https://blockchain.info"
CHARTS_BASE_URL = "https://api.blockchain.info"


def get_latest_block() -> dict:
    """Return the latest block summary."""
    response = requests.get(f"{BASE_URL}/latestblock", timeout=10)
    response.raise_for_status()
    return response.json()


def get_block(block_hash: str) -> dict:
    """Return full details for a block identified by *block_hash*."""
    response = requests.get(
        f"{BASE_URL}/rawblock/{block_hash}", timeout=10
    )
    response.raise_for_status()
    return response.json()


def get_difficulty_history(n_points: int = 100) -> list[dict]:
    """Return the last *n_points* difficulty values as a list of dicts."""
    response = requests.get(
        f"{CHARTS_BASE_URL}/charts/difficulty",
        params={"timespan": "1year", "format": "json", "sampled": "true"},
        timeout=10,
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", "")
    if "application/json" not in content_type.lower():
        raise ValueError("Difficulty endpoint did not return JSON data.")

    data = response.json()
    values = data.get("values", [])
    if not isinstance(values, list):
        raise ValueError("Unexpected difficulty response format.")
    return values[-n_points:]
