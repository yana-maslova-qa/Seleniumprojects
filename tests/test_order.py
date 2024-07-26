import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver. support.wait import WebDriverWait
from selenium.webdriver. support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from helper.common import CommonHelper

URL = 'https://test-shop.qa.studio/'

def test_browser(browser):
    """
    TMS-1: [web][catalig] Проверка SKU товара 
    """

    browser.get(url=URL)

    browser.find_element(By.CSS_SELECTOR, value='[class*="post-11345"]').click()

    sku = browser.find_element(By.CLASS_NAME, value='sku')

    assert sku.text == 'J4W5ADY72', 'Unexpected SKU'


def test_count_of_all_products(browser):
    """
    TMS-2: [web][scroll] Проверка колличества товаров
    """

    browser.get(url=URL)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    text_to_be_present_in_element = EC.text_to_be_present_in_element((By.CLASS_NAME, 'razzi-posts__found-inner'), 'Показано 17 из 17 товары')

    browser.save_screenshot('screenshot1_with_headless.png')
    t1 = WebDriverWait(browser, timeout=60, poll_frequency=2)

    browser.save_screenshot('screenshot2_with_headless.png')
    t1.until(text_to_be_present_in_element)

    browser.save_screenshot('screenshot3_with_headless.png')
    elements = browser.find_elements(by=By.CSS_SELECTOR, value="[id='rz-shop-content'] ul li")

    assert len(elements) == 17, "Unexpected count of products"

def test_right_way(browser):
    """
    TMS-3: [web][use case] Проверка покупки товара
    """  
    browser.get(url=URL)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    text_to_be_present_in_element = EC.text_to_be_present_in_element((By.CLASS_NAME, 'razzi-posts__found-inner'), 'Показано 17 из 17 товары')

    browser.save_screenshot('screenshot4_with_headless.png')

    t1 = WebDriverWait(browser, timeout=30, poll_frequency=2)

    browser.save_screenshot('screenshot5_with_headless.png')

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    t1.until(text_to_be_present_in_element)

    product = browser.find_element(by=By.CSS_SELECTOR, value="[class*='post-11345'] a")
    ActionChains(browser).move_to_element(product).perform()
    product.click()

    WebDriverWait(browser, timeout=60, poll_frequency=2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '[name="add-to-cart"]')))

    browser.find_element(by=By.CSS_SELECTOR, value='[name="add-to-cart"]').click()

    WebDriverWait(browser, timeout=60, poll_frequency=2).until(
        EC.visibility_of_element_located((By.XPATH, "//div[@id='cart-modal']")))
    
    cart_is_visible = browser.find_element(
        By.XPATH, value="//div[@id='cart-modal']").value_of_css_property("display")
    assert cart_is_visible == "block", "Unexpected state of cart"

    browser.find_element(by=By.CSS_SELECTOR, value='p [class*="button checkout"]').click()

    WebDriverWait(browser, timeout=10, poll_frequency=1).until(EC.url_to_be(f"{URL}checkout/"))

    common_helper = CommonHelper(browser)
    common_helper.enter_input(input_id="billing_first_name", data="Alina")
    common_helper.enter_input(input_id="billing_last_name", data="Zhvakina")
    common_helper.enter_input(input_id="billing_address_1", data="2-10, Privoksalnaya street")
    common_helper.enter_input(input_id="billing_city", data="Krasnodar")
    common_helper.enter_input(input_id="billing_state", data="Krasnodar")
    common_helper.enter_input(input_id="billing_postcode", data="350016")
    common_helper.enter_input(input_id="billing_phone", data="+79990552269")
    common_helper.enter_input(input_id="billing_email", data="alina@gmail.com")

    browser.find_element(by=By.ID, value="place_order").click()

    WebDriverWait(browser, timeout=10, poll_frequency=1).until(EC.url_contains(f"{URL}checkout/order-received/"))

    result = WebDriverWait(browser, timeout=10, poll_frequency=2).until(
        EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "p.woocommerce-thankyou-order-received"), \
                "Ваш заказ принят. Благодарим вас."))

    assert result, 'Unexpected notification text'