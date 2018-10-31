from selenium import webdriver
import telepot
import requests

'''save a screenshot from some website'''
token = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'
chatid = 50049212


def sendImage():
    url = "https://api.telegram.org/bot{}/sendPhoto".format(token);                                                         #url is using telegram's api to send a photo

    files = {'photo': open('/Users/bakzs/Desktop/MyApps/Python Telegram Bot/Screenshot_test.py/my_screenshot2.png', 'rb')}  #

    data = {'chat_id' : chatid}

    r = requests.post(url, files=files, data=data)

    print(r.status_code, r.reason, r.content)

def ss():

    bot = telepot.Bot(token)

    url = input("Please input a website")

    url1 = 'https://'+ url

    DRIVER = '/Users/bakzs/Downloads/chromedriver'

    driver = webdriver.Chrome(DRIVER)

    driver.get(url1)

    screenshot = driver.save_screenshot('my_screenshot2.png')



    bot.sendMessage(chatid,'This is the suggested route for you,')

    sendImage()

    bot.sendMessage(chatid,'Enjoy!')

    driver.quit()

ss()