import os
import json

def show_instructions():
    print("Welcome to the Adventure Game!")
    print("Navigate through the rooms and find the treasure.")
    print("Commands: go [direction], get [item], help, map, save, load")

def show_status(current_room, inventory, rooms):
    print("---------------------------")
    print(f"You are in the {current_room}")
    print(f"Inventory: {inventory}")
    if "item" in rooms[current_room]:
        print(f"You see a {rooms[current_room]['item']}")
    print(f"Description: {rooms[current_room]['description']}")
    print("---------------------------")

def show_map():
    print("Map:")
    print("Hall - Kitchen")
    print("  |")
    print("Dining Room - Garden")


def save_game(current_room, inventory):
    # Create the saves directory if it doesn't exist
    if not os.path.exists('../saves'):
        os.makedirs('../saves')

    game_state = {
        'current_room': current_room,
        'inventory': inventory
    }
    with open('../saves/house_escape_save.json', 'w') as save_file:
        json.dump(game_state, save_file)
    print("Game saved!")


def load_game():
    try:
        with open('../saves/house_escape_save.json', 'r') as save_file:
            game_state = json.load(save_file)
        print("Game loaded!")
        return game_state['current_room'], game_state['inventory']
    except FileNotFoundError:
        print("No saved game found.")
        return 'Hall', []

def start_house_escape():
    print("Starting House Escape...\n")

    # Define the rooms and items
    rooms = {
        'Hall': {'south': 'Kitchen', 'east': 'Dining Room', 'item': 'key', 'description': 'A grand hall with a chandelier.'},
        'Kitchen': {'north': 'Hall', 'item': 'monster', 'description': 'A kitchen with a lingering smell of food.'},
        'Dining Room': {'west': 'Hall', 'south': 'Garden', 'item': 'potion', 'description': 'A dining room with a large table.'},
        'Garden': {'north': 'Dining Room', 'description': 'A beautiful garden with blooming flowers.'}
    }

    # Start the player in the Hall
    current_room, inventory = load_game()

    show_instructions()

    # Main game loop
    while True:
        show_status(current_room, inventory, rooms)

        # Get the player's next move
        move = input("> ").lower().split()

        if len(move) < 1:
            print("Invalid command! Type 'help' to see the list of commands.")
            continue

        if move[0] == 'go':
            if len(move) < 2:
                print("Go where? Specify a direction.")
                continue
            if move[1] in rooms[current_room]:
                current_room = rooms[current_room][move[1]]
            else:
                print("You can't go that way!")

        elif move[0] == 'get':
            if len(move) < 2:
                print("Get what? Specify an item.")
                continue
            if 'item' in rooms[current_room] and move[1] == rooms[current_room]['item']:
                inventory.append(move[1])
                print(f"{move[1]} got!")
                del rooms[current_room]['item']
            else:
                print(f"Can't get {move[1]}!")

        elif move[0] == 'help':
            show_instructions()

        elif move[0] == 'map':
            show_map()

        elif move[0] == 'save':
            save_game(current_room, inventory)

        elif move[0] == 'load':
            current_room, inventory = load_game()

        else:
            print("Invalid command! Type 'help' to see the list of commands.")

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
