#MODULES NEEDED
import time                         #for setting a timer for the script
import pyautogui                    #for browser interaction

from selenium import webdriver                              #for opening and interacting with a web browser
from selenium.webdriver.common.keys import Keys             #for entering keys within the opened web browser
pyautogui.FAILSAFE = False

""" Web application does not always return running route distance according to user defined distance.
Web-calculated distance is compared to user defined distance, if it's within the range specified in function, web-calculated running distance will be used """
#purpose of adjustment - to determine the acceptable variation for the route distance 
def define_adjustment(kilometers_float):
    if 0 < kilometers_float < 2:
        adjustment_float = 0.5 * kilometers_float
    elif 2 <= kilometers_float < 3:
        adjustment_float = 0.25 * kilometers_float
    elif 3 <= kilometers_float < 4:
        adjustment_float = 0.2 * kilometers_float
    else:
        adjustment_float = 0.15 * kilometers_float

    print ("adjustment_float returned")
    return adjustment_float

def enter_route_details(browser, address_str, kilometers_float, speed_float):
    #'To load www.routeloops.com on a browser window'
    browser.get("http://www.routeloops.com/mobile/")

#**********************************
    initialisationbutton = browser.find_element_by_id("Wrapper")
    initialisationbutton.click()

#**********************************
    #'To locate the address box element (named "address") in the web source code and enter user-defined address'
    addressbox = browser.find_element_by_id("address")
    addressbox.clear()
    addressbox.send_keys(address_str)

    #To change all distances to 'kilometers'
    unitsystem = browser.find_element_by_xpath("//*[@id='unitSystem']/option[2]")
    unitsystem.click()
    
    #To enter the distance to run
    distance = browser.find_element_by_id("length")
    distance.clear()
    distance.send_keys(str(kilometers_float))

    #To enter the average speed
    averagespeed = browser.find_element_by_id("aveSpeed")
    averagespeed.clear()
    averagespeed.send_keys(str(speed_float))
    
    #'To change travel mode to 'Walk/Run'
    travelmode = browser.find_element_by_xpath("//*[@id='travelMode']/option[3]")
    travelmode.click()
    print ("data entered")
    
'''To handle error alerts that may appear. The script will click on the error alert to select it and press the 'enter' key to acknowledge and close the alert'''

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException

def test_error_presence(browser):
    print ("testing error presence")
    try:
        WebDriverWait(browser, 2).until(expected_conditions.alert_is_present())
        return True
    except TimeoutException:
        print ("no alert")
        return False

def handle_error_alerts(browser):
    while test_error_presence(browser):
        alert = browser.switch_to_alert()
        alert.accept()
        print ("alert accepted")
    
def route_generation (browser, kilometers_float, adjustment_float, timeout):
    while time.time() < timeout:            #to run loop for 120s
        handle_error_alerts(browser)
        try:
            print("route-gen try1 initiated")
            inputpanel = browser.find_element_by_id("showControls")
            inputpanel.click()
            
            distance = browser.find_element_by_id("length")
            distance.clear()
            distance.send_keys(str(kilometers_float))
            print("route-gen try1 end")
        except:
            continue
        try:
            print("to click gobutton")
            controlelement = browser.find_element_by_xpath("//*[@id='controls']")
            controlgobutton = controlelement.find_element_by_id("GoButton")
            controlgobutton.click()
            print("route-gen go button clicked")
        except:
            continue
        handle_error_alerts(browser)
        if test_route_generation(browser, kilometers_float, adjustment_float):
            return True
        else:
            continue

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

#To determine whether the variation of the generated route is suitable
def is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
    if (kilometers_float - adjustment_float) < distancedisplayed < (kilometers_float + adjustment_float):
        print ("variation ok")
        return True
    else:
        print ("variation not ok")
        return False

def get_directions(browser):
    #To open the direction tab on the map
    directionsbutton = browser.find_element_by_id("showDirections")
    directionsbutton.click()

    #To extract the directions from the directions table and save it to a list
    directionstable = browser.find_element_by_id("mydirectionsPanel")
    allrows = directionstable.find_elements_by_tag_name("tr")
    directionstorage = []                #directionstorage is a list that will contain all the information displayed in the directions panel on the website
    for row in allrows:
        cells = row.find_elements_by_tag_name("td")
        for content in cells:            #Each element is one of the following: S/N of directions, direction statement, travelled distance, or total travelled distance
            content = content.text
            directionstorage.append(content)
    print ("this is followed by directionstorage")
    return directionstorage

def set_directions(directionstorage):
    print (directionstorage[0]) #This will print the the following: 'Total distance is x km.' (x = distance) 
    counter = 0
    directionstoprint = ''      #directionstoprint is a string that will contain all the directions that will be sent to the user
    #[6:] because directions start from the 6th element in the list (counting from 0)
    for direction in directionstorage[6:]:
        counter += 1
        directionstoprint += direction
        directionstoprint += ' '
        if counter == 4:
            directionstoprint += '\n'
            counter = 0
    print ("this is followed by directionstoprint")
    return directionstoprint

address_str = "bukit panjang plaza singapore"
kilometers_float = 4.0
speed_float = 5.0

def finalfunction(address_str, kilometers_float, speed_float):
    adjustment_float = define_adjustment(kilometers_float)

    timeout = time.time() + 120   #to run loop for 120s. time.time() returns the number of seconds since 1970

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



