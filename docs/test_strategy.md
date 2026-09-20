# Test Strategy

The project uses layered testing:

1. Unit-level checks validate password hashing and recommendation behavior through application tests.
2. Flask integration tests exercise registration, login, logout, search, details, and recommendations using isolated SQLite databases.
3. Selenium tests exercise browser workflows with stable `data-testid` selectors. They run headlessly by default and skip clearly when Chrome/WebDriver is unavailable.
4. Manual QA records in `qa/test_cases.csv` cover validation, navigation, security basics, usability, and error handling.

Run application tests with `pytest tests/test_auth.py tests/test_movies.py tests/test_dashboard.py -v`. Run browser tests with `pytest tests/selenium -v`.
