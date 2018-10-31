import telepot
import sys
import time
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from pprint import pprint

TOKEN = "353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg"


bot = telepot.Bot(TOKEN)

def handle(msg): #handles msgs and the Offset values
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg) #{'message_id': 51, 'from': {'id': 50049212, 'first_name': 'Bak', 'last_name': 'Zhee Shuen'}, 'chat': {'id': 50049212, 'first_name': 'Bak', 'last_name': 'Zhee Shuen', 'type': 'private'}, 'date': 1490264635, 'text': 'H'}


    if content_type == 'text':
        bot.sendMessage(chat_id,msg['text'])
    else:
        bot.sendMessage(chat_id,'Sorry only text and numbers!')
    return msg



def initiation(chat_id):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Run'), KeyboardButton(text='Walk')]])

    bot.sendMessage(chat_id, "Run or walk?", reply_markup=keyboard)

def calories(chat_id):
    keyboard = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='1'), KeyboardButton(text='2')]])
    bot.sendMessage(chat_id, "How many calories do you want to burn?")

def body(msg):

    hand
    print(reply)
    chatid = reply['chat']['id']
    initiation(chatid)
    reply = bot.getUpdates()
    if reply['text'] == 'Run':
        calories(chatid)
    else:
        bot.sendMessage(chatid,"Bye!")

    cals = int(handle(msg)['text'])
    distance = 27*cals

    bot.sendMessage(chatid, 'You will need to run {>4.2d} metres'.format(distance))
    bot.sendMessage(chatid, 'Here is a suggested route for your run!')




bot.message_loop(body) #loops the function


while 1:
    time.sleep(10)
