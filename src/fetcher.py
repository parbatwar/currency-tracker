"""
Fetches exchange rate data from exchangerate-api.com
"""

import requests
from loguru import logger

from .config import API_URL, TARGET_CURRENCIES


def fetch_rates():
    """Fetch current exchange rates with NPR as base"""
    try:
        response = requests.get(API_URL, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("result") != "success":
            logger.error(f"API returned error: {data}")
            return None

        all_rates = data.get("conversion_rates", {})
        filtered = {
            curr: all_rates[curr] for curr in TARGET_CURRENCIES if curr in all_rates
        }

        logger.success(f"Fetched rates: {filtered}")
        return filtered

    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch rates: {e}")
        return None
