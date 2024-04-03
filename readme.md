## Necessary Actions:
- Get Chrome driver?

## GUI User Guide
### Launching
Launch the GUI by running ```python scraper_gui.py```
### Fields
- *Username:* your username for Carleton College SSO
- *Password:* your password for Carleton College SSO
- *CSV Path:* the path to the CSV file (note: if the file is not in the same folder, you must provide the __absolute__ filepath)
- *Headless:* If checked, this will allow the program to open the browser without visuals. This is best for multitasking


## Recompiling the application

### Windows
1. Open a terminal at this directory
2. enter the ```windows``` directory (```cd ./windows/```)
3. Run Pyinstaller's initialization script: ```python -m PyInstaller --onefile --name "KB Scraper" ../src/scraper_gui.py``` <br> *(This will take several minutes to complete)*
4. This will create the ```build``` and ```dist``` folders, along with the ```KB Scraper.spec``` file. Replace the ```KB Scraper.spec``` file in this folder with the ```KB Scraper.spec``` file in the base directory. The new file will have all the correct compilation settings.
5. Recompile the app with ```python -m PyInstaller "KB Scraper.spec"```.

For debugging, see [Kivy's Documentation](https://kivy.org/doc/stable/guide/packaging-windows.html).