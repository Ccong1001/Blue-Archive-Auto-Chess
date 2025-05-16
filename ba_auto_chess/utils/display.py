"""
Display utilities for the game
"""

def display_units_list(units):
    '''
    Displays a list of units with formatted attributes.
    
    Parameters:
        units (list): Units to be displayed.
    '''
    print(f"{'Idx':<4} {'Name':<12} {'Gold':<5} {'HP':<5} {'ATK':<5} {'Skill':<15} {'School'}")
    print("-" * 60)
    for i, u in enumerate(units):
        print(f"{i:<4} {u.element + u.name:<12} {u.cost:<5} {u.max_hp:<5} {u.atk:<5} {u.skill:<15} {u.school}")
    print()

def game_round(p1, p2, shop):
    '''
    Manages a complete game round including shopping and battle phases.
    
    Handles the income calculation, unit shopping for both the human player
    and AI opponent, and displays relevant information about units and synergies.
    
    Parameters:
        p1 (Player): The human player.
        p2 (Player): The AI player.
        shop (Shop): The shop providing units for purchase.
        
    Returns:
        None
    '''
    # Human Player Phase
    print(f"===== {p1.name}'s Shopping =====")
    p1.income()
    choices = shop.get_choices()
    display_units_list(choices)
    
    # Player buying phase
    while p1.gold > 0:
        buy_input = input(f"Input the numbers you want to buy (space-separated, or Enter to skip): ").strip()
        if not buy_input:
            break
            
        buy_indices = []
        try:
            buy_indices = [int(x) for x in buy_input.split()]
        except ValueError:
            print("Invalid input. Please enter numbers separated by spaces.")
            continue
            
        for idx in buy_indices:
            if 0 <= idx < len(choices):
                if p1.gold >= choices[idx].cost:
                    p1.buy_unit(choices[idx])
                else:
                    print(f"Not enough gold for {choices[idx].element}{choices[idx].name}.")
            else:
                print(f"Invalid index: {idx}")
    
    print(f"\n== {p1.name}'s Final Units After Shopping ==")
    p1.show_units()
    print("Active synergies:", ", ".join(p1.get_synergy()))
    print()

    # AI Player Phase
    print(f"===== {p2.name}'s Turn (AI) =====")
    p2.income()
    for u in shop.get_choices():
        if len(p2.reserve) < 20 and p2.gold >= u.cost:
            p2.buy_unit(u)

    print(f"\n== {p2.name}'s Final Units After Shopping ==")
    p2.show_units()
    print("Active synergies:", ", ".join(p2.get_synergy()))
    print()