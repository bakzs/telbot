UberRun Telegram Bot
----------------------------------------------------------------------------
The purpose of the UberRun telegram bot is to provide users the distance to run/walk based on user-input calories and generate a route for them, with directions and screenshots of map sent to users as a message through telegram.
UberRun provides a form of exercise regime measurement in hopes that it would motivate users to exercise.
--------------------------------------------------------------------------
Getting started
--------------------------------------------------------------------------
Instructions to get UberRun running on local machine for development, usage and testing.

UberRun Bot token: ‘353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg’
-------------
Prerequisites
-------------
- Python v3 is required to run UberRun code
- Firefox browser, gecko driver (win64 version) and driver pathway
- Windows OS
- The following Python modules:
o Selenium
o Telepot
o Pillow
o Requests
- Telegram (latest version)

----------
Installing
----------

1) Make sure Python v3 has been downloaded. Import modules using Command Prompt. pip install <module name>

2) Make sure Firefox browser and gecko driver (https://github.com/mozilla/geckodriver/releases/tag/v0.15.0) has been downloaded or updated to latest version if already installed. Input path of gecko driver under “Initialisations required” found in UberRun Python code as follows: 
driver = webdriver.Firefox(executable_path=’<input path>’)

3) Input path of where screenshot image is saved into initialisation found in UberRun Python code as follows: 
files = {‘photo’:open(r’<input path\screenshot.png>’,’rb’)} 
screenshot.png is typically has the same path as UberRun python script

