from time import sleep

import pandas as pd


# Selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


URL = 'https://sdatool.inc.hp.com/SDA/SDAOverview/Index'

def closed_sda(sda):
    driver = webdriver.Chrome(executable_path = '../../chromedriver.exe')
    driver.maximize_window()
    driver.get(URL)


    sleep(40)
    driver.implicitly_wait(40)
    search_sda = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="SDAOverviewDataTable_filter"]/label/input')))
    search_sda.send_keys(sda)

    sleep(5)

    details = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'detailsbtn')))
    details.click()

    driver.switch_to.window(driver.window_handles[1])
    sleep(10)

    closure = Select(WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.ID, 'selectClosureCancelDelay'))))
    closure.select_by_visible_text('Cancelled')
    # act_options = [option.text for option in closure.options] 
    # print(act_options)

    sleep(5)

    btn_save_daley_reason = driver.find_element_by_id('btnSaveDR')
    driver.implicitly_wait(10)
    ActionChains(driver).move_to_element(btn_save_daley_reason).click(btn_save_daley_reason).perform()

    sleep(10)
    driver.quit()


def run():
    closed_sda('2208-AMS-AR-EXPD-IM-49689-A')


if __name__ == '__main__':
    run()