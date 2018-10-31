import sys
from selenium import webdriver
from PIL import ImageGrab
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton

'''To handle error alerts that may appear. The script will click on the error alert to select it and press the 'enter' key to acknowledge and close the alert'''
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

import requests
import time
import telepot
import pyautogui

pyautogui.FAILSAFE = False
token = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'
BOT_name = 'UberRun'

bot = telepot.Bot(token)


# To determine whether the variation of the generated route is suitable
def is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
    if (kilometers_float - adjustment_float) < distancedisplayed < (kilometers_float + adjustment_float):
        print("variation ok")
        return True
    else:
        print("variation not ok")
        return False


def get_directions(browser):
    # To open the direction tab on the map
    directionsbutton = browser.find_element_by_id("showDirections")
    directionsbutton.click()

    # To extract the directions from the directions table and save it to a list
    directionstable = browser.find_element_by_id("mydirectionsPanel")
    allrows = directionstable.find_elements_by_tag_name("tr")
    directionstorage = []  # directionstorage is a list that will contain all the information displayed in the directions panel on the website
    for row in allrows:
        cells = row.find_elements_by_tag_name("td")
        for content in cells:  # Each element is one of the following: S/N of directions, direction statement, travelled distance, or total travelled distance
            content = content.text
            directionstorage.append(content)
    print("this is followed by directionstorage")
    return directionstorage


def set_directions(directionstorage):
    print(directionstorage[0])  # This will print the the following: 'Total distance is x km.' (x = distance)
    counter = 0
    directionstoprint = ''  # directionstoprint is a string that will contain all the directions that will be sent to the user
    # [6:] because directions start from the 6th element in the list (counting from 0)
    for direction in directionstorage[6:]:
        counter += 1
        directionstoprint += direction
        directionstoprint += ' '
        if counter == 4:
            directionstoprint += '\n'
            counter = 0
    print("this is followed by directionstoprint")
    return directionstoprint


address_str = "bukit panjang plaza singapore"
kilometers_float = 4.0
speed_float = 5.0


def finalfunction(address_str, kilometers_float, speed_float):
    adjustment_float = define_adjustment(kilometers_float)

    timeout = time.time() + 120  # to run loop for 120s. time.time() returns the number of seconds since 1970

    while time.time() < timeout:
        browser = webdriver.Chrome(executable_path=r'/Users/bakzs/Desktop/MyApps/Python Telegram Bot/chromedriver')

        enter_route_details(browser, address_str, kilometers_float, speed_float)
        handle_error_alerts(browser)
        if route_generation(browser, kilometers_float, adjustment_float, timeout):
            handle_error_alerts(browser)
            directionslist = get_directions(browser)
            directionstoprint = set_directions(directionslist)

            showmapbutton = browser.find_element_by_id("showMap")
            showmapbutton.click()

            bot.sendMessage(chat_id, directionstoprint)
            return True
        else:
            continue
    else:
        bot.sendMessage(chat_id, 'Sorry, no route generated')
        return False

#To determine if the test route generated is suitable
#A route is suitable if:
    #(i)  Route distance is loaded on the webpage i.e. route generation is successful
    #(ii) Route distance is > 0
    #(iii)Route distance is suitable (within acceptable variation)

def test_route_generation(browser, kilometers_float, adjustment_float):
    handle_error_alerts(browser)
    distancedisplayed = get_distance(browser)
    if distancedisplayed > 0:
        print ("distancedisplayed >0")
        if is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
            return True
        else:
            return False
    else:
        print ("distancedisplayed <0")
        return False

def get_distance(browser):
    routelength_browserelement = browser.find_elements_by_id('total_1')
    for element in routelength_browserelement:
        templist = (element.text).split()         #To create a list: list = ['x', 'kilometers'], where x = route distance
    distancedisplayed = float(templist[0])
    print("distancedisplayed obtained")
    return distancedisplayed

""" Web application does not always return running route distance according to user defined distance.
Web-calculated distance is compared to user defined distance, if it's within the range specified in function, web-calculated running distance will be used """

# purpose of adjustment - to determine the acceptable variation for the route distance
def define_adjustment(kilometers_float):
    if 0 < kilometers_float < 2:
        adjustment_float = 0.5 * kilometers_float
    elif 2 <= kilometers_float < 3:
        adjustment_float = 0.25 * kilometers_float
    elif 3 <= kilometers_float < 4:
        adjustment_float = 0.2 * kilometers_float
    else:
        adjustment_float = 0.15 * kilometers_float

    print("adjustment_float returned")
    return adjustment_float


def enter_route_details(browser, address_str, kilometers_float, speed_float):
    # 'To load www.routeloops.com on a browser window'
    browser.get("http://www.routeloops.com/mobile/")

    # **********************************
    initialisationbutton = browser.find_element_by_id("Wrapper")
    initialisationbutton.click()

    # **********************************
    # 'To locate the address box element (named "address") in the web source code and enter user-defined address'
    addressbox = browser.find_element_by_id("address")
    addressbox.clear()
    addressbox.send_keys(address_str)

    # To change all distances to 'kilometers'
    unitsystem = browser.find_element_by_xpath("//*[@id='unitSystem']/option[2]")
    unitsystem.click()

    # To enter the distance to run
    distance = browser.find_element_by_id("length")
    distance.clear()
    distance.send_keys(str(kilometers_float))

    # To enter the average speed
    averagespeed = browser.find_element_by_id("aveSpeed")
    averagespeed.clear()
    averagespeed.send_keys(str(speed_float))

    # 'To change travel mode to 'Walk/Run'
    travelmode = browser.find_element_by_xpath("//*[@id='travelMode']/option[3]")
    travelmode.click()
    print("data entered")


''' Function uses telegram's API to send an image.  '''
def send_image(chat_id):
    url = "https://api.telegram.org/bot{}/sendPhoto".format(token)  # telegram's url format for sending images through its API

    files = {'photo': open('/Users/bakzs/Desktop/MyApps/Python Telegram Bot/Screenshot_test.py/screenshot.png', 'rb')}

    data = {'chat_id': chat_id}

    r = requests.post(url, files=files, data=data)  #sends data

    print(r.status_code, r.reason, r.content)



''' 1. uses the ImageGrab module to screenshot an image of current screen
    2. sendImage() to send image after getting screenshot.'''
def screenshot_image(): #url will be from suwen and cheryl's part
    url1 = 'https://' + input('What is the website that you would like to screenshot? format: wwww.().com')

    driver_path = '/Users/bakzs/Desktop/MyApps/Python Telegram Bot/chromedriver'    #professor needs to your own chromedriver path keyed in here for it to work.

    driver = webdriver.Chrome(driver_path)

    driver.get(url1)  # opens url on a browser

    im = ImageGrab.grab()  # screen grabs image after getting getting map's route loads

    im.save('screenshot.png')  # save image file

    im.show()  # shows image on a window in the server


def communicator(msg):
    global calories, command          #what is this line for?
    content_type, chat_type, chat_id = telepot.glance(msg)
    print (content_type, chat_type, chat_id)                                   #information for the server
    if content_type == 'text':
        try:
            int_msg=int(msg['text'])
            if calories != 0:
                weight = int_msg
            else:
                calories = int_msg
                weight = 0
                bot.sendMessage(chat_id, 'What is your weight (in kg)?')
        except ValueError:
            command = msg['text'].strip().lower()
            calories = 0
            weight = 0
            if command == '/start':
                actkeyboard = ReplyKeyboardMarkup(keyboard=[
                    [KeyboardButton(text='Yeah lets run!'),KeyboardButton(text='Imma skywalker'), KeyboardButton(text='Potatoes don\'t exercise')]], one_time_keyboard = True)
                bot.sendMessage(chat_id, "Intending to exercise?", reply_markup=actkeyboard)
            elif command == 'potatoes don\'t exercise':
                bot.sendMessage(chat_id, "Bye then!! Start me when you actually want to run.")
            elif command == 'yeah lets run!' or command == 'imma skywalker':
                bot.sendMessage(chat_id, "That's a great start!\nHow many calories do you want to burn?")
            else:
                bot.sendMessage(chat_id, "Huh? I don't understand. Please restart.")
    else:
        bot.sendMessage(chat_id, "Workout talk only!!")
        command = ''
        calories = 0
        weight = 0
    return command, calories, weight, chat_id

def distancecalc(action, calories, weight):
    if action == 'yeah lets run!':
        distance = calories/weight
    elif action == 'imma skywalker':
        distance = calories/weight * 2
    return distance
    
def main(msg):
    command, calories, weight, chat_id = communicator(msg)
    #print('hello', command, calories, weight)
    if weight != 0:
        #print('dont come here')
        distance = distancecalc(command, calories, weight)
        print(distance)
        msg1 = 'You will need to run {:>5.2f} km!'.format(distance)  #there's a problem with putting a formatted string directly into the bot.sendMessage
        bot.sendMessage(chat_id,msg1)
        #suwen's part

        screenshot_image()
        send_image(chat_id)
        bot.sendMessage(chat_id, 'This is your suggested route. Have fun!')


    #print ('yo', command, calories, weight)

        
bot.message_loop(main)

print ('Listening ...')
# Keep the program running.
while 1:            #while 1 same as while True
    time.sleep(10)  #program sleeps for 10 secs
