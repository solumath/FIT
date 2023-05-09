from selenium.webdriver.common.by import By
from helper import log_as_admin
import time


@given(u'user is in administration on \'Catalog\' page')
def step_impl(context):
    log_as_admin(context)
    context.driver.find_element(By.LINK_TEXT, "Catalog").click()
    context.driver.find_element(By.LINK_TEXT, "Products").click()

@when(u'user searches for \'Canon EOS 5D\'')
def step_impl(context):
    context.driver.find_element(By.ID, "input-name").send_keys("Canon EOS 5D")
    context.driver.find_element(By.ID, "button-filter").click()

@then(u'item is shown with available stock')
def step_impl(context):
    context.driver.find_element(By.XPATH, "//*[contains(text(), \'Canon EOS 5D\')]").text

@when(u'user selects item')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, "tbody > tr:nth-child(1) .form-check-input").click()


@when(u'clicks \'Delete\'')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, ".fa-trash-can").click()

@then(u'item is deleted')
def step_impl(context):
    assert context.driver.switch_to.alert.text == "Are you sure?"
    context.driver.switch_to.alert.accept()


@when(u'user filters by price \'200\'')
def step_impl(context):
    context.driver.find_element(By.ID, "input-price").send_keys("200")
    context.driver.find_element(By.ID, "button-filter").click()

@then(u'item only \'Samsung SyncMaster 941BW\' is shown')
def step_impl(context):
    first = context.driver.find_element(By.CSS_SELECTOR, "tbody > tr:nth-child(1) > .text-start:nth-child(3)").text
    assert first == "Samsung SyncMaster 941BW"

@when(u'user filters quantity \'xxx\'')
def step_impl(context):
    context.driver.find_element(By.ID, "input-quantity").send_keys("Canon EOS 5D")
    context.driver.find_element(By.ID, "button-filter").click()

@then(u'error should be shown \'Invalid number\'')
def step_impl(context):
    try:
        result = context.driver.find_element(By.XPATH, "//tbody/tr/td[3]").text
    except:
        result = ""
    assert result == ""
    

@when(u'user clicks on edit')
def step_impl(context):
    context.driver.find_element(By.CSS_SELECTOR, "tr:nth-child(1) .btn:nth-child(1)").click()

@when(u'changes quantity of available item')
def step_impl(context):
    context.driver.find_element(By.LINK_TEXT, "Data").click()
    input = context.driver.find_element(By.ID, "input-quantity")
    context.driver.execute_script("arguments[0].scrollIntoView();", input)
    time.sleep(1)
    context.driver.find_element(By.ID, "input-quantity").clear()
    context.driver.find_element(By.ID, "input-quantity").send_keys("960")

@when(u'clicks \'Save\'')
def step_impl(context):
    save = context.driver.find_element(By.CSS_SELECTOR, ".float-end > .btn-primary")
    context.driver.execute_script("arguments[0].scrollIntoView();", save)
    time.sleep(1)
    context.driver.find_element(By.CSS_SELECTOR, ".fa-floppy-disk").click()


@then(u'item is updated')
def step_impl(context):
    quantity = context.driver.find_elements(By.CSS_SELECTOR, "#alert .alert-success")
    assert len(quantity) == 1

