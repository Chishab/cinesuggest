# CineSuggest Architecture

CineSuggest uses a Flask application factory with SQLAlchemy and SQLite. Routes handle HTTP concerns, models define persisted data, and services contain reusable recommendation and QA metric logic.

- `app/__init__.py`: application factory and database initialization
- `app/models`: User and Movie entities
- `app/routes`: authentication, catalog, recommendation, and QA dashboard endpoints
- `app/services`: recommendation algorithm and CSV metric aggregation
- `data`: local movie source data
- `qa`: manual test, traceability, defect, and execution records
- `reports`: generated HTML summaries
