def display_menu(menu):
    print("Crypto Menu")
    for n in range(0,len(menu)):
        print(n+1,':',menu[n])
    itemNo = int(input("Enter item number: "))
    if itemNo == len(menu) + 1:
        return -1
    return itemNo


shopping_cart = []
is_still_shopping = True
menu = ('BTC','ETH','LTC',)

while is_still_shopping:
    menu_chosen = display_menu(menu)
    if menu_chosen == -1:
        is_still_shopping = False
    else:
        shopping_cart.append(menu[menu_chosen-1])

    
print("you ordered:", shopping_cart)