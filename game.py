import random

player_inventory = {}

all_items = [
    "sword", "monkey", "potion", "apple", "shield", "bow and arrow"
]

def select_item():
    choices = random.sample(all_items, 3)

    print("Make a selection from the following items:")
    for index, item in enumerate(choices, start=1):
        print(f"[{index}] {item}")

    selection = int(input("Selection: "))

    if selection < 1 or selection > len(choices):
        print("Invalid selection. Giving you the first item.")
        return choices[0]

    return choices[selection - 1]

def view_inventory():
    print("---Player Inventory---")

    if not player_inventory:
        print("Inventory is empty.")
        return

    for index, (item, count) in enumerate(player_inventory.items(), start=1):
        print(f"[{index}] {item} x {count}")

def add_item(item):
    if item in player_inventory:
        player_inventory[item] += 1
    else:
        player_inventory[item] = 1

    print(f"{item} added to inventory.")

def remove_item():
    if not player_inventory:
        print("Inventory is empty.")
        return

    print("---Remove Item---")

    items = list(player_inventory.keys())

    for index, item in enumerate(items, start=1):
        print(f"[{index}] {item} x {player_inventory[item]}")

    selection = int(input("What would you like to remove? "))

    if selection < 1 or selection > len(items):
        print("Invalid selection.")
        return

    selected_item = items[selection - 1]

    quantity = int(input(f"How many {selected_item}s would you like to remove? "))

    if quantity <= 0:
        print("Quantity must be greater than 0.")
        return

    if quantity > player_inventory[selected_item]:
        print("You do not have that many.")
        return

    player_inventory[selected_item] -= quantity

    if player_inventory[selected_item] == 0:
        del player_inventory[selected_item]

    print(f"Removed {quantity} {selected_item}(s).")

while True:
    print(
        "---Main Menu---\n"
        "View Inventory = V\n"
        "Add Item = A\n"
        "Remove Item = R\n"
        "Quit = Q\n"
    )

    main_menu_selection = input("Selection: ").upper()

    if main_menu_selection == "V":
        view_inventory()

    elif main_menu_selection == "A":
        item = select_item()
        add_item(item)

    elif main_menu_selection == "R":
        remove_item()

    elif main_menu_selection == "Q":
        break

    else:
        print("Invalid selection.")