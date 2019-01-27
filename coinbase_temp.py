import cbpro
public_client = cbpro.PublicClient()
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
mydict = public_client.get_currencies()

for n in range(0,len(mydict)):
    print(mydict[n]['id'], mydict[n]['name'],mydict[n]['details']['symbol'])
    print('------------------------------')
#get_time
#print(public_client.get_time())
