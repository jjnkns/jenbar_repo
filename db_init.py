from flask import Flask, render_template
from flask import request
import mysql.connector as mc
import cbpro
import requests
import json
import datetime
import time




# #dictionary for currency types
currency_dict= {0:'BTC-USD',2:'LTC-USD',5:'ETH-USD'}
# #key is the same as currency id in database

# public_client = cbpro.PublicClient()
# mydict = public_client.get_currencies()

# def main():
#     return render_template('index.html')


# def load_currency_list():
#     for n in range(0,len(mydict)):
                
#         query ='insert into currency(currency_id, currency_symbol, currency_long_name, currency_short_name) values(%s,%s,%s,%s)'
#         args = (n, mydict[n]['details']['symbol'], mydict[n]['name'], mydict[n]['id'])


#         run_query(query,args)
 
#         print('------------------------------')
        


def get_connection():
    #returns a connection object
    connection = mc.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
    auth_plugin='mysql_native_password')
    return connection

def add_customer(first_name, middle_name, last_name, user_name, email_address):
     connection = get_connection()
     cursor = connection .cursor()
     sql = ("INSERT INTO customer "
               "(first_name, middle_name, last_name, user_name, email_address) "
               "VALUES (%s, %s, %s,%s,%s)")

     val = (first_name, middle_name, last_name, user_name, email_address)
     
     cursor.execute(sql, val)
     
     connection.commit()
     print('Welcome',first_name, '. Your customer id number is', str(cursor.lastrowid), 'Please retain this for your records')

def add_currency(currency_short_name, currency_long_name, currency_symbol, country_currency):
        connection = get_connection()
        cursor = connection .cursor()
        sql = ("INSERT INTO currency "
               "(currency_short_name, currency_long_name, currency_symbol, country_currency) "
               "VALUES (%s, %s, %s,%s)")

        val = (currency_short_name, currency_long_name, currency_symbol, country_currency)
     
        cursor.execute(sql, val)
     
        connection.commit()

def add_account(currency_id, quantity):
     connection = get_connection()
     cursor = connection .cursor()
     sql = ("INSERT INTO cust_account "
               "(currency_id, quantity) "
               "VALUES (%s, %s)")

     val = (currency_id, quantity)
     
     cursor.execute(sql, val)
     
     connection.commit()

def add_cust_account_assoc(customer_id, account_id):
        connection = get_connection()
        cursor = connection.cursor()
        sql = ("INSERT INTO cust_acct_assoc "
                "(customer_id, account_id) "
                "VALUES(%s,%s)")
        val = (customer_id, account_id)

        cursor.execute(sql, val)
        connection.commit()

add_currency('BTC','Bitcoin','₿','USD')
add_currency('LTC','Litecoin','Ł','USD')
add_currency('ETH','Ethereum','Ξ','USD')

add_customer('Abby', 'Jane', 'Phillips', 'AbbyJay', 'AbbyJay@gmail.com')

#add_cust_account_assoc(0,6)
#add_cust_account_assoc(0,7)
#add_cust_account_assoc(0,8)



#add_account(4,0)
#add_account(5,0) 
#add_account(6,0)   


def get_price(currency_type, price_type):
    my_url = 'https://api.coinbase.com/v2/prices/'
    my_url = my_url+currency_type+"/"+price_type
    response=requests.get(my_url)
    data = response.json()
    #currency = data["data"]["base"]
    price = data["data"]["amount"]
    #print("Currency:", currency, "Sell Price:", price, "as of", datetime.datetime.now())
    as_of_datetime=str(datetime.datetime.now())
    return currency_type, price_type, '$'+price, as_of_datetime
    #currency_type, price_type, currency, price, str(datetime.datetime.now())

# import cbpro
# public_client = cbpro.PublicClient()
# mydict = public_client.get_currencies()

# for n in range(0,len(mydict)):
#     print(mydict[n]['id'], mydict[n]['name'],mydict[n]['details']['symbol'])
#     print('------------------------------')


# https://www.youtube.com/watch?v=tdmccmKDFFw
# code borrowed from youtube demo by Flopperam


#currency_menu = ['BTC-USD', 'ETH-USD', 'LTC-USD']


#market order -- whatever price comes up when you hit submit to buty
#limit order -- with 

#refresh every five seconds
# counter=0
# starttime=time.time()
# while counter<20:
#     currency_type, price_type, currency, price, formatted_date =get_price('LTC-USD','spot')
#     print(price_type, 'price of', currency_type, 'as of', formatted_date, 'is', price)
#     time.sleep(5.0 - ((time.time() - starttime) % 5.0))
#     counter+=1

# for k, v in currency_dict.items():
#      currency_type, price_type, currency, price, formatted_date =get_price(currency_dict(k),'spot')
#      print(price_type, 'price of', currency_type, 'as of', formatted_date, 'is', price)

    