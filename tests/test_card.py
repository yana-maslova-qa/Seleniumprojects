import pytest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver. support.wait import WebDriverWait

URL = 'https://test-shop.qa.studio/'

def test_product_view_sku(browser):
    """
    TMS-4: [web][use case] Проверка выбора товара (журнальный столик)
    """
    browser.get(url=URL)
    print("test")

    element = browser.find_element(by=By.CSS_SELECTOR, value='[class*="tab-best_sellers"]')
    element.click()

    element = browser.find_element(by=By.CSS_SELECTOR, value='[class*="post-11341"]')
    element.click()

    sku = browser.find_element(By.CLASS_NAME, value="sku")
    
    assert sku.text == ' ', 'Unexpected sku'