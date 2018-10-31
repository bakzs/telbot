import sys
from PIL import ImageGrab
import requests
import time                                                 #for setting a timer for the script
import telepot
import pyautogui                                            #for browser interaction
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from selenium import webdriver                              #for opening and interacting with a web browser
from selenium.webdriver.common.keys import Keys             #for entering keys within the opened web browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

'''Required initialisation to use Telegram's web API and telepot module'''
token = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'

BOT_name = 'UberRun'

bot = telepot.Bot(token)

driver = webdriver.Firefox(executable_path=r"/Users/bakzs/Desktop/MyApps/Python Telegram Bot/geckodriver")



# FUNCTIONS

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

    return adjustment_float


'''To open www.routeloops.com and enter the user's start location and distance to run'''

def enter_route_details(driver, address_str, kilometers_float):
    # To load www.routeloops.com on a browser window
    driver.get("http://www.routeloops.com/")

    # To locate the address box element (named "address") in the web source code and enter user-defined address
    addressbox = driver.find_element_by_id("address")
    addressbox.clear()
    addressbox.send_keys(address_str)

    # To set the above address as the start location
    # By clicking on the 'Set Start/End Location' button on the page
    setstartlocation = driver.find_element_by_xpath("//input[@value='Set Start/End Location']")
    setstartlocation.click()

    # To access the settings tab on www.routeloops.com
    # By clicking on the settings button
    settingsbutton = driver.find_element_by_xpath(".//*[@id='Buttons']/a[7]")
    settingsbutton.click()

    # To change travel mode to 'Walk/Run'
    # By selecting the appropriate option (the third option) on the page
    travelmode = driver.find_element_by_xpath("//*[@id='travelMode']/option[3]")
    travelmode.click()

    # To change all distances to 'kilometers'
    unitsystem = driver.find_element_by_xpath("//*[@id='unitSystem']/option[2]")
    unitsystem.click()

    # To locate the route length element and enter the route distance we want
    distance = driver.find_element_by_id("length")
    distance.clear()
    distance.send_keys(str(kilometers_float))


def test_error_presence(driver):
    try:
        WebDriverWait(driver, 2).until(expected_conditions.alert_is_present())
        return True
    except:
        return False


def handle_error_alerts(driver):
    while test_error_presence(driver):
        alert = driver.switch_to_alert()
        alert.accept()


# To obtain the numerical distance of the current displayed route as a float.
# 1. Locate the distance shown on the webpage - this exists as an element with id 'total_1'.
# 2. This element contains the numerical value of the distance and the unit in the following format: x.xx km).
# 3. Convert this element into text and save it into a list, which will consist of the following strings: ['x.xx', 'km'].
# 4. Return the numerical distance as a float

def get_distance(driver):
    routelength_driverelement = driver.find_elements_by_id('total_1')
    for element in routelength_driverelement:
        templist = (element.text).split()  # To create a list: list = ['x', 'kilometers'], where x = route distance
    distancedisplayed = float(templist[0])
    return distancedisplayed


# To determine whether the variation of the generated route is suitable
def is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
    if (kilometers_float - adjustment_float) < distancedisplayed < (kilometers_float + adjustment_float):
        return True
    else:
        return False

        # To determine if the test route generated is suitable
        # A route is suitable if:
        # (i)  Route distance is loaded on the webpage i.e. route generation is successful
        # (ii) Route distance is > 0
        # (iii)Route distance is suitable (within acceptable variation)


def test_route_generation(driver, kilometers_float, adjustment_float):
    handle_error_alerts(driver)
    distancedisplayed = get_distance(driver)
    if distancedisplayed > 0:
        if is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
            return True
        else:
            return False
    else:
        return False


'''this has been commented by Cheryl'''


def get_directions(driver):
    # To open the direction tab on the map
    directionsbutton = driver.find_element_by_xpath(".//*[@id='Buttons']/a[5]")
    directionsbutton.click()

    # To extract the directions from the directions table and save it to a list
    directionstable = driver.find_element_by_id("mydirectionsPanel")
    allrows = directionstable.find_elements_by_tag_name("tr")
    directionstorage = []  # directionstorage is a list that will contain all the information displayed in the directions panel on the website
    for row in allrows:
        cells = row.find_elements_by_tag_name("td")
        for content in cells:  # Each element is one of the following: S/N of directions, direction statement, travelled distance, or total travelled distance
            content = content.text
            directionstorage.append(content)
    return directionstorage


def set_directionstoprint(directionstorage):
    counter = 0
    directionstoprint = ''  # directionstoprint is a string that will contain all the directions that will be sent to the user
    # [6:] because directions start from the 6th element in the list (counting from 0)
    for direction in directionstorage[6:-1]:
        counter += 1
        directionstoprint += direction
        directionstoprint += ' '
        if counter == 4:
            directionstoprint += '\n'
            counter = 0
    directionstoprint += 'is the total distance. '
    return directionstoprint


# Loop - to keep trying to generate new routes until a suitable route is obtained
def route_generation(driver, kilometers_float, adjustment_float, timeout):
    while time.time() < timeout:  # to run loop for 120s
        handle_error_alerts(driver)
        try:
            distance = driver.find_element_by_id("length")
            distance.clear()
            distance.send_keys(str(kilometers_float))
        except:
            continue
        try:
            driver.find_element_by_id(
                "GoButton").click()  # To click the 'Create loop' button on the page. This will trigger route generation by the website.
        except:
            continue
        handle_error_alerts(driver)
        if test_route_generation(driver, kilometers_float, adjustment_float):
            return True
        else:
            continue


def bot_get_route(address_str, kilometers_float, chat_id):
    adjustment_float = define_adjustment(kilometers_float)
    timeout = time.time() + 120  # to run loop for 120s. time.time() returns the number of seconds since 1970

    while time.time() < timeout:  # to run loop for 120s
        driver = webdriver.Firefox(executable_path=r"/Users/bakzs/Desktop/MyApps/Python Telegram Bot/geckodriver")
            
        #server chromedriver file path required
        try:
            enter_route_details(address_str, kilometers_float)
        except:
            driver.quit()
            continue
        handle_error_alerts()
        if route_generation(kilometers_float, adjustment_float, timeout):
            handle_error_alerts()
            directionslist = get_directions()
            directionstoprint = set_directionstoprint(directionslist)

            bot.sendMessage(chat_id, directionstoprint)

            showmapbutton = driver.find_element_by_xpath(".//*[@id='Buttons']/a[4]")
            showmapbutton.click()
            screenshotregion = driver.find_element_by_id("Configure")
            driver.execute_script("return arguments[0].scrollIntoView();", screenshotregion)

            return True
        else:
            continue
    else:
        bot.sendMessage(chat_id, 'Sorry, no route generated')
        return False
    driver.quit()



''' Function uses telegram's API to send an image.  '''
def send_image(chat_id):
    url = "https://api.telegram.org/bot{}/sendPhoto".format(token)  # telegram's url format for sending images through its API

    files = {'photo': open('/Users/bakzs/Desktop/MyApps/Python Telegram Bot/Screenshot_test.py/screenshot.png', 'rb')}

    data = {'chat_id': chat_id}

    r = requests.post(url, files=files, data=data)  #sends data

    print(r.status_code, r.reason, r.content)



''' 1. uses the ImageGrab module to screenshot an image of current screen'''
def screenshot_image(): #url will be from suwen and cheryl's part
    #url1 = 'https://' + input('What is the website that you would like to screenshot? format: wwww.().com')

    #driver_path = '/Users/bakzs/Desktop/MyApps/Python Telegram Bot/geckodriver'    #prof needs to have a chromedriver and path of it keyed in here for it to work.

    #driver = webdriver.Firefox(executable_path=r"/Users/bakzs/Desktop/MyApps/Python Telegram Bot/geckodriver")

    #driver.get(url1)  # opens url on a browser

    im = ImageGrab.grab()  # screen grabs image after getting map's route loads

    im.save('screenshot.png')  # save image file

    im.show()  # shows image on a window in the server


def communicator(msg):              #to interact with the user and obtain userinputs
    global calories, command, weight          #to ensure that calories and command can be called outside of the function; required in main
    content_type, chat_type, chat_id = telepot.glance(msg)      #obtain relevant information from the server
    print (content_type, chat_type, chat_id)                                   #information for the server
    if content_type == 'text':
        try:                                #try-except to filter between text and numerical values
            int_msg=int(msg['text'])        
            if calories > 0 and weight == 0:            #ensure that calories is stored before weight since it is to be obtained first; also calories should not be negative
                weight = int_msg
                location = 0
                bot.sendMessage(chat_id, 'What is postal code of your starting location?')
            elif calories > 0 and weight > 0:
                location = int_msg
            else:
                calories = int_msg
                weight = 0
                location = 0
                bot.sendMessage(chat_id, 'What is your weight (in kg)?')
        except ValueError:
            command = msg['text'].strip().lower()
            calories = 0
            weight = 0
            location = 0
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
        location = 0
    return command, calories, weight, chat_id, location           #so that values can be called again in the main function

def distancecalc(action, calories, weight):
    if action == 'yeah lets run!':
        distance = calories/weight
    elif action == 'imma skywalker':
        distance = calories/weight * 2
    return distance
    
def main(msg):      #to allow all the functions to work together as a whole program
    command, calories, weight, chat_id, location = communicator(msg)      #returns the values obtained from the communicator func into the variables
    #for testing: print('hello', command, calories, weight)
    if location > 0:                  #weight should not be negative
        #for testing: print('dont come here')
        location = str(location)
        distance = distancecalc(command, calories, weight)
        print(distance)
        msg1 = 'You will need to run {:>5.2f} km!'.format(distance)  #there's a problem with putting a formatted string directly into the bot.sendMessage
        bot.sendMessage(chat_id,msg1)

        bot_get_route(location, distance, chat_id)

        time.sleep(2)
        
        screenshot_image()

        send_image(chat_id)

        bot.sendMessage(chat_id, 'This is your suggested route. Have fun!')

        #bot.sendMessage(chat_id,"You will need to run")

    #for testing: print ('yo', command, calories, weight)

        
bot.message_loop(main)

print ('Listening ...')
# Keep the program running.
while 1:            #while 1 same as while True
    time.sleep(10)  #program sleeps for 10 secs
