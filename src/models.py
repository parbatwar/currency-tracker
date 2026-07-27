"""
Database models for currency tracker
"""

from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, Date
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import DATABASE_URL

Base = declarative_base()


class ExchangeRate(Base):
    """Exchange rate record"""

    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    rate = Column(Float, nullable=False)
    fetched_at = Column(Date, default=datetime.now)

    def __repr__(self):
        return (
            f"<ExchangeRate {self.base_currency}->{self.target_currency}: {self.rate}>"
        )


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def init_db():
    """Create tables"""
    Base.metadata.create_all(engine)
    print("Database tables created")
