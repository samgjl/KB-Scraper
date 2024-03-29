import logging
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kb_scraper import KBScraper

class ScraperGUI(Widget): 
    def execute(self):
        logging.getLogger("selenium").setLevel(logging.WARN)
        logging.getLogger("urllib3").setLevel(logging.WARN)

        # Get inputs:
        username = self.ids.username_input.text
        password = self.ids.password_input.text 
        csv_path = self.ids.csv_input.text
        headless = self.ids.headless.active

        # Check for empty inputs:
        if username == "" or password == "":
            print("Please enter a username and password.")
        if csv_path == "": 
            print("Please enter a csv path.")
        
        # Web scraper:
        scraper = KBScraper(username=username, password=password, service="chrome", headless=headless)
        scraper.log_in(scraper.username, scraper.password)
        successes = scraper.delete_from_csv(csv_path=csv_path, gui=True)
        # Write results to file:
        scraper.dict_to_file(successes, "results.csv")
        scraper.driver.quit()
    
class ScraperApp(App):
    def build(self):
        Window.size = (360, 512)
        gui = ScraperGUI()        
        return gui
    
if __name__ == "__main__":
    ScraperApp().run()