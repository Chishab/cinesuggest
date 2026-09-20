# CineSuggest

CineSuggest is a local Flask movie discovery application with a practical Software Testing and Quality Assurance framework. Users can create accounts, log in securely, browse a seeded movie catalog, search and filter movies, and receive understandable content-based recommendations.

## Features

- Registration, login, logout, validation, duplicate detection, and hashed passwords
- SQLite database managed with SQLAlchemy
- Local movie catalog with title/description search, genre filtering, and sorting
- Movie detail pages
- Token-based cosine similarity recommendations
- Pytest integration tests
- Selenium browser tests with stable selectors and headless support
- 40 manual QA test cases, requirements traceability, execution tracking, and demo defect record
- Flask QA dashboard with Chart.js visualizations
- Generated HTML execution, defect, and QA summary reports

## Technology

Python, Flask, Flask-SQLAlchemy, SQLite, Jinja, Bootstrap 5, JavaScript, Chart.js, pytest, and Selenium WebDriver.

## Setup

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Set a real `SECRET_KEY` in `.env` for anything beyond local demonstration. The default database is `instance/cinesuggest.db`.

## Initialize and Run

Use module form for scripts so imports work consistently on Windows:

```powershell
python -m scripts.init_db
python -m scripts.seed_movies
python app.py
```

Open `http://127.0.0.1:5000`. The catalog is at `/movies`, recommendations at `/recommend`, and the QA dashboard at `/dashboard`.

## Public Deployment

The repository includes `render.yaml` for deployment on Render. Push the project to GitHub, create a Render Web Service from the repository, and use the included blueprint or these commands:

```text
Build Command: pip install -r requirements.txt
Start Command: python -m scripts.init_db && python -m scripts.seed_movies && gunicorn app:app
```

Render will create a public URL such as `https://cinesuggest.onrender.com`. Set `SECRET_KEY` as a generated environment variable and keep `FLASK_DEBUG=0`. The current SQLite database is suitable for a demonstration, but its data can reset on hosts with ephemeral storage. Use a managed PostgreSQL database or persistent disk for a permanent public deployment.

For a temporary demo from your own PC, keep the app running and use a tunnel such as `ngrok http 5001`. Do not expose the Flask development server directly to the internet.

## Tests

Application tests:

```powershell
pytest tests/test_auth.py tests/test_movies.py tests/test_dashboard.py -v
```

All tests, including Selenium:

```powershell
pytest -v
```

Selenium requires Google Chrome. Selenium Manager resolves the driver automatically. Tests run headlessly by default; use `HEADLESS=false` to see the browser. In the current verification environment, Chrome/WebDriver was unavailable, so browser tests were skipped while the 9 application tests passed.

## QA Data and Reports

The `qa` directory contains test cases, the requirements traceability matrix, execution records, defects, and summary metadata. `DEMO-001` is explicitly labeled demonstration data and is not an observed product failure.

Generate reports from the CSV source files:

```powershell
python -m scripts.generate_reports
```

Generated files are written to `reports/`:

- `test_execution_report.html`
- `defect_report.html`
- `qa_summary.html`

## Structure

```text
app/                 Flask factory, models, routes, services, templates, static files
data/                Local movie CSV
scripts/              Database seeding and report generation
qa/                   Test cases, RTM, defects, executions, summary metadata
reports/              Generated HTML reports
tests/                Application and Selenium tests
docs/                 Architecture and QA guidance
instance/             Local SQLite database
```

See `docs/architecture.md`, `docs/test_strategy.md`, `docs/selenium_guide.md`, and `docs/defect_lifecycle.md` for project details.

## Known Limitations

The application is designed for local academic demonstration. It does not include production deployment, email verification, password reset, CSRF middleware, external movie APIs, or multi-user defect editing. Chart.js is loaded from a CDN, so the dashboard needs network access for charts to render.

## Future Improvements

Add Flask-WTF CSRF protection, role-based QA permissions, a larger licensed movie dataset, persistent defect management screens, CI execution, and managed PostgreSQL storage.
