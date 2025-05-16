# unit.py
import random

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

