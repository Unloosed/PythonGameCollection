import tkinter as tk
from games import house_escape, snake


def start_game(game_func):
    game_func()

def main_menu():
    games = {
        "House Escape": house_escape.start_house_escape,
        "Snake": snake.start_snake
    }

    root = tk.Tk()
    root.title("Game Menu")

    tk.Label(root, text="Welcome to the Game Menu!", font=("Helvetica", 16)).pack(pady=10)

    for game_name, game_func in games.items():
        tk.Button(root, text=game_name, command=lambda func=game_func: start_game(func), width=20).pack(pady=5)

    tk.Button(root, text="Quit", command=root.quit, width=20).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()