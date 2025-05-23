"""
Main entry point for the Blue Archive Auto Chess game
"""

import time
from models.shop import Shop
from models.player import Player
from core.tutorial import show_tutorial
from core.battle import battle
from core.display import game_round

def main():
    '''
    The main game loop that initializes the game and runs multiple rounds.
    
    Sets up the game environment with players and shop, then runs a fixed
    number of game rounds before ending the game.
    
    Returns:
        None
    '''
    print("\n=== Welcome to Blue Archive Auto Chess Game! ===")

    # Prompt for tutorial
    show_help = input("Would you like to see the game tutorial? (y/n): ").lower().strip()

    if show_help == 'y' or show_help == 'yes':
        # Choose language
        language_choice = input("Choose language / 选择语言 (en/zh): ").lower().strip()
        language = "en" if language_choice != "zh" else "zh"
    
    
        show_tutorial(language)
    
    # Create shop instance
    shop = Shop()
    
    # Get player name
    player_name = input("Enter your name: ")

    print(f"\nWelcome, {player_name}!")
    
    player1 = Player(player_name)
    player2 = Player("🤖 AI")

    # Main game loop
    for round_id in range(1, 6):
        print(f"\n\n🌟🌟 Round {round_id} 🌟🌟")
        game_round(player1, player2, shop)
        battle(player1, player2)
        if player1.win == 3 or player2.win == 3:
            break

    # Game end and results
    print("\n🎮 Game Over! Thanks for Playing!")

    print(f"\n{player1.name} won {player1.win} rounds, {player2.name} won {player2.win} rounds.")
    if player1.win > player2.win:
        print(f"Congratulations {player1.name}, you are the champion!")
    elif player1.win < player2.win:
        print(f"Better luck next time, {player1.name}!")
    else:
        print("It's a draw!") 

if __name__ == "__main__":
    main()