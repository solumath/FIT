#!/usr/bin/env python3
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


base_url = "http://opencart:8080/"
wait_time = 5

def get_driver():
    '''Get Chrome/Firefox driver from Selenium Hub'''
    try:
        driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.CHROME)
    except WebDriverException:
        driver = webdriver.Remote(
                command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.FIREFOX)
    driver.implicitly_wait(wait_time)
    return driver

def before_all(context):
    time.sleep(wait_time*4)
    context.driver = get_driver()
    context.base_url = base_url

def after_all(context):
    context.driver.quit()
