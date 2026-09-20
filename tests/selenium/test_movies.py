from selenium.webdriver.common.by import By


def test_search_details_and_recommendations(browser, live_server):
    browser.get(f"{live_server}/movies")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="movie-search"]').send_keys("Orbit")
    browser.find_element(By.CSS_SELECTOR, '[data-testid="search-button"]').click()
    assert "The Last Orbit" in browser.page_source

    browser.find_element(By.LINK_TEXT, "The Last Orbit").click()
    assert "A pilot explores a distant planet" in browser.page_source
    browser.find_element(By.CSS_SELECTOR, '[data-testid="recommend-button"]').click()
    assert "Midnight Signal" in browser.page_source
