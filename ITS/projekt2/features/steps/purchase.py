from behave import *
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from helper import empty_cart, item_to_cart, scroll
import time
    
@given(u'user is on index page')
def step_impl(context):
    context.driver.get(context.base_url)

# 1. Search for product
@when(u'user searches for \'macbook\'')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//input[@name='search']").click()
    context.driver.find_element(By.XPATH, "//input[@name='search']").send_keys("macbook")
    context.driver.find_element(By.XPATH, "//input[@name='search']").send_keys(Keys.ENTER)

@then(u'page with following products is shown')
def step_impl(context):
    context.driver.implicitly_wait(5)
    macbook = context.driver.find_element(By.XPATH, "//a[contains(text(),\'MacBook\')]").text
    macbook_air = context.driver.find_element(By.XPATH, "//a[contains(text(),\'MacBook Air\')]").text
    macbook_pro = context.driver.find_element(By.XPATH, "//a[contains(text(),\'MacBook Pro\')]").text
    for row in context.table:
        assert(row['product'] in [macbook, macbook_air, macbook_pro])

# 2. Add product to cart
@given(u'user has empty cart')
def step_impl(context):
    empty_cart(context)

@when(u'user clicks \'Add to cart\'')
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, "MacBook").click()
    context.driver.find_element(By.ID, "button-cart").click()

@then(u'user sees item in cart')
def step_impl(context):
    context.driver.get(context.base_url)
    context.driver.find_element(By.XPATH, "//li[4]/a/span").click()
    item = context.driver.find_element(By.LINK_TEXT, "MacBook").text
    assert(item == "MacBook")

# 4. Remove product from cart
@given(u'user is on \'Shopping cart\' page')
def step_impl(context):
    context.driver.get(context.base_url + "/en-gb?route=checkout/cart")

@given(u'user has item in cart')
def step_impl(context):
    product = context.driver.find_elements(By.XPATH, "//td[contains(.,'Product Name')]")
    assert len(product) == 1

@when(u'user clicks \'Remove\' on item')
def step_impl(context):
    empty_cart(context)

@then(u'item is removed from cart')
def step_impl(context):
    context.driver.get(context.base_url + "/en-gb?route=checkout/cart")
    product = context.driver.find_elements(By.XPATH, "//td[contains(.,'Product 16')]")
    assert product[0].text == "Product 16"

# 5. Checkout
@given(u'user is on \'Checkout\' page')
def step_impl(context):
    item_to_cart(context)
    context.driver.get(context.base_url + "/en-gb?route=checkout/checkout")

@when(u'user fills required fields')
def step_impl(context):
    context.driver.find_element(By.ID, "input-firstname").click()
    context.driver.find_element(By.ID, "input-firstname").send_keys("Jan")
    context.driver.find_element(By.ID, "input-lastname").click()
    context.driver.find_element(By.ID, "input-lastname").send_keys("Novák")
    context.driver.find_element(By.ID, "input-email").click()
    context.driver.find_element(By.ID, "input-email").send_keys("jan.novak@seznam.cz")
    context.driver.find_element(By.ID, "input-shipping-address-1").click()
    context.driver.find_element(By.ID, "input-shipping-address-1").send_keys("Božetěchova 1")
    context.driver.find_element(By.ID, "input-shipping-city").click()
    context.driver.find_element(By.ID, "input-shipping-city").send_keys("Brno")
    context.driver.find_element(By.ID, "input-shipping-postcode").click()
    context.driver.find_element(By.ID, "input-shipping-postcode").send_keys("60200")
    context.driver.find_element(By.ID, "input-shipping-country").click()
    dropdown = context.driver.find_element(By.ID, "input-shipping-country")
    dropdown.find_element(By.XPATH, "//option[. = 'Czech Republic']").click()
    scroll(context, Keys.PAGE_DOWN)
    context.driver.find_element(By.ID, "input-shipping-zone").click()
    dropdown = context.driver.find_element(By.ID, "input-shipping-zone")
    dropdown.find_element(By.XPATH, "//option[. = 'Jihomoravský']").click()
    context.driver.find_element(By.CSS_SELECTOR, "#input-shipping-zone > option:nth-child(3)").click()
    context.driver.find_element(By.ID, "input-password").click()
    context.driver.find_element(By.ID, "input-password").send_keys("1234")
    context.driver.find_element(By.ID, "input-register-agree").click()
    scroll(context, Keys.PAGE_DOWN)
    context.driver.find_element(By.ID, "button-register").click()
    scroll(context, Keys.PAGE_UP)
    context.driver.find_element(By.ID, "button-shipping-methods").click()
    context.driver.find_element(By.CSS_SELECTOR, ".form-check:nth-child(3) > label").click()
    context.driver.find_element(By.ID, "button-shipping-method").click()
    context.driver.find_element(By.ID, "button-payment-methods").click()
    context.driver.find_element(By.CSS_SELECTOR, "#form-payment-method label").click()
    context.driver.find_element(By.ID, "button-payment-method").click()
    scroll(context, Keys.PAGE_DOWN)
    scroll(context, Keys.PAGE_DOWN)

@when(u'clicks on \'Confirm order\'')
def step_impl(context):
    context.driver.find_element(By.ID, "button-confirm").click()

@then(u'user is logged in and \'Order has been placed\' is shown')
def step_impl(context):
    logged = True if context.driver.find_elements(By.XPATH, "//a[contains(.,'Login')]") else False
    order = context.driver.find_element(By.XPATH, "//h1[contains(.,'Your order has been placed!')]").text
    assert (logged == True) and (order == "Your order has been placed!")

