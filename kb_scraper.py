import sys
import requests
import csv # for debugging
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By

import getpass # for password input

# from selenium.webdriver.firefox.service import Service #? For Firefox browsers
from selenium.webdriver.chrome.service import Service #? For Chrome browsers

sys.path.append("./chromedriver_win64") #? Add chromedriver to path



def get_driver(service = "chrome") -> webdriver.Chrome | webdriver.Firefox:
    if service.lower() == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.Chrome()
    return driver


# testing for now
def log_in(username, password) -> webdriver.Chrome | webdriver.Firefox:
    # login url for KB:
    url = r"https://stolafcarleton.teamdynamix.com/SBTDClient/2092/Carleton/Login.aspx?ReturnUrl=%2fSBTDClient%2f2092%2fCarleton%2fHome%2f"
    
    # Cleaning username:
    if "@carleton.edu" != username[-13:]:
        username += "@carleton.edu"
        
    # Load driver:  
    driver = get_driver()
    driver.get(url)
    driver.maximize_window()
    
    # Log in:
    driver.find_element(By.ID, "txtUserName").send_keys(username)
    driver.find_element(By.ID, "txtPassword").send_keys(password)
    driver.find_element(By.ID, "btnSignIn").click()
    
    return driver

# True if deleted, False if not.
def delete_article(driver: webdriver.Chrome | webdriver.Firefox, article_id: int, base_url: str = None) -> bool:
    if not base_url:
        base_url = r"https://stolafcarleton.teamdynamix.com/SBTDClient/2092/Carleton/KB/EditDetails"
    
    driver.get(base_url + f"?ID={article_id}")
        
    delete = driver.find_element(By.ID, "ctl00_ctl00_ctl00_cpContent_cpContent_btnDeleteArticle")
    # Are we allowed/able to delete?
    if not delete:
        return False
    # Click delete:
    delete.click()
    driver.switch_to.alert.accept()
    time.sleep(5)
    return True
            

def main(username, password):
    driver = log_in(username, password)
    delete_article(driver, 143859)
    
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = r''.join(sys.argv[1])
    else:
        url = r"https://stolafcarleton.teamdynamix.com/SBTDClient/2092/Carleton/KB/"

    username = input("Carleton username: ")
    password = getpass.getpass("Carleton password: ")
    
    main(url, username, password)