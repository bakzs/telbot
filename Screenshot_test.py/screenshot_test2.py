'''Screenshots your whole screen that you are on, for example if you're on google.com, it will screenshot your whole screen, literally. Including your task bar, basically the screen you
are looking at.'''
#-- include('examples/showgrabfullscreen.py') --#
from selenium import webdriver
from PIL import ImageGrab
import telepot
import requests


token = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'

chatid = 50049212 #chat_id will be provided from telepot.glance()

bot = telepot.Bot(token)





''' Function uses telegram's API to send an image.  '''
def sendImage():

    url = "https://api.telegram.org/bot{}/sendPhoto".format(token);                                                     #telegram's url format for sending images through its API

    files = {'photo': open('/Users/bakzs/Desktop/MyApps/Python Telegram Bot/Screenshot_test.py/screenshot.png', 'rb')}

    data = {'chat_id' : chatid}

    r = requests.post(url, files=files, data=data)  #sends data

    print(r.status_code, r.reason, r.content)




''' 1. uses the ImageGrab module to screenshot an image of current screen
    2. sendImage() to send image after getting screenshot.'''
def screenshot_image():
    #url1 = 'https://' + input('What is the website that you would like to screenshot? format: wwww.().com')

    #driver_path = '/Users/bakzs/Desktop/MyApps/Python Telegram Bot/geckodriver'

    #driver = webdriver.Firefox(driver_path)

    #driver.get(url1)                                                                                                    #opens url on a browser

    im = ImageGrab.grab()                                                                                               #screen grabs image after getting getting map's route loads

    im.save('screenshot.png')                                                                                           #save image file

    im.show()                                                                                                           #shows image on a window in the server


screenshot_image()
sendImage()

