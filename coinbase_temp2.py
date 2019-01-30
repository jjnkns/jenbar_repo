import cbpro
public_client = cbpro.PublicClient()
mydict = public_client.get_currencies()

for n in range(0,len(mydict)):
    print(mydict[n]['id'], mydict[n]['name'],mydict[n]['details']['symbol'])
    print('------------------------------')


# https://www.youtube.com/watch?v=tdmccmKDFFw
# code borrowed from youtube demo by Flopperam
import requests
import json
import datetime
import time

currency_menu = ['BTC-USD', 'ETH-USD', 'LTC-USD']

def get_price(currency_type, price_type):
    my_url = 'https://api.coinbase.com/v2/prices/'
    my_url = my_url+currency_type+"/"+price_type
    response=requests.get(my_url)
    data = response.json()
    currency = data["data"]["base"]
    price = data["data"]["amount"]
    #print("Currency:", currency, "Sell Price:", price, "as of", datetime.datetime.now())
    str(datetime.datetime.now())
    return currency_type, price_type, currency, price, str(datetime.datetime.now())


#refresh every five seconds
counter=0
starttime=time.time()
while counter<20:
    currency_type, price_type, currency, price, formatted_date =get_price('LTC-USD','spot')
    print(price_type, 'price of', currency_type, 'as of', formatted_date, 'is', price)
    time.sleep(5.0 - ((time.time() - starttime) % 5.0))
    counter+=1

# for n in currency_menu:
#     currency_type, price_type, currency, price, formatted_date =get_price(currency_menu[n],'spot')
#     print(price_type, 'price of', currency_type, 'as of', formatted_date, 'is', price)
