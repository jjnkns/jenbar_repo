food_menu = {
    11: {
        'description': 'BTC',
        'price': 1.99,
        'quantity_ordered': 0
    },
    222: {
        'description': 'ETH',
        'price': 1.50,
        'quantity_ordered': 0
    },
    333: {
        'description': 'LTC',
        'price': 1.25,
        'quantity_ordered': 0
    }
}

is_still_shopping = True
while is_still_shopping:
    for k,v in food_menu.items():
        print(k,"--",v['description'],'for','$' + str(v['price']))

    user_choice = int(input('which one do u want'))
    quantity = int(input('how much of it'))
    if user_choice > 3:
        is_still_shopping = False
    else:
        food_menu[user_choice]['quantity_ordered'] = food_menu[user_choice]['quantity_ordered'] + quantity

running_total = 0
for k,v in food_menu.items():
    qty = v['quantity_ordered']
    price = v['price']
    running_total = running_total + (qty * price)

print (running_total)
print (running_total * 1.08)

print(food_menu)






'''
DESCRIPTION = 0
PRICE = 1
print(food_menu[2])
print(food_menu[2][PRICE])
print(food_menu[2][DESCRIPTION])
for k in range(1,4):
    print(food_menu[k][DESCRIPTION])
