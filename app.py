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

        
        return render_template(
        "index.html",
        title="Jenbar Crypto",
        btc_spot_price=btc_spot_price, eth_spot_price=eth_spot_price, ltc_spot_price=ltc_spot_price,
        cd_btc_price=cd_btc_price, cd_btc_price_time=cd_btc_price_time, coinbase_timestamp=coinbase_timestamp)

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
       
        customer_id=0
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
                
                #lookup account numbers and balances for this customer
                
                btc_acct, btc_symbol, btc_qty_owned, btc_last_update= get_account_balance(customer_id,btc_currency_id)
                ltc_acct, ltc_symbol, ltc_qty_owned, ltc_last_update= get_account_balance(customer_id,ltc_currency_id)
                eth_acct, eth_symbol, eth_qty_owned, eth_last_update= get_account_balance(customer_id,eth_currency_id)
                usd_acct, usd_symbol, usd_qty_owned, usd_last_update= get_account_balance(customer_id,usd_currency_id)

                        
                #if btc_qty>0:
                make_trade(customer_id, btc_acct,'BTC-USD',btc_currency_id, btc_qty, 'buy')
                #if eth_qty>0:
                make_trade(customer_id, eth_acct,'ETH-USD',eth_currency_id, eth_qty, 'buy')
                #if ltc_qty>0:
                make_trade(customer_id, ltc_acct,'LTC-USD',ltc_currency_id, ltc_qty, 'buy')


        return render_template('buy.html',
        title="Jenbar Crypto Buy Page",
        btc_buy_price=btc_buy_price, eth_buy_price=eth_buy_price, ltc_buy_price=ltc_buy_price,
        btc_total=btc_total, eth_total=eth_total, ltc_total=ltc_total,btc_qty=btc_qty, eth_qty=eth_qty, ltc_qty=ltc_qty,
        customer_id=customer_id)

@app.route('/sell', methods=['GET','POST'])
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

        customer_id=0
        
        if request.method == 'POST':
                
                btc_qty=request.form['btc_qty']
                eth_qty=request.form['eth_qty']
                ltc_qty=request.form['ltc_qty']

                customer_id = request.form['customer_id_number']


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

                #lookup account numbers and balances for this customer
                
                btc_acct, btc_symbol, btc_qty_owned, btc_last_update= get_account_balance(customer_id,btc_currency_id)
                ltc_acct, ltc_symbol, ltc_qty_owned, ltc_last_update= get_account_balance(customer_id,ltc_currency_id)
                eth_acct, eth_symbol, eth_qty_owned, eth_last_update= get_account_balance(customer_id,eth_currency_id)
                usd_acct, usd_symbol, usd_qty_owned, usd_last_update= get_account_balance(customer_id,usd_currency_id)
                #this checks to see if there are enough coins in inventory to actually sell
                if btc_qty>0 and btc_qty<=btc_qty_owned:
                        make_trade(customer_id, btc_acct,'BTC-USD',btc_currency_id, btc_qty, 'sell')
                if eth_qty>0 and eth_qty<=eth_qty_owned:
                        make_trade(customer_id, eth_acct,'ETH-USD',eth_currency_id, eth_qty, 'sell')
                if ltc_qty>0 and ltc_qty<=ltc_qty_owned:
                        make_trade(customer_id, ltc_acct,'LTC-USD',ltc_currency_id, ltc_qty, 'sell')

        return render_template('sell.html',
        title="Jenbar Crypto Sell Page",
        btc_sell_price=btc_sell_price, eth_sell_price=eth_sell_price, ltc_sell_price=ltc_sell_price,
        btc_total=btc_total, eth_total=eth_total, ltc_total=ltc_total,btc_qty=btc_qty, eth_qty=eth_qty, ltc_qty=ltc_qty,customer_id=customer_id)

@app.route('/view_acct', methods=['GET','POST'])
def view_acct():
        #this will render the page where customer can view account
        #customer_id = 23
        #initialize the variables
        btc_acct=0
        btc_symbol=0
        btc_qty=0
        btc_last_update=0
        ltc_acct= 0
        ltc_symbol=0
        ltc_qty=ltc_qty=0
        ltc_last_update=0
        eth_acct= 0
        eth_symbol=0
        eth_qty=ltc_qty=0
        eth_last_update=0
        usd_acct= 0
        usd_symbol=0
        usd_qty=ltc_qty=0
        usd_last_update=0
        
        btc_currency_id=currency_dict['BTC']
        ltc_currency_id=currency_dict['LTC']
        eth_currency_id=currency_dict['ETH']
        usd_currency_id=currency_dict['USD']
        #hardcoding customer id temporarily because page breaks if no value
        #better to find out how to test for existence and validity
        customer_id=23

        if request.method == 'POST':
                customer_id = request.form['customer_id_number']
                print("Customer id is",customer_id)
                if int(customer_id)>=23:
                        btc_acct, btc_symbol, btc_qty, btc_last_update= get_account_balance(customer_id,btc_currency_id)
                        ltc_acct, ltc_symbol, ltc_qty, ltc_last_update= get_account_balance(customer_id,ltc_currency_id)
                        eth_acct, eth_symbol, eth_qty, eth_last_update= get_account_balance(customer_id,eth_currency_id)
                        usd_acct, usd_symbol, usd_qty, usd_last_update= get_account_balance(customer_id,usd_currency_id)
                
        #make the dates look better
                
        if isinstance(btc_last_update,datetime.date):
                btc_last_update = btc_last_update.strftime("%m/%d/%y at %I:%M %p")
        if isinstance(ltc_last_update,datetime.date):
                ltc_last_update = ltc_last_update.strftime("%m/%d/%y at %I:%M %p")
        if isinstance(eth_last_update,datetime.date):
                eth_last_update = eth_last_update.strftime("%m/%d/%y at %I:%M %p")
        if isinstance(usd_last_update,datetime.date):
                usd_last_update = usd_last_update.strftime("%m/%d/%y at %I:%M %p")


        return render_template('view_acct.html',customer_id=customer_id,
        btc_acct= btc_acct, btc_symbol=btc_symbol,  btc_qty=btc_qty, btc_last_update=btc_last_update,
        ltc_acct= ltc_acct, ltc_symbol=ltc_symbol,  ltc_qty=ltc_qty, ltc_last_update=ltc_last_update,
        eth_acct= eth_acct, eth_symbol=eth_symbol,  eth_qty=eth_qty, eth_last_update=eth_last_update,
        usd_acct= usd_acct, usd_symbol=usd_symbol,  usd_qty=usd_qty, usd_last_update=usd_last_update)

#for future use
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
     #initialize balance as 0
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
     fund_cash_account(customer_id,usd_currency_id,1000000) 

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

def get_cust_cash_acct():

        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT customer_id, account_id FROM customer_cash_accounts")
        cash_acct_dict={}
        for row in cursor:
                key=row[0]
                value=row[1]
                cash_acct_dict.update({key:value})
        return cash_acct_dict

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

def make_trade(customer_id, account_id, currency_short_name, currency_id, quantity, side):
        #update the transaction table and the account table
 
        #coinbase price
        price = get_price(currency_short_name, side)

        trade_value = float(quantity)*float(price)
        trans_sql = "INSERT INTO acct_transaction (account_id, currency_id, side, quantity, price) VALUES (%s, %s, %s,%s,%s)"
        trans_val = (account_id, currency_id, side, float(quantity), float(price))
        
        #update the transaction table
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(trans_sql, trans_val)
        connection.commit()
        cursor.close()

        #now to get the correct USD cash account id for the same customer
        #the function returns a dictionary with account list from db
        #we pass in the customer id to lookup the account number for USD cash account
        cust_cash_acct=get_cust_cash_acct()
        cash_account_id = cust_cash_acct[int(customer_id)]
        print("cash account id is", cash_account_id)

        #these are the parameters for updating the account table balance
        acct_val = (float(quantity), account_id, currency_id) #currency they are buying or selling
        acct_val_cash = (float(trade_value), cash_account_id, usd_currency_id) #us dollars
         
        #dynamically construct sql statements based on whether customer is buying or selling
        if side=='buy':
                #increase quantity of crypto in inventory
                acct_sql = ("UPDATE cust_account set quantity=quantity+%s where account_id=%s and currency_id =%s")
                #decrease quantity of us dollars
                acct_sql_cash = ("UPDATE cust_account set quantity=quantity-%s where account_id=%s and currency_id =%s")
        elif side=='sell':
                #decrease quantity of crypto in inventory
                acct_sql = ("UPDATE cust_account set quantity=quantity-%s where account_id=%s and currency_id =%s")
                #increase quantity of us dollars
                acct_sql_cash = ("UPDATE cust_account set quantity=quantity+%s where account_id=%s and currency_id =%s")

        #now update the relevant crypto and cash accounts
        
        cursor = connection.cursor()
        #update the account for the currency being bought or sold
        cursor.execute(acct_sql, acct_val)
        #update the corresponding cash account for the customers
        cursor.execute(acct_sql_cash, acct_val_cash )
       
        connection.commit()
        connection.close()


def get_account_balance(customer_id, currency_id):
        #find out how much user has in each account
        sql = ("Select account_id, currency_symbol, quantity, last_update from customer_balance where customer_id=%s and currency_id=%s")
        val = (customer_id,currency_id)
        print(sql,val)
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(sql,val)
       

        record = cursor.fetchone()
        account_id=record[0]
        currency_symbol=record[1]
        quantity=record[2]
        last_update=record[3]

        cursor.close()
        connection.close()

        return account_id, currency_symbol, quantity, last_update


def fund_cash_account(customer_id, usd_currency_id, deposit_amount):
        acct_sql = ("UPDATE cust_account set quantity=quantity+%s where currency_id =%s"
         " and account_id in (select account_id from cust_acct_assoc where customer_id =%s)")
        acct_val = (deposit_amount, usd_currency_id, customer_id)

        print(acct_sql, acct_val)
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(acct_sql, acct_val)
        cursor.close()
        connection.commit()
        connection.close()


