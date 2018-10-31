import sys
from PIL import ImageGrab
import requests
#for setting a timer for the function bot_get_route()
import time                                                 
#for telegram interactions
import telepot
#for browser interactions
import pyautogui                                           
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
#Selenium is a browser automation library - for opening and interacting with a web browser ***
from selenium import webdriver
#for entering keys within the opened web browser
from selenium.webdriver.common.keys import Keys
#to allow the browser to wait for a certain number of seconds
from selenium.webdriver.support.ui import WebDriverWait
#to use expected_conditions.alert_is_present(), which determines whether an alert (error message) is present
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

'''Required initialisation to use Telegram's web API and telepot module'''
token = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'

BOT_name = 'UberRun'

bot = telepot.Bot(token)

# FUNCTIONS

""" Web application does not always return running route distance according to user-defined distance.
This function determines the acceptable variation between the web-calculated distsance and the user-defined distance. """
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

    #To change all distances on the website to 'kilometers'
    #By selecting the appropriate option (the second option) on the page
    unitsystem = driver.find_element_by_xpath("//*[@id='unitSystem']/option[2]")
    unitsystem.click()

    #To locate the 'desired route length' element (named "length") and enter the user-defined route distance
    distance = driver.find_element_by_id("length")
    distance.clear()
    distance.send_keys(str(kilometers_float))

'''To determine whether an error message (alert) is present'''
def test_error_presence(driver):
    try:
        #the browser will wait for two seconds until an alert message appears
        WebDriverWait(driver, 2).until(expected_conditions.alert_is_present())
        return True
    except:
        #this section of code will run if no alert message appears
        return False

'''To accept any alert messages that are present'''
def handle_error_alerts(driver):
    while test_error_presence(driver):
        #this makes the browser focus on the alert message 
        alert = driver.switch_to_alert()
        alert.accept()


'''To obtain the numerical distance of the current displayed route as a float.
    1. Locate the distance shown on the webpage - this exists as an element with id 'total_1'.
    2. This element contains the numerical value of the distance and the unit in the following format: x.xx km).
    3. Convert this element into text, split the element into 'x,xx' and 'km', and save it into a list (list = ['x.xx', 'km'])
    4. Return the numerical distance as a float'''
def get_distance(driver):
    routelength_driverelement = driver.find_elements_by_id('total_1')
    for element in routelength_driverelement:
        templist = (element.text).split()  
    distancedisplayed = float(templist[0])
    return distancedisplayed


'''To determine whether the variation of the generated route is suitable'''
def is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
    if (kilometers_float - adjustment_float) < distancedisplayed < (kilometers_float + adjustment_float):
        return True
    else:
        return False

'''To determine if the test route generated is suitable
    A route is suitable if:
        (i)  Route distance is loaded on the webpage i.e. route generation is successful
        (ii) Route distance is > 0
        (iii)Route distance is suitable (within acceptable variation)'''
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

'''To obtain the list of directions generated by the website'''
def get_directions(driver):
    #To open the direction tab on the map by clicking the appropriate button
    directionsbutton = driver.find_element_by_xpath(".//*[@id='Buttons']/a[5]")
    directionsbutton.click()

    #To extract the directions from the directions table and save it to a list (directionstorage)
    directionstable = driver.find_element_by_id("mydirectionsPanel")

    #To generate a list where each element contains the information stored in each row of the table
    allrows = directionstable.find_elements_by_tag_name("tr")

    # directionstorage is a list that will contain all the information displayed in the directions panel on the website
    directionstorage = []
    for row in allrows:
        #To generate a list where each element contains the information stored in each cell of the table
        cells = row.find_elements_by_tag_name("td")
        
        #Each cell contains one of the following: S/N of directions, direction statement, travelled distance, or total travelled distance
        for content in cells:
            #To convert the contents of each cell into text
            content = content.text
            directionstorage.append(content)
    return directionstorage

'''To obtain a string containing the directions to be sent to the user'''
def set_directionstoprint(directionstorage):
    counter = 0

    #directionstoprint is a string that will contain all the directions that will be sent to the user
    directionstoprint = ''

    #[6:] because directions start from index 6 of the directionstorage list
    for direction in directionstorage[6:-1]:
        counter += 1
        directionstoprint += direction
        directionstoprint += ' '

        #To indicate that each step of the directions is to be printed on a new line
        #Each step of the directions contains: S/N of directions, direction statement, travelled distance, and total travelled distance
        #Therefore, every 5th element has to be printed on a new line 
        if counter == 4:
            directionstoprint += '\n'
            counter = 0
    directionstoprint += 'is the total distance. '
    return directionstoprint

'''To keep trying to generate new routes until a suitable route is obtained
    1. User-defined distance is entered into the 'desired route length' element. This needs to be included in the loop because the website will change the distance
        in the 'desired route length' element automatically when the script accepts the following error message:
        "The current route length (x) is too far from the requested distance (y)."
    2. Click the 'Create loop' button (id = "GoButton") on the page to trigger route generation on the website.
    3. Test whether the generated loop is suitable
    
    *Each of the above steps is encased in a 'try-except' block.
    *Reason: error messages may take some time to appear due to lag. If this happens during each 'try' block, an exception
    *will occur. '''
def route_generation(driver, kilometers_float, adjustment_float, timeout):
    #to run loop for 120 seconds - timeout = time.time() + 120 (this is defined in bot_get_route())
    while time.time() < timeout:  
        handle_error_alerts(driver)
        try:
            distance = driver.find_element_by_id("length")
            distance.clear()
            distance.send_keys(str(kilometers_float))
        except:
            continue
        try:
            #To click the 'Create loop' button on the page. This will trigger route generation by the website.
            driver.find_element_by_id("GoButton").click()  
        except:
            continue
        handle_error_alerts(driver)
        if test_route_generation(driver, kilometers_float, adjustment_float):
            return True
        else:
            continue

'''To generate a suitable route for the user according to the user's start location and the user-defined route distance '''
def bot_get_route(address_str, kilometers_float, chat_id):
    adjustment_float = define_adjustment(kilometers_float)
    
    #To set timeout as 90s from the time this line of code is run. time.time() returns the number of seconds since the epoch (1/1/1970, 0h)
    timeout = time.time() + 120  

    #To run loop for 90s
    while time.time() < timeout:
        #This opens a browser window.
        driver = webdriver.Firefox(executable_path=r"/Users/bakzs/Desktop/MyApps/Python Telegram Bot/geckodriver")

        #This section enters the relevant information into the website (see comments for the enter_route_details() function above).
        #If an error occurs, the script quits the browser and restart the loop.

        try:
            enter_route_details(driver, address_str, kilometers_float)
        except:
            driver.quit()
            continue
        handle_error_alerts(driver)

        #This runs if the route generated is suitable 
        if route_generation(driver, kilometers_float, adjustment_float, timeout):
            handle_error_alerts(driver)
            directionslist = get_directions(driver)
            directionstoprint = set_directionstoprint(directionslist)

            bot.sendMessage(chat_id, directionstoprint)

            #To stop viewing the directions panel and show only the map on the screen
            #By selecting the 'Map Only' option
            showmapbutton = driver.find_element_by_xpath(".//*[@id='Buttons']/a[4]")
            showmapbutton.click()

            #To scroll the page down to focus on the map
            #"Configure" is an element immediately below the map on the webpage
            #driver.execute_script() will scroll the page down until the "Configure" element comes into view 
            screenshotregion = driver.find_element_by_id("Configure")
            driver.execute_script("return arguments[0].scrollIntoView();", screenshotregion)

            time.sleep(2)
            screenshot_image()
            send_image(chat_id)

            driver.quit()

            return True
        else:
            continue
    else:
        driver.quit()
        return False

''' Function uses telegram's API to send an image.  '''
def send_image(chat_id):
    # telegram's url format for sending images through its API
    url = "https://api.telegram.org/bot{}/sendPhoto".format(token)  
    files = {'photo': open(r'/Users/bakzs/Desktop/MyApps/Python Telegram Bot/Screenshot_test.py/screenshot.png', 'rb')}
    data = {'chat_id': chat_id}
    #sends data
    r = requests.post(url, files=files, data=data)
    print(r.status_code, r.reason, r.content)

''' 1. uses the ImageGrab module to screenshot an image of current screen'''
def screenshot_image():
    # screen grabs image after getting getting map's route loads
    im = ImageGrab.grab()  
    # save image file
    #screenshot = driver.save_screenshot('my_screenshot2.png')
    im.save('screenshot.png')  
    # shows image on a window in the server
    im.show()  

''' This function obtains all the necessary input from the user and returns it into variables to be called in subsequent functions '''
def communicator(msg):              
    #to ensure that calories, weight and command values are stored globally across all functions;
    #required to compare whether calories and weight are > 0 or == 0 when the message sent is a numerical value
    global calories, command, weight
    #obtain relevant information from the server
    content_type, chat_type, chat_id = telepot.glance(msg)
    #information for the server
    print (content_type, chat_type, chat_id)                                   
    if content_type == 'text':
        #required try-except to filter between wordings and numerical values which are both of content-type text
        try:                                
            float_msg=float(msg['text'])        
            #to ensure that a non-negative value for calories is stored before weight since it is to be obtained first
            if calories > 0 and weight == 0:            
                weight = float_msg
                location = 0
                bot.sendMessage(chat_id, 'What is postal code of your starting location?')
            #to ensure that calories and weight have a non-negative value assigned before location is stored
            elif calories > 0 and weight > 0:
                location = int(float_msg)
            elif calories < 0 or weight < 0:
                bot.sendMessage(chat_id, 'Please input non-negative values.')
            else:
                calories = float_msg
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
                    [KeyboardButton(text='Yeah lets run!')],[KeyboardButton(text='Imma skywalker')],
                    [KeyboardButton(text='Potatoes don\'t exercise')]], one_time_keyboard = True)
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
    #to ensure values are stored in the variables in the main function    
    return command, calories, weight, chat_id, location           



''' This function is used to calculate the distance required to be run/walked in terms of calories and weight'''
def distancecalc(action, calories, weight):
    if action == 'yeah lets run!':
        distance = calories/weight
    elif action == 'imma skywalker':
        distance = calories/weight * 2
    return distance



'''The main body of the entire program which links all the functions together to carry out the bot's desired role.'''    
def main(msg):
    #obtains values from communicator function into the variables
    command, calories, weight, chat_id, location = communicator(msg)
    #location should not be negative
    if location > 0:                  
        location = str(location)
        distance = distancecalc(command, calories, weight)

        bot.sendMessage(chat_id, 'We\'re generating a route for you - please be patient!')

        if bot_get_route(location, distance, chat_id):
            bot.sendMessage(chat_id, 'This is your suggested route. Have fun!')
        else:
            bot.sendMessage(chat_id, 'Sorry, no suitable route was found   :( Try again?')
    

bot.message_loop(main)

print ('Listening ...')
# Keep the program running.
#while 1 same as while True
while 1:
    #program sleeps for 10 secs
    time.sleep(10)  
