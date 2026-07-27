"""
Example SQL queries against the currency tracker database
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import func
from src.models import SessionLocal, ExchangeRate


def main():
    session = SessionLocal()

    print("\n" + "=" * 50)
    print("CURRENCY TRACKER — ANALYSIS")
    print("=" * 50)

    # 1. Latest rate for each currency
    print("\nLatest rates:")
    subq = (
        session.query(
            ExchangeRate.target_currency,
            func.max(ExchangeRate.date).label("max_date"),
        )
        .group_by(ExchangeRate.target_currency)
        .subquery()
    )

    latest = (
        session.query(ExchangeRate)
        .join(
            subq,
            (ExchangeRate.target_currency == subq.c.target_currency)
            & (ExchangeRate.date == subq.c.max_date),
        )
        .all()
    )
    for r in latest:
        print(f"   NPR -> {r.target_currency}: {r.rate} (as of {r.date})")

    # 2. Average rate per currency (all-time)
    print("\nAverage rate per currency:")
    avg_rates = (
        session.query(
            ExchangeRate.target_currency,
            func.avg(ExchangeRate.rate).label("avg_rate"),
        )
        .group_by(ExchangeRate.target_currency)
        .all()
    )
    for currency, avg in avg_rates:
        print(f"   {currency}: {avg:.6f}")

    # 3. Min/Max rate per currency
    print("\nRate range per currency:")
    ranges = (
        session.query(
            ExchangeRate.target_currency,
            func.min(ExchangeRate.rate).label("min_rate"),
            func.max(ExchangeRate.rate).label("max_rate"),
        )
        .group_by(ExchangeRate.target_currency)
        .all()
    )
    for currency, min_r, max_r in ranges:
        print(f"   {currency}: min={min_r:.6f}, max={max_r:.6f}")

    # 4. Total records and date range
    total = session.query(ExchangeRate).count()
    earliest = session.query(func.min(ExchangeRate.date)).scalar()
    latest_date = session.query(func.max(ExchangeRate.date)).scalar()

    print(f"\nTotal records: {total}")
    print(f"Date range: {earliest} to {latest_date}")
    print("=" * 50)


if __name__ == "__main__":
    main()
