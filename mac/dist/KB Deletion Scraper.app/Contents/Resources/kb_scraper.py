import sys
import time
import pandas
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass # for password input

class KBScraper:
    def __init__(self, username: str = "", password: str = "", service: str = "chrome", headless: bool = False):
        # Cleaning username:
        if len(username) < 14 or "@carleton.edu" != username[-13:]:
            username += "@carleton.edu"
        self.username = username
        self.password = password
        self.driver = self.get_driver(service=service, headless=headless)
        
    # Returns a webdriver object for the given service.
    # * PARAMS:
    # * * service: str - the service to use, either "chrome" or "firefox"
    # * * headless: bool - whether or not to run the browser in headless mode
    # * RETURNS:
    # * * webdriver.Chrome | webdriver.Firefox -> the driver object
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


    # Logs into the KB with the given username and password.
    # * PARAMS:
    # * * username: str - the username to log in with
    # * * password: str - the password to log in with
    # * RETURNS: 
    # * * webdriver.Chrome | webdriver.Firefox - the driver that is now logged in
    def log_in(self, username, password) -> webdriver.Chrome | webdriver.Firefox:
        # login url for KB:
        url = r"https://stolafcarleton.teamdynamix.com/TDClient/2092/Carleton/Login.aspx?ReturnUrl=%2fSBTDClient%2f2092%2fCarleton%2fHome%2f"
        if not self.driver:
            self.driver = self.get_driver()
            
        self.driver.get(url) 
        self.driver.maximize_window()
        
        # Log in:      
        self.driver.find_element(By.ID, "txtUserName").send_keys(username)
        self.driver.find_element(By.ID, "txtPassword").send_keys(password)
        self.driver.find_element(By.ID, "btnSignIn").click()
                
        # Really ugly workaround to see if we're logged in:
        try:
            self.driver.implicitly_wait(3)
            self.driver.find_element(By.CLASS_NAME, "alert-danger")
            print("Login failed. Please check your username and password.")
            self.driver.quit()
            return None
        except:
            self.driver.implicitly_wait(0)
            print("Login successful.")
            return self.driver

    # Deletes an article with the given ID.
    # * PARAMS:
    # * * article_id: int - the ID of the article to delete
    # * * base_url: str - the base url for the KB
    # * RETURNS:
    # * * bool - whether or not the article was deleted
    def delete_article(self, article_id: int, base_url: str = "https://stolafcarleton.teamdynamix.com/TDClient/2092/Carleton/KB/EditDetails") -> bool:
        self.driver.get(base_url + f"?ID={article_id}")
        
        # Make sure we are allowed to delete:
        try:    
            delete = self.driver.find_element(By.ID, "ctl00_ctl00_ctl00_cpContent_cpContent_btnDeleteArticle")
            # Click delete:
            delete.click()
            self.driver.switch_to.alert.accept()
            return True
        except:
            return False
     
    # Writes a dictionary to a csv file.
    def dict_to_file(self, dictionary: dict, path: str) -> None:
        print("Writing results to file...")
        with open(path, "w") as f:
            f.write("Article ID, Deleted?\n")
            f.write("\n".join([f"{key}, {value}" for key, value in dictionary.items()]))
       
    # Deletes articles from a csv file.
    # * PARAMS:
    # * * csv_path: str - the path to the csv file
    # * RETURNS:
    # * * dict - a dictionary of article IDs and whether or not they were deleted
    def delete_from_csv(self, csv_path: str, gui = False) -> dict: 
        csv_path = csv_path.replace("\\", "/") # clean the input
        df = pandas.read_csv(csv_path)
        # Delete articles:
        successes = {key: True for key in df["ID"]}
        i = 0
        for article_id in tqdm(df["ID"]):
            successes[article_id] = self.delete_article(article_id)
            if gui:
                i += 1
                deleted = "deleted." if successes[article_id] else "FAILED."
                print(f"Article {article_id} {deleted} ({i}/{len(successes.keys())})")
        return successes


if __name__ == "__main__":
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        csv_path = input("Path to csv file: ")
    # Get username and password:
    username = input("Carleton username: ")
    password = getpass.getpass("Carleton password: ")
    # Delete articles from dedicated csv file:
    scraper = KBScraper(username=username, password=password)
    scraper.log_in(scraper.username, scraper.password)
    successes = scraper.delete_from_csv(csv_path=csv_path)
    t = time.localtime()
    scraper.dict_to_file(successes,f"KB Deletion - Results {t.tm_year}-{t.tm_mon}-{t.tm_mday}__{t.tm_hour}{t.tm_min}{t.tm_sec}.csv")
    scraper.driver.quit()