from typing import List

from selenium.webdriver.common.by import By


def find_element_by_id_and_send_keys(driver, element_identifier, keys: List):
    _find_element_and_send_keys(driver, By.ID, element_identifier, keys)


def find_element_by_xpath_and_send_keys(driver, element_identifier, keys):
    _find_element_and_send_keys(driver, By.XPATH, element_identifier, keys)


def _find_element_and_send_keys(driver, property_identifier, element_identifier, keys):
    element = driver.find_element(property_identifier, element_identifier)
    for key in keys:
        element.send_keys(key)


def find_element_by_id_and_click_it_with_javascript(driver, element_identifier):
    _find_element_and_click_it_with_javascript(driver, By.ID, element_identifier)


def find_element_by_xpath_and_click_it_with_javascript(driver, element_identifier):
    _find_element_and_click_it_with_javascript(driver, By.XPATH, element_identifier)


def _find_element_and_click_it_with_javascript(driver, property_identifier, element_identifier):
    element = driver.find_element(property_identifier, element_identifier)
    driver.execute_script("arguments[0].click();", element)
