from functools import wraps
from environment import wait_time
from selenium.webdriver.common.by import By
import time

def remove_wait(func):
    """Decorator to remove implicit wait for a function when looking for non existent elements"""
    @wraps(func)
    def wrapper(context, *args, **kwargs):
        context.driver.implicitly_wait(0)
        func(context, *args, **kwargs)
        context.driver.implicitly_wait(wait_time)
    return wrapper

@remove_wait
def empty_cart(context):
    context.driver.find_element(By.XPATH, "//li[4]/a/span").click()
    elements = context.driver.find_elements(By.CLASS_NAME, "btn btn-danger")
    if len(elements) > 0:
        for button in elements:
            button.click()
    context.driver.get(context.base_url)

def item_to_cart(context):
    """Add item to cart"""
    context.driver.get(context.base_url)
    context.driver.find_element(By.LINK_TEXT, "iPhone").click()
    context.driver.find_element(By.ID, "button-cart").click()
    context.driver.get(context.base_url)

def scroll(context, key):
    """Scroll to bottom of page"""
    context.driver.find_element(By.TAG_NAME, "body").send_keys(key)
    time.sleep(0.5)

def log_as_admin(context):
    """Log in as admin"""
    context.driver.get(context.base_url + "/administration")
    time.sleep(1)
    context.driver.find_element(By.ID, "input-username").send_keys("user")
    context.driver.find_element(By.ID, "input-password").send_keys("bitnami")
    context.driver.find_element(By.XPATH, "//button[contains(.,' Login')]").click()