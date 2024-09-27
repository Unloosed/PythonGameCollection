def show_instructions():
    print("Welcome to the Adventure Game!")
    print("Navigate through the rooms and find the treasure.")
    print("Commands: go [direction], get [item]")

def show_status(current_room, inventory, rooms):
    print("---------------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")
    print("---------------------------")

def start_house_escape():
    print("Starting House Escape...\n")

    # Define the rooms and items
    rooms = {
        'Hall': {'south': 'Kitchen', 'east': 'Dining Room', 'item': 'key'},
        'Kitchen': {'north': 'Hall', 'item': 'monster'},
        'Dining Room': {'west': 'Hall', 'south': 'Garden', 'item': 'potion'},
        'Garden': {'north': 'Dining Room'}
    }

    # Start the player in the Hall
    current_room = 'Hall'
    inventory = []

    show_instructions()

    # Main game loop
    while True:
        show_status(current_room, inventory, rooms)

        # Get the player's next move
        move = input("> ").lower().split()

        if move[0] == 'go':
            if move[1] in rooms[current_room]:
                current_room = rooms[current_room][move[1]]
            else:
                print("You can't go that way!")

        elif move[0] == 'get':
            if 'item' in rooms[current_room] and move[1] == rooms[current_room]['item']:
                inventory.append(move[1])
                print(f"{move[1]} got!")
                del rooms[current_room]['item']
            else:
                print(f"Can't get {move[1]}!")

        # Check if the player encounters the monster
        if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
            print("A monster has got you... GAME OVER!")
            break

        # Check if the player wins by reaching the Garden with the key
        if current_room == 'Garden' and 'key' in inventory:
            print("You escaped the house with the key... YOU WIN!")
            break

if __name__ == "__main__":
    start_house_escape()