import logging
import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kb_scraper import KBScraper

# The following ensures the image loads properly in the packaged app:
import sys
import kivy.resources

if getattr(sys, 'frozen', False):
    # this is a Pyinstaller bundle
    kivy.resources.resource_add_path(sys._MEIPASS)

# Proper window sizing:
from kivy.config import Config
Config.set("graphics", "resizable", True)
Config.set("graphics", "width", 360)
Config.set("graphics", "height", 512)
Config.write()

kivy.require("2.1.0")

class ScraperGUI(Widget): 
    def execute(self):
        # Make logging less annoying
        logging.getLogger("selenium").setLevel(logging.WARN)
        logging.getLogger("urllib3").setLevel(logging.WARN)
        self.ids.errors.text = ' ' # clear errors

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
        if not scraper.log_in(scraper.username, scraper.password):
            self.ids.errors.text = "Incorrect username/password."
            return False
        
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
    
    def on_key_up(self, keyboard, keycode, text):
        if keycode != 9:
            return
        
        username = self.ids.username_input
        password = self.ids.password_input
        csv_path = self.ids.csv_input
        
        if username.focus:
            self.swap_focus(username, password)
        elif password.focus:
            self.swap_focus(password, csv_path)
        elif csv_path.focus:
            self.swap_focus(csv_path, username)
    
    def swap_focus(self, old, new) -> None:
        old.do_backspace()
        old.focus = False
        new.focus = True
        
        
        
    
class ScraperApp(App):
    def build(self):

        # Window.size = (360, 512)
        gui = ScraperGUI() 
        # Bind the events to the corresponding methods
        Window.bind(on_dropfile=gui.on_drop_file)
        Window.bind(on_key_up=gui.on_key_up)
        return gui
    
if __name__ == "__main__":
    ScraperApp().run()