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
response=requests.get('https://api.coinbase.com/v2/prices/BTC-USD/spot')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Spot Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Spot Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/LTC-USD/spot')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Spot Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/BTC-USD/buy')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Buy Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/ETH-USD/buy')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Buy Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/LTC-USD/buy')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Buy Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/BTC-USD/sell')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Sell Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/ETH-USD/sell')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Sell Price:", price)

response=requests.get('https://api.coinbase.com/v2/prices/LTC-USD/sell')
data = response.json()
currency = data["data"]["base"]
price = data["data"]["amount"]
print("Currency:", currency, "Sell Price:", price)

# from coinbase.wallet.client import Client

# #client = Client()

# client = Client(api_key, api_secret, api_version='YYYY-MM-DD')

# currency_code = 'USD'  # can also use EUR, CAD, etc.

# Make the request
#price = client.get_spot_price(currency=currency_code)

#print('Current bitcoin price in %s: %s' % (currency_code, price.amount))

# from coinbase.wallet.client import Client
# #client = Client(<api_key>, <api_secret>)

# price = client.get_buy_price(currency_pair = 'BTC-USD')


#wsClient.products()
#print(public_client.get_products())


#PublicClient Methods
#get_products
# public_client.get_products()
# public_client.get_product_order_book('ETH-USD')
# # Get the order book at the default level.
# public_client.get_product_order_book('BTC-USD')
# # Get the order book at a specific level.
# public_client.get_product_order_book('BTC-USD', level=1)
# public_client.get_product_ticker('BTC-USD',)
# # Get the product ticker for a specific product.
# public_client.get_product_ticker(product_id='ETH-USD')
# #get_product_trades (paginated)
# # Get the product trades for a specific product.
# # Returns a generator
# public_client.get_product_trades(product_id='ETH-USD'
# #get_product_historic_rates
# public_client.get_product_historic_rates('ETH-USD')
# # To include other parameters, see function docstring:
# public_client.get_product_historic_rates('ETH-USD', granularity=3000)
#get_product_24hr_stats
# public_client.get_product_24hr_stats('ETH-USD')
#get_currencies
#print(public_client.get_currencies())

#get_time
#print(public_client.get_time())
