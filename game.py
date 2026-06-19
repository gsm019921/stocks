import random

player_inventory = []
all_items = [
    "sword", "monkey", "potion", "apple", "shield", "bow and arrow"
]

while True:
    main_menu = input ("Main Menu\n View Inventory=V\n " \
"Add Item=A\n Remove Item=R\n Quit=Q\n")
    if main_menu == "V":
        if not player_inventory:  
            print("Inventory is empty.")
        else: 
            for item in player_inventory:
                print(item)

    elif main_menu == "A":
        item_one = all_items[int(random.randint(0,5))]
        item_two = all_items[int(random.randint(0,5))]
        item_three = all_items[int(random.randint(0,5))]
        
        selection = int(input(f"Make a selection from the following items:\n"
                              f"[1]: {item_one}\n"
                              f"[2]: {item_two}\n"
                              f"[3]: {item_three}\n"))
        
        if selection == 1: 
            player_inventory.append(item_one)
        elif selection == 2:
            player_inventory.append(item_two)
        else:
            player_inventory.append(item_three)

        for item in player_inventory:
            print(item)
        
    elif main_menu == "R":
        print("removing item")

    elif main_menu == "Q":
        break