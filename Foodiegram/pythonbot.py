import sys
import time
import telepot
import random
from twx.botapi import TelegramBot, ReplyKeyboardMarkup 
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
from bs4 import BeautifulSoup
import requests
import html

foodcourt_halal=("Plain Naan" , "Garlic Naan" , "Butter Naan" , "Cheese Naan" , "\
Tandoori Roti" , "Dahi" , "Gobi Mutter" , "Chaana Masala" , "Aloo Fry Masala" , "\
Curry Chicken" , "Mutton Masala" , "Bindi Masala" , "Fry Chicken" , "\
Paneer Butter Masala" , "Vegetarian Briyani Dahi Aloo Fry" , "Mutton Briyani" , "\
Curry Chicken Briyani" , "Fried Chicken Briyani" , "Sambal Chicken Briyani" , "\
Fish briyani" , "BBQ Chicken" , "Ayam Penyet" , "Fish Fillet" , "Ayam Penyet Fried Rice" , "\
Fried Chicken White Rice" , "Mee Rebus" , "Mee Siam" , " Mee Soto" , "Lantong")
 
foodcourt_anything=("Chargrill Chicken Set" , "Black Pepper Chicken Set" , "\
Fried Bread Crumbs Chicken Set" , "Jumbo Chicken Sausage Set" , "Karaage Chicken Set" , "\
Grill Fish With Italian Herb Set" , "Fried Bread Crumbs Fish Set" , "\
Grill Blacked Pepper Fish Set" , "Grill Satman Fillet Set" , "\
Grill Pork Chop With Pepper Set" , "Grill Sirioin Steak Set" , "\
Fried Bread Crumbs Pork Set" , "Rib Eye Steak Set" , "\
Chicken Spaghetti With Cream Sauce" , "Chicken Bolognese" , "\
Karaage Chicken Spaghetti With Tomato Sauce", "Chicken Aglio-Olio Spicy" , "\
Karaage Aglio-Olio Spicy" , "Beef Noodle" , "Spicy Beef Noodle" , "\
Grilled Meat Noodle" , "Chicken Noodle" , "Grilled Chicken Rice" , "\
Grilled Pork Rice" , "Meat Rolls" , "Claypot Chicken" , "Claypot Pork Ribs" , "\
Claypot Beef" , "Claypot Seafood" , "Hotplate Saba Set" , "Hotplate Pork Set" , "\
Hotplate Chicken and Beef Set" , "Hotplate Chicken Set" , "Biang Biang Noodle" , "\
Spicy And Sour Noodle" , "Zha Jiang Noodle" , "Hui Ma Shi" , "\
Fried Egg With Tomato Noodle" , "Hot And Dry Noodle" , "Chinese Hambuger" , "\
Seasame Liang Pi" , "Steamed Vegetables" , "Jian Boo" , "Pancake With Green Onion" , "\
Dumpling" , "Wanton Soup" , "Yogurt Ice Cream" , "Laksa" , "Kway Chap" , "Prawn Mee Noodle" , "Mee Rebus" , "\
Vegetarian Bee Hoon Set" , "Vegetarian Rice Set" , "Beef Steak" , "Chicken Chop" , "\
Chicken Cutlet" , "Fisn And Chips" , "American Breakfast Set" , "Beef Steak Rice" , "\
Chicken Chop Rice" , "Chicken Cutlet Rice" , "Fish and Chips Rice" , "\
Chicken Popcorn Rice" , "Sausage Rice" , "Spaghetti With Chicken Cutlet","Spaghetti With Chicken Chop","Spaghetti With Fish And Chips","Spaghetti With Beef Steak","\
Spaghetti With Sausage","Spaghetti With Popcorn","Mixed Pork Soup","Pig's Liver Soup","Lean Meat Soup","Meat Ball Soup","\
Bak Kut Teh","Salted Fish Soup","Assorted Soup","Roasted Duck Rice","Char Siew Rice","Char Siew Noodle","Roasted Duck Rice","\
Char Siew Roasted Meat Noodle","Cai Fan","Chicken Rice","Mushroom Minced Meat Noodle","Fishball Noodle","Yong Tau Fu Soup","Curry Yong Tau Fu","\
Fishball Vermicelli Soup","Fishball Soup","Yong Tau Fu Dry","Spicy Yong Tau Fu","Tom Yam Yong Tau Fu","Laksa Yong Tau Fu","Fried Beef Hor Fun","\
Seafood Ee Mee","Seafood Bee Hoon","Seafood Hokkien Mee","Sambai Chicken Fried Rice","Ginger And Onion Pork Rice","Salted Fish Fried Rice","Kung Boo Chicken Rice","\
Fried Rice With Prawn","Black Pepper Chicken Rice","Fried Rice With Fillet","Ginger And Onion Chicken Rice","Chicken Fried Rice","Pan Fried Chicken Rice","Ban Mian/Mee Hoon Kway","\
Sichuan Veg Ban Mian","Sliced Fish Ban Mian","Seafood Soup","U Mian","Dumpling Ban Mian","sliced Fish Bee Hoon","Fish Porridge","Mee Sua","Tom Yam Ban Mian","\
Fried Dumpling","Yi Mian","Spicy N Spicy Noodle","Fried Fish Soup","Steamed Dumpling","Thin Bee Hoon","Zha Jiang Mian","Sliced Fish Soup",\
"Plain Naan" , "Garlic Naan" , "Butter Naan" , "Cheese Naan" , "\
Tandoori Roti" , "Dahi" , "Gobi Mutter" , "Chaana Masala" , "Aloo Fry Masala" , "\
Curry Chicken" , "Mutton Masala" , "Bindi Masala" , "Fry Chicken" , "\
Paneer Butter Masala" , "Vegetarian Briyani Dahi Aloo Fry" , "Mutton Briyani" , "\
Curry Chicken Briyani" , "Fried Chicken Briyani" , "Sambal Chicken Briyani" , "\
Fish briyani" , "BBQ Chicken" , "Ayam Penyet" , "Fish Fillet" , "Ayam Penyet Fried Rice" , "\
Fried Chicken White Rice" , "Mee Rebus" , "Mee Siam" , " Mee Soto" , "Lantong")


kfc_alacarte=["Zinger Burger","Caesar Roast Burger","Shrooms Fillet Burger","Fish Ole Burger","Crispy Tenders Burger",\
"Cheesy BBQ Meltz","Pockett Bandito","Original Recipe Rice Bucket","Spicy Sambal Rice Bucket","Curry Rice Bucket",\
"Roast Chicken Salad","Ordinary Salad"]

kfc_meals=["3 pcs Chicken Meal","2 pcs Chicken Meal","All-Chicken Bucket","Shrooms Box","Zinger Box","Pockett Box","Tenders Box",\
"Spicy Sambal Rice Bucket Meal","Original Recipe Rice Bucket Meal","Curry Rice Bucket Meal","Crispy Tenders Burger Meal",\
"Fish Ole Meal","Shrooms Fillet Burger Meal","Crispy Tenders (2 pcs) Snackers","Popcorn Chicken Snackers","Nuggets (4 pcs) Snackers",\
"Wing Snackers"]

kfc_am=["Original Recipe Porridge and Youtiao","Original Recipe Platter","Pancakes and Turkey Bacon Platter","Original Recipe Twister",\
"American Twister","Riser","Brekkie","Fish Ole","Hash Brown","Egg Tart"]


sub_sandwich=["Chicken & Bacon Ranch","Chicken Teriyaki","Cold Cut Trio","Egg Mayo","Italian B.M.T.","Meatball Marinara Melt",\
"Roast Beef","Roasted Chicken Breast","Steak & Cheese","Subway Club","Ham","Subway Melt","Tuna","Turkey","Veggie Delite",\
"Veggie Patty"]

sub_salad=["Cold Cut Trio","Chicken & Bacon Ranch","Chicken Teriyaki","Egg Mayo","Ham","Italian B.M.T.","Meatball Marinara Melt",\
"Roast Beef","Roasted Chicken Breast","Steak & Cheese","Subway Club","Subway Melt","Tuna","Turkey","Veggie Delite","Veggie Patty"]

suggestion = ["How about " , "Do you want to try " , "Is it time for " , "Om nom nom nom --> " , "Shall we have some " , "Why not grab a bite of ","Let's get ",\
"Why don't you try ", "You could go for ","Perhaps you could try "]

#MCBREAKFASTLIST
quote_page = "https://www.mcdonalds.com.sg/our-food/mcdonalds/breakfast/"
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
breakfast = soup.findAll(attrs={'class': 'product-type__title'})
 
 
list=[]
for i in breakfast:
    a = i.text.strip()
    list.append(a)
 
breakfast_list=(list[1:14]) 

#MCLUNCHLIST

quote_page = "https://www.mcdonalds.com.sg/our-food/mcdonalds/non-breakfast/"
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
lunch = soup.findAll(attrs={'class': 'product-type__title'})
 
list=[]
for i in lunch:
    a = i.text.strip()
    list.append(a)
 
lunch_list = list[1:19] 


#PIZZAHUT'S PIZZA LIST

quote_page = "http://www.pizzahut.com.sg/dine_in/menu/restaurants-pizza.aspx"
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
pizza = soup.findAll(attrs={'class': 'panel-container'})
 
pizza_html=(random.choice(pizza).text.strip())
 
list = [pizza_html]               
 
for words in list:
    list = words.splitlines()     
 
                
 
pizza_list = []                 
 
for i in list:
    if len(i) > 0:
        pizza_list.append(i)
        
        
#PIZZAHUT'S PASTA LIST

quote_page = "http://www.pizzahut.com.sg/dine_in/menu/restaurants-pasta.aspx"
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
pasta = soup.findAll(attrs={'class': 'panel-container'})
 
pasta_html=(random.choice(pasta).text.strip())
 
list = [pasta_html]               
 
for words in list:
    list = words.splitlines()  
 
                
 
pasta_list = []                  
 
for i in list:
    if len(i) > 0:
        pasta_list.append(i)

#PIZZAHUT'S BAKED RICE LIST

quote_page = "http://www.pizzahut.com.sg/dine_in/menu/restaurants-bakedpastanrice.aspx"
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
bakedrice = soup.findAll(attrs={'class': 'panel-container'})
 
bakedrice_html=(random.choice(bakedrice).text.strip())
 
list = [bakedrice_html]               
 
for words in list:
    list = words.splitlines()  
 
                
 
bakedrice_list = []                  
 
for i in list:
    if len(i) > 0:
        bakedrice_list.append(i)
        
#PIZZAHUT'S ENTREE LIST

quote_page = "http://www.pizzahut.com.sg/dine_in/menu/restaurants-entree.aspx"
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, 'html.parser')
entree = soup.findAll(attrs={'class': 'panel-container'})
 
entree_html=(random.choice(entree).text.strip())
 
list = [entree_html]               
 
for words in list:
    list = words.splitlines()  
 
                
 
entree_list = []                  
 
for i in list:
    if len(i) > 0:
        entree_list.append(i)
        
        








def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(content_type, chat_type, chat_id)

    if content_type == 'text':
        print ("Received texts:" + msg['text'])
        understand(chat_id,msg['text'])
        
def understand(chat_id, txt):
	txt = txt.lower()
	if "/start" in txt or "hello" in txt or "start" in txt or "restart" in txt:
		bot.sendMessage(chat_id, "Hello, I'm a little bot! I can advice you on what food to eat at NorthSpine! ")
		
	if "/start" in txt or "hello" in txt or "start" in txt or "restart" in txt or "no" in txt:
	
		keyboard = [
    		['Foodcourt', 'FastFood'],   		
		]
	
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id, 'Please choose your preferred location.', reply_markup=reply_markup)

#FOODCOURT
	
	elif "foodcourt" in txt:
		keyboard = [
    		['Halal', 'Anything'], 
    		['Restart'],    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id, 'Please choose your preferred choice.', reply_markup=reply_markup)	
	elif "halal" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(foodcourt_halal))+"?")
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
		
	elif "anything" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(foodcourt_anything))+"?")
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
		

#FASTFOOD
	
	
	elif "fastfood" in txt:
		keyboard = [
    		[ "McDonalds" , "KFC"], 
    		["Pizzahut" , "Subway" ],		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id, 'Please choose your preferred choice.', reply_markup=reply_markup)

#MCDONALDS	
	
	elif "mcdonalds" in txt:
		keyboard = [
    		[ "McBreakfast" , "Lunch/Dinner"],
			['Restart'],	
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id, 'Please choose your preferred choice.', reply_markup=reply_markup)

	elif "mcbreakfast" in txt:
		
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(breakfast_list))+"?")
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
		
	elif "lunch/dinner" in txt:	
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(lunch_list))+"?")
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
	
	
	
#KFC
		
	elif "kfc" in txt :
		keyboard = [
    		['Alacarte','Meals'],
    		['AM','Restart'],		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Please choose one of the following categories!', reply_markup=reply_markup)
	elif "alacarte" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(kfc_alacarte))+"?")
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
			
	elif "meals" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(kfc_meals))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
		
	elif "am" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(kfc_am))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
		
	
#PIZZAHUT
	
	elif "pizzahut" in txt :
		keyboard = [
    		['Pizza','Pasta'],
    		['BakedRice','Entrée'],
    		['Restart'],
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Please choose one of the following categories!', reply_markup=reply_markup)
		
	elif "pizza" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(pizza_list))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)

	elif "pasta" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(pasta_list))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)

	elif "bakedrice" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(bakedrice_list))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)

	elif "entrée" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(entree_list))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
	
		
		
		
		
#SUBWAY
	
	elif "subway" in txt :
		keyboard = [
    		['Sandwiches','Salads'],
    		['Restart'],
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Please choose one of the following categories!', reply_markup=reply_markup)
	elif "sandwiches" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(sub_sandwich))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
		
	elif "salads" in txt:
		bot.sendMessage(chat_id,(random.choice(suggestion))+(random.choice(sub_salad))+"?")	
		keyboard = [
    		['YES!','NO!'],
    		
		]
		reply_markup = ReplyKeyboardMarkup.create(keyboard)
		bot.sendMessage(chat_id,'Are you satisfied with the choice given ?', reply_markup=reply_markup)
	
#DECISIONAL CHOICE
	
	elif "yes" in txt:
		bot.sendMessage(chat_id,"Thank you for using FOODIEGRAM! HAVE A NICE DAY! Type '/start' to restart the program!")
		
	
	
	
TOKEN = ("262877045:AAESYCfi29ymGcBTd44S-e8emMbl6S4k9rA")  # get token from command-line

bot = telepot.Bot(TOKEN)
bot.message_loop(handle)
print ('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)