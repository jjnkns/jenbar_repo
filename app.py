from flask import Flask, render_template
from flask import request
import mysql.connector as mc
import cbpro


app = Flask(__name__)

@app.route('/')
def monkey():
        #main()
        #return "Hithere"
        return render_template('index.html')

@app.route('/buy')
def buy():
        #main()
        #return "Hithere"
        return render_template('buy.html')

@app.route('/sell')
def sell():
        #main()
        #return "Hithere"
        return render_template('sell.html', products=['ETH','LTC','BTC'])


public_client = cbpro.PublicClient()
mydict = public_client.get_currencies()

def main():
    return render_template('index.html')


def load_currency_list():
    for n in range(0,len(mydict)):
        #print(mydict[n]['id'], mydict[n]['name'],mydict[n]['details']['symbol'])
        # currency_id = str(n)
        # print('insert into currency(currency_id, currency_symbol, currency_long_name, currency_short_name) values('+currency_id+ ',\''  + 
        #     mydict[n]['details']['symbol']+'\',\''+ 
        #     mydict[n]['name']+'\',\''+
        #     mydict[n]['id']+ '\')')
                
        query ='insert into currency(currency_id, currency_symbol, currency_long_name, currency_short_name) values(%s,%s,%s,%s)'
        args = (n, mydict[n]['details']['symbol'], mydict[n]['name'], mydict[n]['id'])
        # values('+currency_id+ ',\''  + 
        #     mydict[n]['details']['symbol']+'\',\''+ 
        #     mydict[n]['name']+'\',\''+
        #     mydict[n]['id']+ '\')')

        run_query(query,args)
       
        #+','+vmydict[n]['name'])
        print('------------------------------')
        


def get_connection():
    #returns a connection object
    connection = mc.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
    auth_plugin='mysql_native_password')
    return connection

# def call_stored_proc(arg):
#     connection = get_connection()
#     cursor = connection .cursor()
#     cursor.callproc('GetCurrencySymbol',arg)
#     #records = cursor.fetchall()
#     #print("Total number of currencies is - ", cursor.rowcount)
#     #print(records)
#     #cursor.close()


def run_query(query,args):
    connection = get_connection()
    sql_select_Query = 'select * from currency where currency_short_name = %s (arg)'
    arg = 'BTC'
    cursor = connection .cursor()
    cursor.execute(sql_select_Query, arg)
    records = cursor.fetchall()
    print("Total number of currencies is - ", cursor.rowcount)
    print(records)
    cursor.close()

def get_currency_detail(currency_short_name):
    import mysql.connector
    mydb = mysql.connector.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
        auth_plugin='mysql_native_password')

    mycursor = mydb.cursor()

    sql = "SELECT currency_symbol, currency_short_name, currency_long_name FROM currency WHERE currency_short_name = %s"
    nam = (currency_short_name,)

    mycursor.execute(sql, nam)

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)

currency_list = ('BTC','LTC','ETH')

for n in range(0,len(currency_list)):
    get_currency_detail(currency_list[n])

# call_stored_proc('BTC')

    
# <html>
# <div class="container-fluid" id="feedback">
#     <p><h2>Give us your feedback on the cafe!</h2>
#         <h4><em>Maximum of 150 Characters.</em></h4>
#     </p>
#     <form action="{{ url_for('feedback') }}" method="post">
#         <div class="form-group">
#             <label class="sr-only" for="fb">Feedback</label>
#             <textarea class="form-control" id="fb" placeholder="Enter your Feedback here..." type="text" maxlength="150"></textarea>
#         </div>
#         <div class="form-group">
#             <label class="sr-only" for="rating">Rating for Cafe</label>
#             <select class="form-control" id="rating">
#                 <option>5</option>
#                 <option>4</option>
#                 <option selected>3</option>
#                 <option>2</option>
#                 <option>1</option>
#             </select>
#         </div>
#         <div class="form-group">
#             <input autocomplete="off" autofocus class="form-control" name="postal_code" placeholder="Postal Code of Cafe" type="text"/>
#         </div>
#         <div class="form-group">
#             <button class="btn btn-default" type="submit">Submit!</button>
#         </div>
#     </form>
# </div>
#     return  'Welcome'


    

# @app.route('/buy')
# def route_buy():
    
#     currency = request.args.get('What do you want to buy?')
#     return 'You want to buy' + str(currency).upper()

# @app.route('/sell')
# def route_sell():
#     currency = request.args.get('What do you want to sell?')
#     return 'You want to sell' + str(currency).upper()

