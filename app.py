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
        #get the spot prices from Coinbase API
        btc_spot_price=locale.currency( float(get_price('BTC-USD','spot')), grouping=True)
        eth_spot_price=locale.currency( float(get_price('ETH-USD','spot')), grouping=True)
        ltc_spot_price=locale.currency( float(get_price('LTC-USD','spot')), grouping=True)
        
        cd_btc_price, cd_btc_price_time=get_coindesk_btc_price()
        #time when we got price from the API
        coinbase_timestamp=datetime.datetime.now()
        coinbase_timestamp=coinbase_timestamp.strftime("%m/%d/%y at %I:%M %p")
        cd_btc_price=locale.currency( float(cd_btc_price),grouping=True)
        
        account_balance=get_account_balance(0)
        
        return render_template(
        "index.html",
        title="Jenbar Crypto",
        btc_spot_price=btc_spot_price, eth_spot_price=eth_spot_price, ltc_spot_price=ltc_spot_price,
        cd_btc_price=cd_btc_price, cd_btc_price_time=cd_btc_price_time, coinbase_timestamp=coinbase_timestamp,
        account_balance=account_balance)

@app.route('/form',methods=['GET','POST'])
def form_login():

        if request.method == 'POST':
                first_name=request.form['first_name']
                middle_name=request.form['middle_name']
                last_name=request.form['last_name']
                user_name=request.form['email']
                email_address=request.form['email']
                add_customer(first_name, middle_name, last_name, user_name, email_address)

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
                
                customer_id = request.form['customer_id_number']
                
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

                #make_trade(account_id, currency_short_name, currency_id, quantity, side):
                if btc_qty>0:
                        make_trade(6,'BTC-USD',btc_currency_id, btc_qty, 'buy')
                if eth_qty>0:
                        make_trade(6,'ETH-USD',eth_currency_id, eth_qty, 'buy')
                if ltc_qty>0:
                        make_trade(6,'LTC-USD',ltc_currency_id, ltc_qty, 'buy')

               


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
def get_account_id(customer_id,curreny_id):
        
        return account_id

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
     #create an customer with 4 accounts-one for USD cash and one for each crypto
     #initalize balance as 0
     connection = get_connection()
     cursor = connection.cursor()
     sql = ("INSERT INTO customer "
               "(first_name, middle_name, last_name, user_name, email_address) "
               "VALUES (%s, %s, %s,%s,%s)")

     val = (first_name, middle_name, last_name, user_name, email_address)
     
     cursor.execute(sql, val)
     connection.commit()
     customer_id = str(cursor.lastrowid)
     
     quantity=0
     sql = ("SELECT currency_id from currency")
     cursor = connection.cursor()
     cursor.execute(sql)
     data=cursor.fetchall()
     for row in data :
             currency_id = row[0]
             account_id = add_account(currency_id,quantity)
             add_cust_account_assoc(customer_id, account_id)
       
     connection.commit()
     print('Welcome',first_name, '. Your customer id number is', customer_id, 'Please retain this for your records')
     return customer_id

def add_currency(currency_short_name, currency_long_name, currency_symbol, country_currency):
        connection = get_connection()
        cursor = connection .cursor()
        sql = ("INSERT INTO currency "
               "(currency_short_name, currency_long_name, currency_symbol, country_currency) "
               "VALUES (%s, %s, %s,%s)")

        val = (currency_short_name, currency_long_name, currency_symbol, country_currency)
     
        cursor.execute(sql, val)
     
        connection.commit()
        currency_id=cursor.lastrowid
        cursor.close()
        connection.close()
        return currency_id

def get_currency_dict():

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT currency_short_name, currency_id FROM currency")
        currency_dict={}
        for row in cursor:
                key=row[0]
                value=row[1]
                currency_dict.update({key:value})
        return currency_dict

currency_dict=get_currency_dict() 
print(currency_dict)
       
btc_currency_id=currency_dict['BTC']
ltc_currency_id=currency_dict['LTC']
eth_currency_id=currency_dict['ETH']
usd_currency_id=currency_dict['USD']

def add_account(currency_id, quantity):
     connection = get_connection()
     cursor = connection .cursor()
     sql = ("INSERT INTO cust_account "
               "(currency_id, quantity) "
               "VALUES (%s, %s)")

     val = (currency_id, quantity)
     
     cursor.execute(sql, val)
     
     connection.commit()
     account_id=cursor.lastrowid
     cursor.close()
     connection.close()
     return account_id
     

def add_cust_account_assoc(customer_id, account_id):
        connection = get_connection()
        cursor = connection.cursor()
        sql = ("INSERT INTO cust_acct_assoc "
                "(customer_id, account_id) "
                "VALUES(%s,%s)")
        val = (customer_id, account_id)

        cursor.execute(sql, val)
        connection.commit()
        cust_acct_assoc_id= cursor.lastrowid
        cursor.close()
        connection.close()
        return cust_acct_assoc_id

def get_price(currency_type, price_type):
    my_url = 'https://api.coinbase.com/v2/prices/'
    my_url = my_url+currency_type+"/"+price_type
    response=requests.get(my_url)
    data = response.json()
    price = data["data"]["amount"]
    return price
    
#at this time we can only use a Coindesk api for bitcoin only, not ETH or LTC
def get_coindesk_btc_price():
        my_url='https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
        response=requests.get(my_url)
        data = response.json()
        coindesk_btc_price= data['bpi']['USD']['rate_float']
        coindesk_btc_price_time=data["time"]["updated"]
        return coindesk_btc_price, coindesk_btc_price_time


       
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



#use cust account #6 for practice
#accounts: 6=BTC,7=LTC,8=ETH,9=CASH
#currencies: 4=BTC,5=LTC,6=ETH,7=CASH
def make_trade(account_id, currency_short_name, currency_id, quantity, side):
 
        #coinbase price
        price = get_price(currency_short_name, side)

        trade_value = float(quantity)*float(price)
        trans_sql = "INSERT INTO acct_transaction (account_id, currency_id, side, quantity, price) VALUES (%s, %s, %s,%s,%s)"
        trans_val = (account_id, currency_id, side, quantity, price)
        
        acct_val = (quantity, 6, 4)
        if side=='buy':
                acct_sql = ("UPDATE cust_account set quantity=quantity+%s where account_id=%s and currency_id =%s")
                
        else:
                acct_sql = ("UPDATE cust_account set quantity=quantity-%s where account_id=%s and currency_id =%s")
                
        
        #return trade_value
        
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(trans_sql, trans_val)
        connection.commit()
        cursor.close()
        
        cursor = connection.cursor()
        cursor.execute(acct_sql, acct_val)
        connection.commit()
        connection.close()
#         return side, trade_value

# #make_trade(14, 0, 'buy', 23.5)

def get_account_balance(customer_id):
        sql = ("Select currency_long_name, currency_symbol, quantity, last_update from customer_balance where customer_id=22")
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql)
       
        for (currency_long_name, currency_symbol, quantity, last_update) in cursor:
                print("{} {}{:.4f} Last updated on {:%m/%d/%Y at %I:%M %p}".format(
                currency_long_name, currency_symbol, quantity, last_update))

        cursor.close()
        connection.close()
get_account_balance(22)

def fund_cash_account(customer_id, amount):
        pass

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


# import cbpro
# public_client = cbpro.PublicClient()
# mydict = public_client.get_currencies()

# for n in range(0,len(mydict)):
#     print(mydict[n]['id'], mydict[n]['name'],mydict[n]['details']['symbol'])
#     print('------------------------------')


# https://www.youtube.com/watch?v=tdmccmKDFFw
# code borrowed from youtube demo by Flopperam


#currency_menu = ['BTC-USD', 'ETH-USD', 'LTC-USD']

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

    