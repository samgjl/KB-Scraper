# Installation
## Executables
### Windows:
- Download ```KB Scraper.exe``` from [```KB-Scraper/windows/dist/KB Deletion Scraper.exe```](https://github.com/samgjl/KB-Scraper/blob/main/windows/dist/KB%20Deletion%20Scraper.exe) (CTRL+Shift+D).
### Mac:
1. Clone this repository (```git clone https://github.com/samgjl/KB-Scraper.git```).
2. Locate the executable file at ```mac/dist/KB Deletion Scraper.exe```. <br> You can either move this file to your desired location, or create a shortcut.

## Full code:
- Clone this repository (```git clone https://github.com/samgjl/KB-Scraper.git```)
- You can launch from the python files n ```/src/```.

# Usage
### Launching Without Executable
*If you aren't using the executable, make sure to install all the requirements!* <br> (Install Python, then run ```python -m pip install -r requirements.txt```)
* Launch the base program by running ```python kb_scraper.py```.
* Launch the GUI by running ```python scraper_gui.py```.
### Fields
- *Username:* your username for Carleton College SSO
- *Password:* your password for Carleton College SSO
- *CSV Path:* the path to the CSV file (note: if the file is not in the same folder, you must provide the __absolute__ filepath)
- *Headless:* If checked, this will allow the program to open the browser without visuals. This is best for multitasking

# Building from source
This software requires ```PyInstaller``` (```pip install pyinstaller```), <br> along with all packages in ```requirements.txt``` *(```python -m pip install -r requirements.txt```)*

### Windows
1. Open a terminal at this directory
2. Enter the ```windows``` directory (```cd ./windows/```)
3. Run PyInstaller's initialization script: ```python -m PyInstaller --onefile --name "KB Deletion Scraper" ../src/scraper_gui.py``` <br> *(This will take several minutes to complete)*
4. This will create the ```build``` and ```dist``` folders, along with the ```KB Deletion Scraper.spec``` file. Replace the text in the ```KB Deletion Scraper.spec``` file in this folder with the text from ```windows.spec``` in the base directory. The new file will have all the correct compilation settings.
5. Recompile the app with ```python -m PyInstaller "KB Deletion Scraper.spec"```.

For debugging, see [Kivy's Documentation](https://kivy.org/doc/stable/guide/packaging-windows.html).

### MacOS
1. Open a terminal at this directory
2. Enter the ```mac``` directory (```cd ./mac/```)
3. Run PyInstaller's initialization script: 

```bash
pyinstaller -y --clean --onefile --windowed --name "KB Deletion Scraper" \
  --exclude-module _tkinter \
  --exclude-module Tkinter \
  --exclude-module enchant \
  --exclude-module twisted \
  ../src/scraper_gui.py
```

1. This will create the ```build``` and ```dist``` folders, along with the ```KB Deletion Scraper.spec``` file. Replace the text in the ```KB Deletion Scraper.spec``` file in this folder with the text from ```mac.spec``` in the base directory. The new file will have all the correct compilation settings.
2. Recompile the app with ```pyinstaller -y --clean 'KB Deletion Scraper.spec'```.

For debugging, see [Kivy's Documentation](https://kivy.org/doc/stable/guide/packaging-osx.html).