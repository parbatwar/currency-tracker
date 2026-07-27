# Currency Tracker

A Python application that fetches daily exchange rates for NPR against major world currencies, stores them in PostgreSQL, and provides SQL-based analysis of currency trends over time. Runs automatically on a daily schedule.

## Overview

Automates tracking how the Nepali Rupee moves against USD, EUR, and other currencies — useful for import/export businesses, remittance tracking, or personal finance monitoring. Runs unattended once a day via Windows Task Scheduler, building a historical dataset that can be queried with SQL.

## Tech Stack

- **Python 3.9+** — core language
- **exchangerate-api.com** — live exchange rate data source
- **SQLAlchemy** — database ORM
- **PostgreSQL** — storage
- **Loguru** — logging (console + rotating daily log files)
- **python-dotenv** — configuration management
- **Windows Task Scheduler** — daily automated execution

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

Fetch and store today's rates manually:
```bash
python scripts/run.py
```

Run analysis queries against stored data:
```bash
python scripts/query_examples.py
```

## Automation

This pipeline is configured to run automatically once per day via **Windows Task Scheduler**, calling the project's virtual environment Python directly (no manual activation needed):

Program: <project-path>\venv\Scripts\python.exe
Arguments: scripts/run.py
Start in: <project-path>


Each run is logged to a rotating daily log file under `logs/`, so past runs can be reviewed even if the run happened unattended.

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
├── logs/ # Daily rotating log files
├── requirements.txt
└── README.md


## How It Works

1. **Fetch** — calls exchangerate-api.com with NPR as the base currency, retrieves rates for configured target currencies
2. **Store** — saves each currency's rate for the day into PostgreSQL, skipping duplicates if the same day/currency pair already exists
3. **Log** — every run is recorded to a daily log file with timestamps and results
4. **Analyze** — SQL queries find latest rates, average rates, min/max ranges, and total data coverage
5. **Repeat automatically** — Task Scheduler triggers the pipeline daily without manual intervention

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

**Challenge: Running unattended without a persistent background process**
Rather than keeping a Python process running continuously (using memory 24/7), the pipeline is designed to run once, do its job, and exit — triggered externally by Windows Task Scheduler. This is lighter on system resources and mirrors how production cron/scheduled jobs typically work.

## Known Limitations

- Requires the machine to be on and awake at the scheduled time — if the laptop is off or asleep, that day's run is skipped and a gap will appear in the data
- Currently scheduled via local Task Scheduler rather than a cloud-hosted scheduler, so uptime depends on the local machine

## Future Enhancements

- Move scheduling to a cloud environment (e.g. small AWS EC2 instance) to eliminate gaps from local downtime
- Percentage change tracking (day-over-day, week-over-week)
- Alerting when a currency moves beyond a threshold
- Simple visualization dashboard
- FastAPI endpoint to serve the latest rates and trends

## License

MIT