# Currency Tracker

A Python application that fetches daily exchange rates for NPR against major world currencies, stores them in PostgreSQL, and provides SQL-based analysis of currency trends over time.

## Overview

Automates tracking how the Nepali Rupee moves against USD, EUR, and other currencies — useful for import/export businesses, remittance tracking, or personal finance monitoring. Instead of manually checking exchange rates, this runs on demand (or on a schedule) and builds a historical dataset you can query.

## Tech Stack

- **Python 3.9+** — core language
- **exchangerate-api.com** — live exchange rate data source
- **SQLAlchemy** — database ORM
- **PostgreSQL** — storage
- **Loguru** — logging
- **python-dotenv** — configuration management

## Installation

```bash
git clone https://github.com/parbatwar/currency-tracker.git
cd currency-tracker

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env
```

Update `.env` with your PostgreSQL credentials and a free API key from [exchangerate-api.com](https://www.exchangerate-api.com/).

Create the database:
```bash
psql -U postgres
CREATE DATABASE currency_tracker;
```

## Usage

Fetch and store today's rates:
```bash
python scripts/run.py
```

Run analysis queries against stored data:
```bash
python scripts/query_examples.py
```

## Project Structure
currency-tracker/
├── src/
│ ├── fetcher.py # API calls to exchangerate-api.com
│ ├── database.py # Database read/write operations
│ ├── models.py # SQLAlchemy models
│ └── config.py # Configuration
├── scripts/
│ ├── run.py # Fetch and store today's rates
│ └── query_examples.py # SQL analysis queries
├── requirements.txt
└── README.md

## How It Works

1. **Fetch** — calls exchangerate-api.com with NPR as the base currency, retrieves rates for configured target currencies (USD, EUR, INR)
2. **Store** — saves each currency's rate for the day into PostgreSQL, skipping duplicates if the same day/currency pair already exists
3. **Analyze** — runs SQL queries to find latest rates, average rates, min/max ranges, and total data coverage

## Example Queries Included

- Latest rate per currency (using a subquery to find the most recent date per currency)
- Average rate per currency across all recorded history
- Min/max rate range per currency
- Total record count and date range covered

## Challenges & Solutions

**Challenge: NPR not supported by all exchange rate APIs**
Many free currency APIs (like Frankfurter) don't include NPR. Solved by switching to exchangerate-api.com, which supports NPR as a base currency.

**Challenge: Avoiding duplicate daily records**
Running the script multiple times in a day could create duplicate rows. Solved by checking for an existing record (same date + currency pair) before inserting.

## Future Enhancements

- Scheduled daily runs (cron)
- Percentage change tracking (day-over-day, week-over-week)
- Alerting when a currency moves beyond a threshold
- Simple visualization dashboard

## License

MIT