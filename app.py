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


for n in range(0,len(mydict)):
    print(mydict[n]['id'], mydict[n]['name'],mydict[n]['details']['symbol'])
    currency_id = str(n)
    #currency_symbol = mdyict[n]['details']['symbol']
    #currency_short_name = mdyict[n]['id']
    #currency_long_name = mydict[n]['details']
   
    print('insert into currency(currency_id, currency_symbol, currency_short_name, currency_long_name) values('+currency_id+ ',' + mydict[n]['details']['symbol']+','+ mydict[n]['name'])
    #+','+vmydict[n]['name'])
    print('------------------------------')



def get_connection():
    #returns a connection object
    connection = mc.connect(user='root', password='ttcr^Yet1', host='127.0.0.1',database='jenbar',
    auth_plugin='mysql_native_password')
    return connection

def run_query(sql):
    connection = get_connection()
    result_set = connection.cmd_query(sql)
    result_set_and_meta = connection.get_rows()
    result_set = result_set_and_meta[0]
    connection.close()
    return result_set
    
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

