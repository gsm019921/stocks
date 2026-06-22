import random

player_inventory = []

all_items = [
    "sword", "monkey", "potion", "apple", "shield", "bow and arrow"
]

def main_menu():
    while True:
        print("\n---Main Menu---\nView Inventory = V\n" \
            "Add Item = A\nRemove Item = R\nQuit = Q\n")
        main_menu_selection = input("Selection: ")
        
        if main_menu_selection == "V":
            view_inventory()

        elif main_menu_selection == "A":
            item = select_item()
            player_inventory.append(item)
        
            print(f"{item} added to inventory")
            
        elif main_menu_selection == "R":
            remove_item()

        elif main_menu_selection == "Q":
            break

def select_item():
        item_one = all_items[int(random.randint(0,5))]
        item_two = all_items[int(random.randint(0,5))]
        item_three = all_items[int(random.randint(0,5))]
        
        selection = int(input(f"\nMake a selection from the following items:\n"
                              f"[1] {item_one}\n"
                              f"[2] {item_two}\n"
                              f"[3] {item_three}\n"
                              "\nSelection: "))
        
        if selection == 1: 
            return item_one
        elif selection == 2:
            return item_two
        else:
            return item_three
        
def view_inventory():
    print("\n---Player Inventory---")
    if not player_inventory:  
        print("Inventory is empty.")
        return
    counting_inventory = {}
    for item in player_inventory:
        if item in counting_inventory: 
            counting_inventory[item] += 1
        else: 
            counting_inventory[item] = 1
    for item, count in counting_inventory.items():
        print(f"{item} x{count}")

def remove_item():
    numbers = 0
    counting_inventory = {}
    for item in player_inventory:
        if item in counting_inventory: 
            counting_inventory[item] += 1
        else: 
            counting_inventory[item] = 1
    remove_menu = []
    for item in counting_inventory:
        remove_menu.append(item)
    for item in remove_menu:
        numbers += 1
        print(f"\n[{numbers}] {item} x{counting_inventory[item]}")
    removal_option = int(input("\nSelect an item to remove:\n"))
    index = removal_option - 1
    item_to_remove = remove_menu[index]
    player_inventory.remove(item_to_remove)
    print(f"You have removed 1 {item_to_remove}.")

main_menu()