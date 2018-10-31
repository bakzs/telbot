import sys
from selenium import webdriver
from PIL import ImageGrab
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import requests
import time
import telepot
import pyautogui


token = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'
BOT_name = 'UberRun'

bot = telepot.Bot(token)

''' Function uses telegram's web API to send an image.  '''
def send_image(chat_id):
    url = "https://api.telegram.org/bot{}/sendPhoto".format(token)  # telegram's url format for sending images through its API

    files = {'photo': open('/Users/bakzs/Desktop/MyApps/Python Telegram Bot/Screenshot_test.py/screenshot.png', 'rb')}

    data = {'chat_id': chat_id}

    r = requests.post(url, files=files, data=data)  #sends data

    print(r.status_code, r.reason, r.content)



''' 1. uses the ImageGrab module to screenshot an image of current screen'''
def screenshot_image(): #url will be from suwen and cheryl's part
    url1 = 'https://' + input('What is the website that you would like to screenshot? format: wwww.().com')

    driver_path = '/Users/bakzs/Desktop/MyApps/Python Telegram Bot/chromedriver'    #prof needs to have a chromedriver and path of it keyed in here for it to work.

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

        #bot.sendMessage(chat_id,"You will need to run")

    #print ('yo', command, calories, weight)

        
bot.message_loop(main)

print ('Listening ...')
# Keep the program running.
while 1:            #while 1 same as while True
    time.sleep(10)  #program sleeps for 10 secs
