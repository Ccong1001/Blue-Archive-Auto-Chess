"""
Unit class definition
"""

import random
from core.constants import ELEMENT_DAMAGE_MULTIPLIER

class Unit:
    '''
    Represents a unit in the auto chess game with various attributes and abilities.
    
    The Unit class defines all the properties and behaviors of a game unit including
    its stats (health, attack), special abilities, and element type that affects combat.
    
    Parameters:
        name (str): The name of the unit.
        cost (int): The gold cost to purchase this unit from the shop.
        hp (int): The initial and maximum health points of the unit.
        atk (int): The base attack damage of the unit.
        skill (str): The special ability of the unit (e.g. "AOE-all", "heal").
        school (str): The faction/school the unit belongs to for synergy bonuses.
        element (str): The element type (🔴, 🟡, 🔵) affecting damage multipliers.
    '''

    def __init__(self, name, cost, hp, atk, skill, school, element):
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
        '''
        Generates a unique identifier string for the unit.
        
        Creates a string that combines the unit's name and star level to
        uniquely identify it in the game.
        
        Returns:
            str: A string in the format "{name}_★{star}".
        '''
        return f"{self.name}_★{self.star}"

    def is_alive(self):
        '''
        Checks if the unit is still alive.
        
        Determines whether the unit has health points remaining.
        
        Returns:
            bool: True if the unit's HP is greater than 0, False otherwise.
        '''
        return self.hp > 0
    
    def get_health_bar(self, bar_length=10):
        '''
        Creates a visual representation of the unit's current health.
        
        Generates a text-based health bar showing the current HP ratio.
        
        Parameters:
            bar_length (int): The total length of the health bar in characters.
            
        Returns:
            str: A string containing the health bar visualization and the current/maximum HP.
        '''
        ratio = self.hp / self.max_hp
        filled_length = int(bar_length * ratio)
        
        # Choose color based on health ratio
        if ratio > 0.7:  # Health > 70%, show green
            bar = '█' * filled_length + ' ' * (bar_length - filled_length)
            return f"HP: [{bar}] {self.hp}/{self.max_hp}"
        elif ratio > 0.3:  # Health 30%-70%, show yellow
            bar = '█' * filled_length + ' ' * (bar_length - filled_length)
            return f"HP: [{bar}] {self.hp}/{self.max_hp}"
        else:  # Health < 30%, show red
            bar = '█' * filled_length + ' ' * (bar_length - filled_length)
            return f"HP: [{bar}] {self.hp}/{self.max_hp}"

    def upgrade(self):
        '''
        Upgrades the unit to the next star level.
        
        Increases the unit's star level and enhances its stats (HP and attack)
        according to predefined multipliers.
        
        Returns:
            None
        '''
        self.star += 1
        self.max_hp = int(self.max_hp * 1.8)  # 80% HP increase
        self.hp = self.max_hp
        self.base_atk = int(self.base_atk * 1.5)  # 50% ATK increase
        self.atk = self.base_atk
    
    def attack(self, enemies, allies, owner_name):
        '''
        Performs an attack action based on the unit's skill.
        
        Executes different attack patterns depending on the unit's skill,
        targeting either one or multiple enemies.
        
        Parameters:
            enemies (list): List of enemy Unit objects.
            allies (list): List of allied Unit objects.
            owner_name (str): Name of the unit's owner for display purposes.
        
        Returns:
            None
        '''
        if not enemies:
            return
            
        # AOE-all skill: Attack all enemies
        if self.skill == "AOE-all" and enemies:
            print(f"{owner_name}'s [{self.element}{self.name}] cast AOE-all, make attack to all enemies.")
            for e in enemies:
                multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][e.element]
                damage = int(self.atk * multiplier)
                e.hp -= damage // 2
                e.hp = max(0, e.hp)  # Prevent negative HP
                
                # Display element advantage/disadvantage
                if multiplier > 1.0:
                    advantage = "⚡EFFECTIVE⚡"
                elif multiplier < 1.0:
                    advantage = "❄️RESIST❄️"
                else:
                    advantage = ""
                
                print(f"{owner_name}'s [{self.element}{self.name}] attack [{e.element}{e.name}] make {damage//2} point damage {advantage} (HP {e.hp}).")
        
        # AOE-3 skill: Attack 3 random enemies
        elif self.skill == "AOE-3" and enemies:
            targets = random.sample(enemies, min(3, len(enemies)))
            print(f"{owner_name}'s [{self.element}{self.name}] cast AOE-3, make attack to {len(targets)} enemies.")
            for e in targets:
                multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][e.element]
                damage = int(self.atk * multiplier)
                e.hp -= damage // 3
                e.hp = max(0, e.hp)
                
                # Display element advantage/disadvantage
                if multiplier > 1.0:
                    advantage = "⚡EFFECTIVE⚡"
                elif multiplier < 1.0:
                    advantage = "❄️RESIST❄️"
                else:
                    advantage = ""
                    
                print(f"{owner_name}'s [{self.element}{self.name}] attack [{e.element}{e.name}] make {damage//3} point damage {advantage} (HP {e.hp}).")
        
        # AOE-2 skill: Attack 2 random enemies
        elif self.skill == "AOE-2" and enemies:
            targets = random.sample(enemies, min(2, len(enemies)))
            print(f"{owner_name}'s [{self.element}{self.name}] cast AOE-2, make attack to {len(targets)} enemies.")
            for e in targets:
                multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][e.element]
                damage = int(self.atk * multiplier)
                e.hp -= damage // 2
                e.hp = max(0, e.hp)
                
                # Display element advantage/disadvantage
                if multiplier > 1.0:
                    advantage = "⚡EFFECTIVE⚡"
                elif multiplier < 1.0:
                    advantage = "❄️RESIST❄️"
                else:
                    advantage = ""
                    
                print(f"{owner_name}'s [{self.element}{self.name}] attack [{e.element}{e.name}] make {damage//2} point damage {advantage} (HP {e.hp}).")
        
        # Other skills and normal attack
        else:
            # Shield skill: Add shield to self
            if self.skill == "shield":
                shield_amount = self.atk // 2
                print(f"{owner_name}'s [{self.element}{self.name}] cast shield, get {shield_amount} shield.")
                self.hp += shield_amount
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
            
            # Heal skill: Heal all allies
            elif self.skill == "heal" and allies:
                heal_amount = self.atk // 2
                print(f"{owner_name}'s [{self.element}{self.name}] cast heal, all allies recover {heal_amount} HP.")
                for ally in allies:
                    if ally.is_alive():
                        ally.hp += heal_amount
                        if ally.hp > ally.max_hp:
                            ally.hp = ally.max_hp
                        print(f"{ally.element}{ally.name} HP recovered to {ally.hp}.")
            
            # Normal attack: Target one random enemy
            target = random.choice(enemies)
            multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][target.element]
            damage = int(self.atk * multiplier)
            target.hp -= damage
            target.hp = max(0, target.hp)
            
            # Display element advantage/disadvantage
            if multiplier > 1.0:
                advantage = "⚡EFFECTIVE⚡"
            elif multiplier < 1.0:
                advantage = "❄️RESIST❄️"
            else:
                advantage = ""
                
            print(f"{owner_name}'s [{self.element}{self.name}] attack [{target.element}{target.name}] make {damage} point damage {advantage} (HP {target.hp}).")