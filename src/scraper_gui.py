import logging
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kb_scraper import KBScraper

kivy.require("2.1.0")

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
        if username == "":
            self.ids.errors.text = "Please enter a username."
            return False
        elif password == "":
            self.ids.errors.text = "Please enter a password."
            return False
        elif csv_path == "": 
            self.ids.errors.text = "Please enter a csv path."
            return False
        elif csv_path[-3:] != "csv":
            self.ids.errors.text = "Please use a .CSV file."
            return False
        
        # Web scraper:
        scraper = KBScraper(username=username, password=password, service="chrome", headless=headless)
        scraper.log_in(scraper.username, scraper.password)
        successes = scraper.delete_from_csv(csv_path=csv_path, gui=True)
        # Write results to file:
        scraper.dict_to_file(successes, "results.csv")
        scraper.driver.quit()
    
    def on_drop_file(self, window, file_path, *args):
        if file_path[-3:] != b"csv":
            self.ids.errors.text = "Please drop a csv file."
            return
        path = file_path.decode("utf-8").replace("\\", "/")
        self.ids.csv_input.text = path
        # Do something with the dropped file here
        
        
        
    
class ScraperApp(App):
    def build(self):
        Window.size = (360, 512)
        gui = ScraperGUI() 
        Window.bind(on_dropfile=gui.on_drop_file)
        # Bind the events to the corresponding methods
        return gui
    
if __name__ == "__main__":
    ScraperApp().run()