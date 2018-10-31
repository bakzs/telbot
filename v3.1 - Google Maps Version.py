#MODULES NEEDED
import time                             #for setting a timer for the script
import pyautogui                        #for browser interaction

from selenium import webdriver      #for opening and interacting with a web browser
from selenium.webdriver.common.keys import Keys #for entering keys within the opened web browser
pyautogui.FAILSAFE = False
######################################
############################################################
#VARIABLES - FOR USER INPUT
address_str = "nanyang junior college singapore"
kilometers_float = 4.0

###########

########################################################################################
#VARIABLES
#The variable 'browser' is initialised in the main loop
#Reason: initialisation causes a browser window to open

###################################################################################################

#FUNCTIONS
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
        
    return adjustment_float


'''To open www.routeloops.com and enter the user's start location and distance to run'''
def enter_route_details(browser, address_str, kilometers_float):
    'To load www.routeloops.com on a browser window'
    browser.get("http://www.routeloops.com/")

    'To locate the address box element (named "address") in the web source code and enter user-defined address'
    addressbox = browser.find_element_by_id("address")
    print ("addressbox", addressbox)
    addressbox.clear()
    addressbox.send_keys(address_str)

    'To set the above address as the start location'
    setstartlocation = browser.find_element_by_xpath("//input[@value='Set Start/End Location']")
    setstartlocation.click()
    #print ("start location set")

    'To access the settings on www.routeloops.com;'
    settingsbutton = browser.find_element_by_xpath(".//*[@id='Buttons']/a[8]")
    settingsbutton.click()
    #print ("settingsbutton clicked")

    '''To change travel mode to 'Walk/Run'''
    travelmode = browser.find_element_by_xpath("//*[@id='travelMode']/option[3]")
    travelmode.click()
    #print ("Travelmode selected")

    #To change all distances to 'kilometers'
    unitsystem = browser.find_element_by_xpath("//*[@id='unitSystem']/option[2]")
    unitsystem.click()
    #print ("Unit system selected")

    #To enter the distance to run
    distance = browser.find_element_by_id("length")
    distance.clear()
    distance.send_keys(str(kilometers_float))
    #print ("Distance entered")


'''To click the 'Create loop' button on the page. This will trigger route generation by the website. '''
def click_go_button(browser):
    browser.find_element_by_id("GoButton").click()       #To start route generation on www.routeloops.com
    #print ("GoButton clicked")



#To close error alerts
#***How to generalise this?
'''To handle error alerts that may appear. The script will click on the error alert to select it and press the 'enter' key to acknowledge and close the alert'''
def handle_error_alerts(browser):
    pyautogui.click(x=650, y=335)
    pyautogui.press('enter')
    #print ("enter key pressed")



#To obtain the generated route's distance from the webpage
def get_distance(browser):
    '''To obtain the numerical distance of the current displayed route as a float.
        1. Locate the distance shown on the webpage - this exists as an element with id 'total_1'.
        2. This element contains the numerical value of the distance and the unit in the following format: x.xx km).
        3. Convert this element into text and save it into a list, which will consist of the following strings: ['x.xx', 'km'].
        4. Return the numerical distance as a float'''
    routelength_browserelement = browser.find_elements_by_id('total_1')
    for element in routelength_browserelement:
        #To create a list: list = ['x', 'kilometers'], where x = route distance
        templist = (element.text).split()
    distancedisplayed = float(templist[0])
    #print ("distancedisplayed = ", distancedisplayed)
    return distancedisplayed



#To determine whether the distance of the generated route is suitable
def is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
    if (kilometers_float - adjustment_float) < distancedisplayed < (kilometers_float + adjustment_float):
        #print ("variation is acceptable")
        #print ("Route distance = ", distancedisplayed)
        return True
    else:
        #print ("variation is not acceptable")
        return False



''''#To determine if the test route generated is suitable
    #A route is suitable if:
    #(i)  Route distance is loaded on the webpage i.e. route generation is successful
    #(ii) Route distance is > 0
    #(iii)Route distance is suitable (within acceptable variation)'''
def test_route_generation(browser, kilometers_float, adjustment_float):
    handle_error_alerts(browser)
    handle_error_alerts(browser)
    #print ("testdistancepresence is going to start")
    handle_error_alerts(browser)
    handle_error_alerts(browser)
    handle_error_alerts(browser)        
    handle_error_alerts(browser) #DON'T REMOVE ***
    handle_error_alerts(browser) #DON'T REMOVE ***
    #print ("going to get distancedislayed")
    distancedisplayed = get_distance(browser)        
    if distancedisplayed > 0:
        #print ("Route distance is more than 0.")
        if is_variation_acceptable(kilometers_float, adjustment_float, distancedisplayed):
            return True
        else:
            return False
    else:
        #print ("distance displayed <= 0")
        return False

'''this has been commented by Cheryl'''



def get_directions(browser):
    #To open the direction tab on the map
    directionsbutton = browser.find_element_by_xpath(".//*[@id='Buttons']/a[6]")
    directionsbutton.click()
    #print ("directionbutton clicked")

    #To extract the directions from the directions table and save it to a list
    directionstable = browser.find_element_by_id("mydirectionsPanel")
    allrows = directionstable.find_elements_by_tag_name("tr")
    #print ("allrows found")
    directionstorage = []
    for row in allrows:
        #print ("row found")
        cells = row.find_elements_by_tag_name("td")
        print (cells)
        print (type(cells))
        #print ("cells found")
        #Each element is one of the following: S/N of directions, direction statement, travelled distance, or total travelled distance
        for content in cells:
            content = content.text
            #print (content)
            directionstorage.append(content)
    return directionstorage
    #print (type(directionstorage))




def set_directions(directionstorage):
    #print (directionstorage)
    print(directionstorage[0])
    counter = 0
    directionstoprint = ''
    #[6:] because directions start from the 6th element in the list (counting from 0)
    for direction in directionstorage[6:]:
        counter += 1
        directionstoprint += direction
        directionstoprint += ' '
        #print (direction, end=' ')
        if counter == 4:
            directionstoprint += '\n'
            counter = 0
    return directionstoprint
    #print ("Directions: ")
    #print (directionstoprint)



#Loop - to keep trying to generate new routes until a suitable route is obtained
def route_generation(browser, kilometers_float, adjustment_float, timeout):

    while time.time() < timeout:        #to run loop for 120s
        handle_error_alerts(browser)
        try:
            distance = browser.find_element_by_id("length")
            distance.clear()
            distance.send_keys(str(kilometers_float))
            #print ("Distance entered")
        except:
            continue
        try:
            click_go_button(browser)
            #print ("Section try2 of route_generation succeeded")
        except:
            #print ("Section try2 of route_generation failed")
            continue
        handle_error_alerts(browser)
        handle_error_alerts(browser)
        if test_route_generation(browser, kilometers_float, adjustment_float):
            #print ("generated route is suitable")
            return True
        else:
            #print ("generated route is not suitable")
            continue



###################################################################################################
#MAIN BODY
#i = 1
#to run loop for 120s
adjustment_float = define_adjustment(kilometers_float)
#time.time() returns the number of seconds since 1970 ***
timeout = time.time() + 120
while time.time() < timeout: 

    #print ("Loop iteration: ", i)
    #pathname ='C:\Users\User\AppData\Local\Programs\Python\Python36\geckodriver.exe'
    #browser = webdriver.Firefox(executable_path=r'{}'.format(pathname))
    browser = webdriver.Chrome(executable_path=r'/Users/bakzs/Downloads/chromedriver')

    #print ("Loading page")
    try:
        enter_route_details(browser, address_str, kilometers_float)
        #print ("enterroutedetails", i, "executed")
        #i += 1


    except:
        browser.quit()


        #print ("enterroutedetails", i, "failed")
        #i += 1
        continue
    handle_error_alerts(browser)
    if route_generation(browser, kilometers_float, adjustment_float, timeout):
        handle_error_alerts(browser)
        handle_error_alerts(browser)
        #print ("To run get directions")
        directionslist = get_directions(browser)
        directionstoprint = set_directions(directionslist)

       # browser.quit()
       # print ("Browser has quit")
        break
    else:
        continue
else:
    print ("Script failed to get directions.")
   # browser.quit()
   # print ("Browser has quit")

showmapbutton = browser.find_element_by_xpath(".//*[@id='Buttons']/a[5]")
showmapbutton.click()

screenshotregion = browser.find_element_by_id("Configure")
browser.execute_script("return arguments[0].scrollIntoView();", screenshotregion)
print("screenshot code executed")

print(directionstoprint)
#bot.sendMessage(chat_id, directionstoprint)
