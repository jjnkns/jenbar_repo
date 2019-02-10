from flask import Flask, render_template
from flask import request
import mysql.connector as mc
import cbpro
import requests
import json
import datetime
import time

BUY=1
SELL=2

app = Flask(__name__)

@app.route('/')
def main_page():
        #this will render the main page by default
        return render_template(
        "index.html",
        title="Hello, Flask, this is Jennifer",
        content = get_price('BTC-USD', 'spot'),
        eth_price=get_price('ETH-USD', 'spot'))
        #content="this is where content goes",
        #prices=get_price('BTC-USD', 'spot'))
        #return render_template('index.html')
        #{prices} = print(get_price('BTC-USD', 'spot'),# get_price('ETH-USD', 'spot'), get_price('LTC-USD', 'spot'))

@app.route('/buy')
def buy():
        #this will render the page where customers can buy
        return render_template('buy.html')

@app.route('/sell')
def sell():
        #this will render the page where customers can sell
        return render_template('sell.html', products=['ETH','LTC','BTC'])

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
        


# def get_connection():
#     #returns a connection object
#     connection = mc.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
#     auth_plugin='mysql_native_password')
#     return connection

# def add_customer(first_name, middle_name, last_name):
#      connection = get_connection()
#      cursor = connection .cursor()
#      sql = ("INSERT INTO customer2 "
#                "(customer_first_name, customer_middle_name, customer_last_name) "
#                "VALUES (%s, %s, %s)")

#      val = (first_name, middle_name, last_name)
     
#      cursor.execute(sql, val)
     
#      connection.commit()
#      print('Welcome',first_name, '. Your customer id number is', str(cursor.lastrowid), 'Please retain this for your records')

# class Trade:
#     def __init__(self,a, q,c,p,sd):
#         self.__account_id = a
#         self.__quantity = q
#         self.__currency = c
#         self.__price = p
#         self.__side = sd
#     def get_trade(self):
#         return self.__quantity, self.__currency, self.__price
#     def get_dollars(self):
#         return self.__price * self.__quantity

def get_price(currency_type, price_type):
    my_url = 'https://api.coinbase.com/v2/prices/'
    my_url = my_url+currency_type+"/"+price_type
    response=requests.get(my_url)
    data = response.json()
    #currency = data["data"]["base"]
    price = data["data"]["amount"]
    #print("Currency:", currency, "Sell Price:", price, "as of", datetime.datetime.now())
    as_of_datetime=str(datetime.datetime.now())
    return currency_type, price, as_of_datetime
    #currency_type, price_type, currency, price, str(datetime.datetime.now())


# def make_trade(account_id, currency_id, quantity, side):
#         currency_short_name = currency_dict[currency_id]
#         price = get_price(currency_short_name, side)
#         trade_value = float(quantity)*float(price)
#         print("$",price)
        
         
#         connection = get_connection()
#         cursor = connection .cursor()
#         sql = ("INSERT INTO transaction "
#                "(customer_id, currency_id, side_id, quantity, price, transaction_datetime )"
#                "VALUES (%s, %s, %s,%s,%s,%s)")

#         val = (account_id, currency_id, quantity, price, side, datetime.datetime())
     
#         cursor.execute(sql, val)
#         connection.commit()
#         return side, trade_value

# #make_trade(14, 0, 23.5, 'buy')

# class Customer:
#         def __init__(self,f,m,l):
#                 self.__first_name = f
#                 self.__middle_name = m
#                 self.__last_name =l
#         def get_customer(self, id):
#                 return self.__first_name, self.__middle_name, self.__last_name
# class Account:
#         def __init__(self, currency_id, quantity):
#                 #self.__customer_id=customer_id
#                 self.__currency_id =currency_id
#                 self.__quantity= quantity
#         def get_account(self, id):
#                 sql = ("Select * from account inner join customer on account.customer_id = customer.customer_id inner join currency on account.currency_id = currency.currency_id where account_id =%s")
#                 val = id
#                 connection = get_connection()
#                 cursor = connection .cursor()
#                 result= cursor.execute(sql, val)
#                 return result
#         def update_account(self, customer_id, currency_id, quantity, side_id):
#                 if side_id ==1:
#                          sql = ("UPDATE account set quantity = quantity+%s "
#                         " where customer_id = %s and currency_id = %s")
#                 elif side_id==2:
#                         sql = ("UPDATE account set quantity = quantity-%s "
#                         " where customer_id = %s and currency_id = %s")
#                 val = (customer_id, currency_id, quantity, side_id)

#                 connection = get_connection()
#                 cursor = connection .cursor()
               
#                 val = (customer_id, currency_id, quantity)
     
#                 cursor.execute(sql, val)
#                 connection.commit()
#                 print(sql, val)

# acct1 = Account(4,1)
# acct2 = Account(5,1)
# acct3 = Account(3,1)

# acct1.update_account(float(20.234),0,1,BUY)
# acct2.update_account(float(40.12),0,2,BUY)
# acct1.update_account(float(60.07),0,3,BUY)

# acct1.update_account(3,0,1,SELL)
# acct1.update_account(4,0,2,SELL)
# acct1.update_account(5,0,3,SELL)



# def run_query_test(query,args):
#     connection = get_connection()
#     sql_select_Query = 'select * from currency where currency_short_name = %s (arg)'
#     arg = 'BTC'
#     cursor = connection .cursor()
#     cursor.execute(sql_select_Query, arg)
#     records = cursor.fetchall()
#     print("Total number of currencies is - ", cursor.rowcount)
#     print(records)
#     cursor.close()

# def get_currency_detail(currency_short_name):
#     import mysql.connector
#     mydb = mysql.connector.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
#         auth_plugin='mysql_native_password')

#     mycursor = mydb.cursor()

#     sql = "SELECT currency_symbol, currency_short_name, currency_long_name FROM currency WHERE currency_short_name = %s"
#     nam = (currency_short_name,)

#     mycursor.execute(sql, nam)

#     myresult = mycursor.fetchall()

#     for x in myresult:
#         print(x)

# currency_list = ('BTC','LTC','ETH')

# for n in range(0,len(currency_list)):
#     get_currency_detail(currency_list[n])

# add_customer('Mary','Joan','Gibson')


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

    