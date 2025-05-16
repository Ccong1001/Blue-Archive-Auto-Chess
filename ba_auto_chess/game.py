# game.py
from shop import Shop
from player import Player
from battle import battle
from unit_pool import unit_pool

def game_round(p1, p2, shop):
    print(f"\n===== {p1.name}'s Shopping =====")
    p1.income()
    print(f"{p1.name} has {p1.gold} gold.")
    choices = shop.get_choices(p1.level)
    for i, u in enumerate(choices):
        print(f"{i}: {u.name}(gold:{u.cost}, HP:{u.max_hp}, ATK:{u.atk}, Skill:{u.skill}, school: {u.school}）")

    buy = input("Input the number you want to buy(space to separate or Enter to skip):").strip()

    if buy:
        try:
            indices = list(map(int, buy.split()))
            for idx in indices:
                if 0 <= idx < len(choices):
                    p1.buy_unit(choices[idx])
                else:
                    print(f"Index {idx} is out of range.")
        except ValueError:
            print("Invalid input! Please enter numbers separated by spaces.")
    
    print(f"{p1.name} recent units")
    p1.show_units()
    print("Recent synergy:", ", ".join(p1.get_synergy()))

    # Player 2 AI
    p2.income()
    for u in shop.get_choices(p2.level):
        if len(p2.reserve) < 20 and p2.gold >= u.cost:
            p2.buy_unit(u)

def main():
    shop = Shop(unit_pool)
    player_name = input("Enter your name: ")
    player1 = Player(player_name)
    player2 = Player("AI")

    for round_id in range(1, 6):
        print(f"\n\n🌟🌟 Round {round_id} 🌟🌟")
        game_round(player1, player2, shop)
        battle(player1, player2)

    print("\n🎮 Game Over! Thanks for Playing!")

if __name__ == "__main__":
    main()
