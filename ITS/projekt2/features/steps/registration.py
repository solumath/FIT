from behave import *
from selenium.webdriver.common.by import By
import time
    
@given(u'user is on registration')
def step_impl(context):
    context.driver.get(context.base_url + "/en-gb?route=account/register")

@given(u'user is not logged in')
def step_impl(context):
    logged = False if context.driver.find_elements(By.LINK_TEXT, "Login") else True
    if logged:
        context.driver.find_element(By.XPATH, "//span[contains(text(),'My Account')]").click()
        context.driver.find_element(By.LINK_TEXT, "Logout").click()

@when(u'user fills all required fields')
def step_impl(context):
    context.driver.get(context.base_url + "/en-gb?route=account/register")
    context.driver.find_element(By.ID, "input-firstname").click()
    context.driver.find_element(By.ID, "input-firstname").send_keys("Jana")
    context.driver.find_element(By.ID, "input-lastname").click()
    context.driver.find_element(By.ID, "input-lastname").send_keys("Nováková")
    context.driver.find_element(By.ID, "input-email").click()
    context.driver.find_element(By.ID, "input-email").send_keys("jana.novakova@seznam.cz")
    context.driver.find_element(By.ID, "input-password").click()
    context.driver.find_element(By.ID, "input-password").send_keys("1234")

@when(u'checks \'I have read and agree...\'')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//input[@name='agree']").click()
    context.driver.find_element(By.XPATH, "//button[contains(.,'Continue')]").click()

@then(u'page with \'Your Account Has Been Created!\' is shown')
def step_impl(context):
    text = context.driver.find_element(By.XPATH, "//h1[contains(.,'Your Account Has Been Created!')]").text
    assert(text == "Your Account Has Been Created!")


@given(u'user is logged in')
def step_impl(context):
    context.driver.get(context.base_url + "/en-gb?route=account/login")
    logged = True if context.driver.find_elements(By.XPATH, "//h2[contains(.,'My Account')]") else False
    if not logged:
        context.driver.find_element(By.ID, "input-email").send_keys("jan.novak@seznam.cz")
        context.driver.find_element(By.ID, "input-password").send_keys("1234")
        context.driver.find_element(By.XPATH, "//button[@type='submit']").click()

@given(u'user is on \'My account\'')
def step_impl(context):
    context.driver.get(context.base_url + "/en-gb?route=account/login")
    time.sleep(1)

@when(u'user clicks \'Order History\'')
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, "Order History").click()
    time.sleep(1)

@then(u'user sees his order with status \'Pending\'')
def step_impl(context):
    pending = True if context.driver.find_elements(By.XPATH, "//tbody/tr/td[4]") else False
    assert pending == True