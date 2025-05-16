"""
Battle system implementation
"""

import time

def battle(p1, p2):
    '''
    Simulates a battle between two players' deployed units.
    
    Handles the combat sequence where units from both sides attack
    each other and use their skills until one team is defeated.
    
    Parameters:
        p1 (Player): The first player.
        p2 (Player): The second player.
        
    Returns:
        None
    '''
    input("Press Enter to start battle...")
    print("\n========== BATTLE START ==========")
    p1.deploy_units()
    p2.deploy_units()

    # Display both lineups
    print(f"\n {p1.name}'s lineup:")
    for i, u in enumerate(p1.units):
        print(f"  [{i+1}] {u.element}{u.name}★{u.star} - {u.get_health_bar()}, ATK: {u.atk}, Skill: {u.skill}, School: {u.school}")
    
    print(f"\n {p2.name}'s lineup:")
    for i, u in enumerate(p2.units):
        print(f"  [{i+1}] {u.element}{u.name}★{u.star} - {u.get_health_bar()}, ATK: {u.atk}, Skill: {u.skill}, School: {u.school}")

    team1 = p1.units.copy()
    team2 = p2.units.copy()
    round_num = 1

    while any(u.is_alive() for u in team1) and any(u.is_alive() for u in team2):
        print(f"\n === Round {round_num} === ")
        
        # Display survival status
        alive1 = sum(1 for u in team1 if u.is_alive())
        alive2 = sum(1 for u in team2 if u.is_alive())
        print(f"Survival status: {p1.name}: {alive1}/{len(team1)} vs {p2.name}: {alive2}/{len(team2)}")

        if round_num % 2 == 1:
            # Team1 turn first
            # Team1 turn
            print(f"\n {p1.name}'s turn:")
            for u in team1:
                if u.is_alive():
                    enemies = [e for e in team2 if e.is_alive()]
                    if enemies:
                        print(f"  👉 {u.element}{u.name}★{u.star} acting...")
                        u.attack(enemies=enemies, allies=team1, owner_name=p1.name)
                        time.sleep(0.2)  # Brief pause to enhance battle pacing

            # Team2 turn
            print(f"\n {p2.name}'s turn:")
            for u in team2:
                if u.is_alive():
                    enemies = [e for e in team1 if e.is_alive()]
                    if enemies:
                        print(f"  👉 {u.element}{u.name}★{u.star} acting...")
                        u.attack(enemies=enemies, allies=team2, owner_name=p2.name)
                        time.sleep(0.2)  # Brief pause to enhance battle pacing
        
        else:
            # Team2 turn first
            # Team2 turn
            print(f"\n {p2.name}'s turn:")
            for u in team2:
                if u.is_alive():
                    enemies = [e for e in team1 if e.is_alive()]
                    if enemies:
                        print(f"  👉 {u.element}{u.name}★{u.star} acting...")
                        u.attack(enemies=enemies, allies=team2, owner_name=p2.name)
                        time.sleep(0.2)  # Brief pause to enhance battle pacing
        
            # Team1 turn
            print(f"\n {p1.name}'s turn:")
            for u in team1:
                if u.is_alive():
                    enemies = [e for e in team2 if e.is_alive()]
                    if enemies:
                        print(f"  👉 {u.element}{u.name}★{u.star} acting...")
                        u.attack(enemies=enemies, allies=team1, owner_name=p1.name)
                        time.sleep(0.2)  # Brief pause to enhance battle pacing

        

        round_num += 1
        time.sleep(1)  # Pause between rounds

    # End battle, display results
    alive1 = sum(1 for u in team1 if u.is_alive())
    alive2 = sum(1 for u in team2 if u.is_alive())
    
    print("\n🏁 === BATTLE END === 🏁")
    if alive1 > alive2:
        print(f"\n🏆 {p1.name} wins! (Surviving units: {alive1})")
        p1.fail = 0
        p2.fail += 1
    elif alive2 > alive1:
        print(f"\n🏆 {p2.name} wins! (Surviving units: {alive2})")
        p2.fail = 0
        p1.fail += 1
    else:
        print("\n🤝 It's a tie!")
    
    # Display post-battle unit status
    print(f"\nPost-battle unit status:")
    print(f"\n {p1.name}'s units:")
    for i, u in enumerate(team1):
        status = "Alive" if u.is_alive() else "Defeated"
        print(f"  [{i+1}] {u.element}{u.name}★{u.star} - {u.get_health_bar()} - {status}")
    
    print(f"\n {p2.name}'s units:")
    for i, u in enumerate(team2):
        status = "Alive" if u.is_alive() else "Defeated"
        print(f"  [{i+1}] {u.element}{u.name}★{u.star} - {u.get_health_bar()} - {status}")
    
    input("Press Enter to continue...")