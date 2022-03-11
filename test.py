import time
from selenium import webdriver
from selenium.webdriver.common.by import By


def loginToomics():
    dri = webdriver.Chrome()
    dri.get('https://global.toomics.com')
    dri.find_element(By.ID, 'toggle-login').click()
    dri.find_element(By.XPATH, "//div[@class='section_sns_sign_wrap01']/button").click()
    dri.find_element(By.ID, 'user_id').send_keys('fantimeng@gmail.com')
    dri.find_element(By.ID, 'user_pw').send_keys('ti199058')
    dri.find_element(By.XPATH, "//fieldset[@id='login_fieldset']/button").click()
    dri.find_element(By.CLASS_NAME, 'section_19plus')

loginToomics()
