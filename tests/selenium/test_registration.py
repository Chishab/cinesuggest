from selenium.webdriver.common.by import By


def test_registration(browser, live_server):
    browser.get(f"{live_server}/register")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-username"]').send_keys("browseruser")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-email"]').send_keys("browser@example.com")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-password"]').send_keys("password123")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="register-button"]').click()

    assert "Login" in browser.title
    assert "Registration successful" in browser.page_source
