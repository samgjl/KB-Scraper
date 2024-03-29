import sys
import pandas
from tqdm import tqdm
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass # for password input

class KBScraper:
    def __init__(self, username: str = "", password: str = "", headless: bool = False):
        # Cleaning username:
        if len(username) < 14 or "@carleton.edu" != username[-13:]:
            username += "@carleton.edu"
        self.username = username
        self.password = password
        self.driver = self.get_driver(headless=headless)
        
    
    def get_driver(self, service: str = "chrome", headless: bool = False) -> webdriver.Chrome | webdriver.Firefox:        
        if service.lower() == "firefox":
            options = webdriver.FirefoxOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--log-level=3")
            self.driver = webdriver.Firefox(options=options)
        elif service.lower() == "chrome":
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")
                options.add_argument("--log-level=3")
            self.driver = webdriver.Chrome(options=options)
        else:
            raise ValueError("Service must be either 'firefox' or 'chrome'.")
        return self.driver


    # testing for now
    def log_in(self, username, password) -> webdriver.Chrome | webdriver.Firefox:
        # login url for KB:
        url = r"https://stolafcarleton.teamdynamix.com/SBTDClient/2092/Carleton/Login.aspx?ReturnUrl=%2fSBTDClient%2f2092%2fCarleton%2fHome%2f"
        self.driver.get(url) 
        self.driver.maximize_window()
        
        # Log in:      
        self.driver.find_element(By.ID, "txtUserName").send_keys(username)
        self.driver.find_element(By.ID, "txtPassword").send_keys(password)
        self.driver.find_element(By.ID, "btnSignIn").click()
        
        return self.driver

    # True if deleted, False if not.
    def delete_article(self, article_id: int, base_url: str = "https://stolafcarleton.teamdynamix.com/SBTDClient/2092/Carleton/KB/EditDetails") -> bool:
        
        self.driver.get(base_url + f"?ID={article_id}")
        
        # Make sure we are allowed to delete:
        try:    
            delete = self.driver.find_element(By.ID, "ctl00_ctl00_ctl00_cpContent_cpContent_btnDeleteArticle")
            # Click delete:
            delete.click()
            self.driver.switch_to.alert.accept()
            return True
        except:
            print(f"Article {article_id} not deletable.")
            return False
                

    def example(self):
        self.log_in(self.username, self.password)
        successes = self.delete_from_csv("Articles-03-27-2024.csv")
        self.dict_to_file(successes, "Deletion-Results.csv")
        # self.delete_article(150038)
        
    def dict_to_file(self, dictionary, path) -> None:
        with open(path, "w") as f:
            f.write("Article ID, Deleted?\n")
            f.write("\n".join([f"{key}, {value}" for key, value in dictionary.items()]))
        
    def delete_from_csv(self, csv_path):  
        df = pandas.read_csv(csv_path)
        successes = {}
        for article_id in tqdm(df["ID"][:10]):
            successes[article_id] = self.delete_article(article_id)
        
        return successes


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = r''.join(sys.argv[1])
    else:
        url = r"https://stolafcarleton.teamdynamix.com/SBTDClient/2092/Carleton/KB/"

    username = input("Carleton username: ")
    password = getpass.getpass("Carleton password: ")
    
    scraper = KBScraper(username=username, password=password)
    scraper.example()