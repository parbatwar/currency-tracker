import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from loguru import logger
from src.config import LOGS_DIR

logger.add(
    LOGS_DIR / "run_{time:YYYY-MM-DD}.log", rotation="1 day", retention="30 days"
)

from src.fetcher import fetch_rates
from src.database import Database


def main():
    print("\n" + "=" * 50)
    print("CURRENCY TRACKER")
    print("=" * 50)

    logger.info("Fetching latest exchange rates...")
    rates = fetch_rates()

    if not rates:
        logger.error("Failed to fetch rates. Check API key and connection.")
        print("Failed to fetch rates. Check your API key and connection.")
        return

    db = Database()
    saved = db.save_rates(rates)

    logger.success(f"Run complete. Rates: {rates}, new records: {saved}")
    print(f"\nRates fetched: {rates}")
    print(f"New records saved: {saved}")
    print("=" * 50)


if __name__ == "__main__":
    main()
