"""
Database operations for currency tracker
"""

from datetime import date
from loguru import logger

from .models import SessionLocal, ExchangeRate, init_db


class Database:
    def __init__(self):
        init_db()
        self.session = SessionLocal()

    def save_rates(self, rates, base_currency="NPR"):
        """Save today's rates to the database"""
        today = date.today()
        saved = 0

        for target, rate in rates.items():
            # Avoid duplicate entry for the same day + currency pair
            existing = (
                self.session.query(ExchangeRate)
                .filter_by(
                    date=today, base_currency=base_currency, target_currency=target
                )
                .first()
            )
            if existing:
                continue

            record = ExchangeRate(
                date=today,
                base_currency=base_currency,
                target_currency=target,
                rate=rate,
            )
            self.session.add(record)
            saved += 1

        self.session.commit()
        logger.success(f"Saved {saved} new rate records for {today}")
        return saved

    def get_history(self, target_currency, limit=30):
        """Get rate history for a currency"""
        return (
            self.session.query(ExchangeRate)
            .filter_by(target_currency=target_currency)
            .order_by(ExchangeRate.date.desc())
            .limit(limit)
            .all()
        )
