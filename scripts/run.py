"""
Main entry point — fetch and store today's exchange rates
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.fetcher import fetch_rates
from src.database import Database
from loguru import logger


def main():
    print("\n" + "=" * 50)
    print("CURRENCY TRACKER")
    print("=" * 50)

    logger.info("Fetching latest exchange rates...")
    rates = fetch_rates()

    if not rates:
        print("Failed to fetch rates. Check your API key and connection.")
        return

    db = Database()
    saved = db.save_rates(rates)

    print(f"\nRates fetched: {rates}")
    print(f"New records saved: {saved}")
    print("=" * 50)


if __name__ == "__main__":
    main()
