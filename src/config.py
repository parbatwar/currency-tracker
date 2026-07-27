"""
Configuration for currency tracker
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

# PostgreSQL connection
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "currency_tracker")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# API settings
BASE_CURRENCY = os.getenv("BASE_CURRENCY", "NPR")
TARGET_CURRENCIES = os.getenv("TARGET_CURRENCIES", "USD,EUR,INR").split(",")
EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY")
API_URL = (
    f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/{BASE_CURRENCY}"
)


# Logs
LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(exist_ok=True)
