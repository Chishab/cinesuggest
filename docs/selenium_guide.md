# Selenium Guide

Install dependencies with `pip install -r requirements.txt`. Ensure Google Chrome is installed; Selenium Manager resolves the compatible driver. Set `HEADLESS=false` to see the browser window.

Run `pytest tests/selenium -v`. The fixture starts an isolated Flask server and SQLite database, seeds two movies, and closes the server after the session.
