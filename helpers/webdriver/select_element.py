from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select


def select_element_by_visible_text_and_id(driver, element_identifier, text):
    _select_element_by_visible_text(driver, By.ID, element_identifier, text)


def _select_element_by_visible_text(driver, property_identifier, element_identifier, visible_text):
    element = Select(driver.find_element(property_identifier, element_identifier))
    element.select_by_visible_text(visible_text)
