# battle.py
import random
import time

def battle(p1, p2):
    print("\n=== Auto Battle Start ===")
    p1.deploy_units()
    p2.deploy_units()

    p1.apply_synergy_bonus()
    p2.apply_synergy_bonus()

    team1 = p1.units.copy()
    team2 = p2.units.copy()
    round_num = 1

    while any(u.is_alive() for u in team1) and any(u.is_alive() for u in team2):
        print(f"\n--- Battle {round_num} ---")
        for u in team1:
            if u.is_alive():
                enemies = [e for e in team2 if e.is_alive()]
                if enemies:
                    u.cast_skill(enemies=enemies, allies=team1)
                    u.attack(random.choice(enemies))

        for u in team2:
            if u.is_alive():
                enemies = [e for e in team1 if e.is_alive()]
                if enemies:
                    u.cast_skill(enemies=enemies, allies=team2)
                    u.attack(random.choice(enemies))

        round_num += 1
        time.sleep(1)

    alive1 = sum(1 for u in team1 if u.is_alive())
    alive2 = sum(1 for u in team2 if u.is_alive())
    if alive1 > alive2:
        print(f"\n🏆 {p1.name} Win!")
    elif alive2 > alive1:
        print(f"\n🏆 {p2.name} Win!")
    else:
        print("\n🤝 Equal!")
