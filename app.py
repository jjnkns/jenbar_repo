from flask import Flask
from flask import request
import mysql.connector as mc
import cbpro


app = Flask(__name__)

@app.route('/')
def monkey():
    return "Hithere"


public_client = cbpro.PublicClient()
mydict = public_client.get_currencies()


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
        #print(query, args)
        #+','+vmydict[n]['name'])
        print('------------------------------')
        


def get_connection():
    #returns a connection object
    connection = mc.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
    auth_plugin='mysql_native_password')
    return connection

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


# get_currency_detail('BTC')
# get_currency_detail('LTC')
# get_currency_detail('ETH')
    #mydb.close()

# get_currency_list()
    
#     #sql = 'select * from currency where currency_short_'
#     #connection.cmd_query(sql)
#     #mycursor = connection.cursor()
    
#     args = 'ETH'
    #mycursor.execute(query)
    #connection.commit()

    #print(query, args)
    #mycursor.execute(query, args)
    #print(query, args)
    #sql = query + args
    #result_set = mycursor.fetchall()
    #result_set = connection.cmd_query(sql)
    #result_set_and_meta = mycursor._affected_rows
    #print(result_set)
    # result_set = result_set_and_meta[0]
    
    
#load_currency_list()
# get_currency_menu('ETH')
    
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

# #     <html>
# #     <head>
# #         <title>Favorite Game</title>
# #     </head>
# #     <body>
# #         <form action="/submitgame" method="get">
# #             Enter your name: <input type="text" name="username">
# #             Enter your fav game: <input type="text" name="favgame">
# #             <input type="submit">
# #         </form>
# #     </body>
# # </html> 
    

@app.route('/buy')
def route_buy():
    
    currency = request.args.get('What do you want to buy?')
    return 'You want to buy' + str(currency).upper()

@app.route('/sell')
def route_sell():
    currency = request.args.get('What do you want to sell?')
    return 'You want to sell' + str(currency).upper()

