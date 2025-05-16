import random
import time
from collections import defaultdict

# === Element Damage Multiplier ===
ELEMENT_DAMAGE_MULTIPLIER = {
    "🔴": {"🔴": 2.0, "🟡": 1.0, "🔵": 0.5},
    "🟡": {"🔴": 0.5, "🟡": 2.0, "🔵": 1.0},
    "🔵": {"🔴": 1.0, "🟡": 0.5, "🔵": 2.0},
}


MAX_UNITS_ON_FIELD = 10


# Chess Class
class Unit:
    def __init__(self, name: str, cost: int, hp: int, atk: int, skill: str, school: str, element: str):
        self.name = name
        self.cost = cost
        self.max_hp = hp
        self.hp = hp
        self.base_atk = atk
        self.atk = atk
        self.skill = skill
        self.star = 1
        self.school = school
        self.element = element

    def key(self):
        return f"{self.name}_★{self.star}"

    def is_alive(self):
        return self.hp > 0
    
    def get_health_bar(self, bar_length=10):
        ratio = self.hp / self.max_hp
        filled_length = int(bar_length * ratio)
        bar = '█' * filled_length + ' ' * (bar_length - filled_length)
        return f"HP: [{bar}] {self.hp}/{self.max_hp}"

    def upgrade(self):
        self.star += 1
        self.max_hp = int(self.max_hp * 1.8)
        self.base_atk = int(self.base_atk * 1.5)
        self.atk = self.base_atk
        self.hp = self.max_hp
        print(f"{self.name} goes up to {self.star} STR!")

    def cast_skill(self, enemies, allies):
        if self.skill == "AOE" and enemies:
            print(f"{self.name} cast AOE, make {self.atk//2} attack to all enemies.")
            for e in enemies:
                e.hp -= self.atk // 2

        if self.skill == "shield":
            print(f"{self.name} cast shield, get {self.atk//2} shield.")
            self.hp += self.atk // 2
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            
        if self.skill == "heal":
            print(f"{self.name} casts heal-all, teammates recover {self.atk // 3} HP.")
            for ally in allies:
                if ally.is_alive():
                    ally.hp += self.atk // 3
                    if ally.hp > ally.max_hp:
                        ally.hp = ally.max_hp


    def attack(self, target):
        multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][target.element]
        damage =  int(self.atk * multiplier)
        target.hp -= damage
        target.hp = max(0, target.hp)
        print(f"{self.name} attack {target.name} make {damage} point damage (HP {target.hp}).")


# === Shop Class ===
class Shop:
    def __init__(self, pool):
        self.pool = pool

    def get_choices(self, level):
        return [Unit(u.name, u.cost, u.max_hp, u.atk, u.skill, u.school, u.element) for u in random.sample(self.pool, min(5, len(self.pool)))]

# === Player Class ===
class Player:
    def __init__(self, name):
        self.name = name
        self.gold = 10
        self.level = 1
        self.units = []
        self.reserve = []
        self.unit_counter = defaultdict(int)

    def income(self):
        base_income = 5
        interest = self.gold // 10
        self.gold += base_income + interest
        print(f"{self.name} get income: base {base_income} + interest {interest} = {base_income+interest} gold.")

    def buy_unit(self, unit: Unit):
        if self.gold >= unit.cost:
            self.gold -= unit.cost
            new_unit = Unit(unit.name, unit.cost, unit.max_hp, unit.atk, unit.skill, unit.school, unit.element)
            self.reserve.append(new_unit)
            print(f"{self.name} bought {new_unit.name}")
            self.try_merge()
        else:
            print(f"{self.name} hasn't enough gold, can't buy {unit.name}")

    def try_merge(self):
        counter = defaultdict(list)
        for u in self.reserve:
            counter[u.name].append(u)

        for name, units_list in counter.items():
            while len(units_list) >= 3:
                to_merge = units_list[:3]
                for u in to_merge:
                    self.reserve.remove(u)
                    units_list.remove(u)
                base = to_merge[0]
                new_unit = Unit(base.name, base.cost, base.max_hp, base.atk, base.skill, base.school, base.element)
                new_unit.star = base.star
                new_unit.upgrade()
                self.reserve.append(new_unit)
                print(f"{self.name} successfully merged {name} to ★{new_unit.star}")
                units_list.append(new_unit)

    def deploy_units(self):
        self.units = self.reserve[:MAX_UNITS_ON_FIELD]  # simply take first 10 units
        for u in self.units: 
            u.hp = u.max_hp

    def show_units(self):
        for i, u in enumerate(self.reserve):
            print(f"[{i}] {u.name}★{u.star} - HP: {u.get_health_bar()}, ATK: {u.atk}, skill: {u.skill}, synergy: {u.school}")

    def get_synergy(self):
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1
        bonuses = []
        for r, c in school_count.items():
            if c >= 2: bonuses.append(f"{r} synergy(+1 ATK)")
        return bonuses
    
    def apply_synergy_bonus(self):
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1
        for u in self.units:
            u.atk = u.base_atk
            if school_count[u.school] >= 2:
                u.atk += 1


# === Battle ===
def battle(p1: Player, p2: Player):
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

# === One Round Process ===
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


# === Unit Pool ===
unit_pool = [
    Unit("Momoi", 3, 6, 2, "AOE", "Millennium", "🟡"),
    Unit("Midori", 3, 6, 5, "/", "Millennium", "🟡"),
    Unit("Yuuka", 3, 15, 3, "shield", "Millennium", "🔴"),
    Unit("Alice", 3, 5, 6, "/", "Millennium", "🔵"),
    Unit("Asuna", 2, 8, 4, "/", "Millennium", "🔵"),
    Unit("Hoshino", 4, 14, 4, "shield", "Abydos", "🟡"),
    Unit("Shiroko", 2, 8, 4, "/", "Abydos", "🔴"),
    Unit("Mika", 6, 10, 8, "/", "Trinity", "🟡"),
    Unit("Koharu", 3, 6, 3, "heal", "Trinity", "🔴"),
    Unit("Natsu", 4, 12, 5, "shield", "Trinity", "🔵"),
    Unit("Hina", 5, 8, 9, "/", "Gehenna", "🔴"),
    Unit("Mutsuki", 4, 6, 3, "AOE", "Gehenna", "🔴"),
    Unit("Iroha", 10, 6, 6, "AOE", "Gehenna", "🔵"),
]



# === Game Main ===
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
