import os
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
import importlib

def start_game(game_func) -> None:
    """Execute a reference to a function"""
    game_func()

def is_valid_game_file(filename) -> bool:
    """Check if the file is a valid game file."""
    return filename.endswith('.py') and filename != '__init__.py'

def import_game_module(games_dir, filename):
    """Import the game module."""
    module_name = f"{games_dir}.{filename[:-3]}"
    return importlib.import_module(module_name)

def get_start_function(module, filename):
    """Get the start function from the module."""
    start_func_name = f"start_{filename[:-3]}"
    if hasattr(module, start_func_name):
        return getattr(module, start_func_name)
    return None

def get_games():
    """
    Scan the 'games' directory for Python files, import them, and check for a start function.

    Returns:
        dict: A dictionary where the keys are the game names (formatted nicely) and the values are the corresponding start functions.
    """
    games = {}
    games_dir = 'games'
    for filename in os.listdir(games_dir):
        if is_valid_game_file(filename):
            module = import_game_module(games_dir, filename)
            start_func = get_start_function(module, filename)
            if start_func:
                titled_game_name = filename[:-3].replace('_', ' ').title()
                games[titled_game_name] = start_func
    return games

def main_menu():
    """
    Create the main menu GUI for launching games.

    This function initializes the main window, loads the available games, and creates buttons for each game.
    """
    games = get_games()

    root = tk.Tk()
    root.title("Game Menu")
    root.geometry("400x400")
    root.configure(bg="#282c34")

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TButton', font=('Helvetica', 12), padding=10)
    style.configure('TLabel', font=('Helvetica', 16), background="#282c34", foreground="#ffffff")

    ttk.Label(root, text="Welcome to the Game Menu!").pack(pady=10)

    for game_name, game_func in games.items():
        ttk.Button(root, text=game_name, command=lambda func=game_func: start_game(func), width=20).pack(pady=5)

    ttk.Button(root, text="Quit", command=root.quit, width=20).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
