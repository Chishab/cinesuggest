from selenium.webdriver.common.by import By


def test_login_and_logout(browser, live_server):
    browser.get(f"{live_server}/register")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-username"]').send_keys("loginuser")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-email"]').send_keys("login@example.com")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-password"]').send_keys("password123")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-button"]').click()
    browser.find_element(By.CSS_SELECTOR, '[data-testid="login-email"]').send_keys("login@example.com")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys("password123")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]').click()

    assert "Welcome back, loginuser" in browser.page_source
    browser.find_element(By.CSS_SELECTOR, '[data-testid="logout-button"]').click()
    assert "You have been logged out" in browser.page_source


def test_invalid_login(browser, live_server):
    browser.get(f"{live_server}/login")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="login-email"]').send_keys("missing@example.com")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="login-password"]').send_keys("wrong-password")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="login-button"]').click()

    assert "Invalid email or password" in browser.page_source
