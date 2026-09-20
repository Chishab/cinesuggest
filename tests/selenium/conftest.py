import os
import threading
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from werkzeug.serving import make_server

from app import create_app, db
from app.models.movie import Movie


@pytest.fixture(scope="session")
def live_app(tmp_path_factory):
    class TestConfig:
        TESTING = True
        SECRET_KEY = "selenium-test-secret"
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{tmp_path_factory.mktemp('selenium') / 'test.db'}"
        SQLALCHEMY_TRACK_MODIFICATIONS = False

    application = create_app(TestConfig)
    with application.app_context():
        db.session.add_all([
            Movie(title="The Last Orbit", genre="Sci-Fi", description="A pilot explores a distant planet.", year=2023, rating=8.4, director="Ava Chen"),
            Movie(title="Midnight Signal", genre="Sci-Fi", description="An engineer follows a mysterious signal.", year=2022, rating=7.9, director="Noah Brooks"),
        ])
        db.session.commit()
    return application


@pytest.fixture(scope="session")
def live_server(live_app):
    server = make_server("127.0.0.1", 0, live_app)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()
    thread.join()


@pytest.fixture()
def browser():
    options = Options()
    if os.getenv("HEADLESS", "true").lower() == "true":
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1440,1000")
    try:
        driver = webdriver.Chrome(options=options)
    except WebDriverException as error:
        pytest.skip(f"Chrome/WebDriver unavailable: {error}")
    yield driver
    driver.quit()
