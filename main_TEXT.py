from games import house_escape, snake

def main_menu():
    games = {
        "House Escape": house_escape.start_house_escape,
        "Snake": snake.start_snake
    }

    while True:
        print("Welcome to the Game Menu!")
        for i, game in enumerate(games, start=1):
            print(f"{i}. {game}")
        print(f"{len(games) + 1}. Quit")

        choice = input("Enter your choice: ")

        if choice.isdigit() and 1 <= int(choice) <= len(games):
            index = int(choice) - 1
            game_name = list(games.keys())[index]
            games[game_name]()
        elif choice == str(len(games) + 1):
            print("Exiting the game. Goodbye!")
            break
        else:
            print("Invalid choice. Please select again.")

if __name__ == "__main__":
    main_menu()
