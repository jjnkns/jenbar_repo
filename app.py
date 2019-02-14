from flask import Flask, render_template
from flask import request
import mysql.connector as mc
import cbpro #coinbase pro 
import requests
import json
import datetime
import time
import locale #useful for formatting-
import tzlocal
from dateutil import tz


locale.setlocale( locale.LC_ALL, '' )
'English_United States.1252'

local_timezone=tzlocal.get_localzone()


BUY=1
SELL=2

app = Flask(__name__)

@app.route('/')
def main_page():
        #this will render the main page by default

        btc_spot_price=locale.currency( float(get_price('BTC-USD','spot')), grouping=True)
        eth_spot_price=locale.currency( float(get_price('ETH-USD','spot')), grouping=True)
        ltc_spot_price=locale.currency( float(get_price('LTC-USD','spot')), grouping=True)
        
        cd_btc_price, cd_btc_price_time=get_coindesk_btc_price()
        
        
        return render_template(
        "index.html",
        title="Jenbar Crypto",
        btc_spot_price=btc_spot_price, eth_spot_price=eth_spot_price, ltc_spot_price=ltc_spot_price,
        cd_btc_price=cd_btc_price, cd_btc_price_time=cd_btc_price_time)

@app.route('/form')
def form_login():
        return render_template(
        "form.html",
        title="Jenbar Crypto Login")

@app.route('/buy',methods=['GET','POST'])
def buy():
        #this will render the page where customers can buy
       

        btc_buy_price=locale.currency( float(get_price('BTC-USD','buy')), grouping=True)
        eth_buy_price=locale.currency( float(get_price('ETH-USD','buy')), grouping=True)
        ltc_buy_price=locale.currency( float(get_price('LTC-USD','buy')), grouping=True)

        btc_qty=0
        eth_qty=0
        ltc_qty=0

        btc_total=get_price('BTC-USD','buy')*btc_qty
        eth_total=get_price('ETH-USD','buy')*eth_qty
        ltc_total=get_price('LTC-USD','buy')*ltc_qty
        
        if request.method == 'POST':
                
                btc_qty=request.form['btc_qty']
                eth_qty=request.form['eth_qty']
                ltc_qty=request.form['ltc_qty']

                if not btc_qty=="":
                        btc_qty=float(btc_qty)
                else:
                        btc_qty=0

                if not eth_qty=="":
                        eth_qty=float(eth_qty)
                else:
                        eth_qty=0
                if not ltc_qty=="":
                        ltc_qty=float(ltc_qty)
                else:
                        ltc_qty=0

                btc_total=0
                eth_total=0
                ltc_total=0

                if float(btc_qty)>0:
                        btc_total=float(get_price('BTC-USD','buy'))*float(btc_qty)
                if float(eth_qty)>0:
                        eth_total=float(get_price('ETH-USD','buy'))*float(eth_qty)
                if float(ltc_qty)>0:
                        ltc_total=float(get_price('LTC-USD','buy'))*float(ltc_qty)

                #format the prices and totals nicely

                btc_total=locale.currency( float(btc_total), grouping=True )
                eth_total=locale.currency( float(eth_total), grouping=True )
                ltc_total=locale.currency( float(ltc_total), grouping=True )

                btc_buy_price=locale.currency( float(get_price('BTC-USD','buy')), grouping=True)
                eth_buy_price=locale.currency( float(get_price('ETH-USD','buy')), grouping=True)
                ltc_buy_price=locale.currency( float(get_price('LTC-USD','buy')), grouping=True)
               


        return render_template('buy.html',
        title="Jenbar Crypto Buy Page",
        btc_buy_price=btc_buy_price, eth_buy_price=eth_buy_price, ltc_buy_price=ltc_buy_price,
        btc_total=btc_total, eth_total=eth_total, ltc_total=ltc_total)

@app.route('/sell')
def sell():
        #this will render the page where customers can sell
        btc_sell_price=locale.currency( float(get_price('BTC-USD','sell')), grouping=True)
        eth_sell_price=locale.currency( float(get_price('ETH-USD','sell')), grouping=True)
        ltc_sell_price=locale.currency( float(get_price('LTC-USD','sell')), grouping=True)

        btc_qty=0
        eth_qty=0
        ltc_qty=0

        btc_total=get_price('BTC-USD','sell')*btc_qty
        eth_total=get_price('ETH-USD','sell')*eth_qty
        ltc_total=get_price('LTC-USD','sell')*ltc_qty
        
        if request.method == 'POST':
                
                btc_qty=request.form['btc_qty']
                eth_qty=request.form['eth_qty']
                ltc_qty=request.form['ltc_qty']

                if not btc_qty=="":
                        btc_qty=float(btc_qty)
                else:
                        btc_qty=0

                if not eth_qty=="":
                        eth_qty=float(eth_qty)
                else:
                        eth_qty=0
                if not ltc_qty=="":
                        ltc_qty=float(ltc_qty)
                else:
                        ltc_qty=0

                btc_total=0
                eth_total=0
                ltc_total=0

                if float(btc_qty)>0:
                        btc_total=float(get_price('BTC-USD','sell'))*float(btc_qty)
                if float(eth_qty)>0:
                        eth_total=float(get_price('ETH-USD','sell'))*float(eth_qty)
                if float(ltc_qty)>0:
                        ltc_total=float(get_price('LTC-USD','sell'))*float(ltc_qty)

                #format the prices and totals nicely

                btc_total=locale.currency( float(btc_total), grouping=True )
                eth_total=locale.currency( float(eth_total), grouping=True )
                ltc_total=locale.currency( float(ltc_total), grouping=True )

                btc_sell_price=locale.currency( float(get_price('BTC-USD','sell')), grouping=True)
                eth_sell_price=locale.currency( float(get_price('ETH-USD','sell')), grouping=True)
                ltc_sell_price=locale.currency( float(get_price('LTC-USD','sell')), grouping=True)
               
        return render_template('sell.html',
        title="Jenbar Crypto Sell Page",
        btc_sell_price=btc_sell_price, eth_sell_price=eth_sell_price, ltc_sell_price=ltc_sell_price,
        btc_total=btc_total, eth_total=eth_total, ltc_total=ltc_total)

@app.route('/view_acct')
def view_acct():
        #this will render the page where customer can view account
        return render_template('view_acct.html')
        


# #dictionary for currency types
currency_dict= {0:'BTC-USD',2:'LTC-USD',5:'ETH-USD'}
# #key is the same as currency id in database

# public_client = cbpro.PublicClient()
# mydict = public_client.get_currencies()

# def load_currency_list():
#     for n in range(0,len(mydict)):
                
#         query ='insert into currency(currency_id, currency_symbol, currency_long_name, currency_short_name) values(%s,%s,%s,%s)'
#         args = (n, mydict[n]['details']['symbol'], mydict[n]['name'], mydict[n]['id'])


#         run_query(query,args)
 
#         print('------------------------------')
        

#mysql connectivity
def get_connection():
    #returns a connection object
    connection = mc.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
    auth_plugin='mysql_native_password')
    return connection


def add_customer(first_name, middle_name, last_name, user_name, email_address):
     connection = get_connection()
     cursor = connection.cursor()
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
    return price#, as_of_datetime
    

def get_coindesk_btc_price():
        my_url='https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response=requests.get(my_url)
        data = response.json()
        coindesk_btc_price= data['bpi']['USD']['rate_float']
        coindesk_btc_price_time=data["time"]["updated"]
        return coindesk_btc_price, coindesk_btc_price_time

#there is no coindesk api for ethereum at this time
# def get_coindesk_eth_price():
 
#there is no coindesk api for litecoin at this time   
# def get_coindesk_ltc_price():

       
#         return coindesk_ltc_price, coindesk_ltc_price_time    
        # # Auto-detect zones:
        # from_zone = tz.tzutc()
        # to_zone = tz.tzlocal()

        # # utc = datetime.utcnow()
        # utc = datetime.datetime.month
        # print(utc)

        # Tell the datetime object that it's in UTC time zone since 
        # datetime objects are 'naive' by default
        #utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        #display_price_time = utc.astimezone(to_zone)
        #print(display_price_time)

print(get_price('BTC-USD', 'spot'))
print(get_price('BTC-USD', 'buy'))
print(get_price('BTC-USD', 'sell'))


#use cust account #6 for practice
#accounts: 6=BTC,7=LTC,8=ETH,9=CASH
#currencies: 4=BTC,5=LTC,6=ETH,7=CASH
def make_trade(account_id, currency_short_name, quantity, side):
#      
        #coinbase price
        price = get_price(currency_short_name, side)

        trade_value = float(quantity)*float(price)
#        print("$",price)
        trans_sql = "INSERT INTO transaction (account_id, currency_id, side, quantity, price) "
        "VALUES (%s, %s, %s,%s,%s,%s)"
        trans_val = (account_id, currency_id, side, quantity, price)
        
        if side=='buy':
                acct_sql = ("UPDATE cust_account set quantity=quantity+%s where account_id=%s and currency_id =%s")
                acct_val = (trade_value, account_id, 6)
        else:
                acct_sql = ("UPDATE cust_account set quantity=quantity-%s where account_id=%s and currency_id =%s")
                acct_val = (trade_value, account_id, 6)
        
        #return trade_value
        
        connection = get_connection()
        cursor = connection .cursor()
        cursor.execute(trans_sql, trans_val)
        cursor.execute(acct_sql, trans_val)
        connection.commit()
#         return side, trade_value

# #make_trade(14, 0, 'buy', 23.5)

# class Customer:
#         def __init__(self,f,m,l):
#                 self.__first_name = f
#                 self.__middle_name = m
#                 self.__last_name =l
#         def get_customer(self, id):
#                 return self.__first_name, self.__middle_name, self.__last_name
#class Account:
#         def __init__(self, currency_id, quantity):
#                 #self.__account_id=account_id
#                 self.__currency_id =currency_id
#                 self.__quantity= quantity
def get_account_balance(account_id):
        sql = ("Select * from customer_balance where account_id =%s")
        val = account_id
        connection = get_connection()
        cursor = connection .cursor()
        result= cursor.execute(sql, val)
        return result
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

    