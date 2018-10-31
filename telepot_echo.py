import telepot
import time
import sys

TOKEN = '353987109:AAFa3AQZ0fVQ6qTS9J3ivCNC8y50SIlXbGg'

bot = telepot.Bot(TOKEN)

def handle(msg): #handles msgs and the Offset values
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg) #{'message_id': 51, 'from': {'id': 50049212, 'first_name': 'Bak', 'last_name': 'Zhee Shuen'}, 'chat': {'id': 50049212, 'first_name': 'Bak', 'last_name': 'Zhee Shuen', 'type': 'private'}, 'date': 1490264635, 'text': 'H'}


    if content_type == 'text':
        bot.sendMessage(chat_id,msg['text'])
    else:
        bot.sendMessage(chat_id,'Text, numbers and emojis!')

print('Listening...')
bot.message_loop(handle)

while True:
    time.sleep(10)
hi

hi

hi