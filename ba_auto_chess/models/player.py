"""
Player class definition
"""

from collections import defaultdict
from core.constants import MAX_UNITS_ON_FIELD
from models.unit import Unit

class Player:
    '''
    Represents a player in the auto chess game.
    
    The Player class manages a player's resources, units (both in reserve and
    deployed), and handles all player-related actions such as buying units,
    merging identical units, and deploying units for battle.
    
    Parameters:
        name (str): The name of the player.
    '''
    
    def __init__(self, name):
        self.name = name
        self.gold = 5
        self.units = []  # Units on the field
        self.reserve = []  # Units in reserve
        self.fail = 0  # Track consecutive losses for comeback gold
    
    def income(self):
        '''
        Calculates and adds income to the player's gold at the start of their turn.
        
        Determines the player's income based on base income, interest on current gold,
        and bonus gold for consecutive losses, then adds it to the player's total.
        
        Returns:
            None
        '''
        base_income = 5
        interest = self.gold // 10  # 10% interest
        streak_gold = self.fail  # Gold bonus for consecutive losses
        
        total_income = base_income + interest + streak_gold
        self.gold += total_income
        
        print(f"{self.name} gets income: base {base_income} + interest {interest} + loss streak {streak_gold} = {total_income} gold.")
        print(f"Gold :{self.gold}")
    
    def buy_unit(self, unit):
        '''
        Purchases a unit from the shop and adds it to the player's reserve.
        
        Checks if the player has enough gold, deducts the cost if possible,
        and adds a new copy of the unit to the player's reserve. Also triggers
        the merge check to combine identical units if possible.
        
        Parameters:
            unit (Unit): The unit to purchase.
            
        Returns:
            bool: True if purchase successful, False otherwise.
        '''
        if self.gold < unit.cost:
            print(f"{self.name} doesn't have enough gold to buy {unit.name}.")
            return False
        
        self.gold -= unit.cost
        self.reserve.append(unit)
        print(f"{self.name} bought {unit.element}{unit.name}")
        
        # Try to merge after each purchase
        self.try_merge()
        return True
    
    def try_merge(self):
        '''
        Attempts to merge three identical units into an upgraded version.
        
        Checks the player's reserve for sets of three identical units with the same name,
        removes them, and adds a new unit with increased star level.
        
        Returns:
            None
        '''
        # Count units by name
        name_count = defaultdict(list)
        for i, unit in enumerate(self.reserve):
            name_count[unit.name].append(i)
        
        # Check for mergeable units (2 or more of the same name and star)
        for name, indices in name_count.items():
            # Group units by star level
            by_star = defaultdict(list)
            for idx in indices:
                by_star[self.reserve[idx].star].append(idx)
            
            # Try to merge for each star level
            for star, idx_list in by_star.items():
                if len(idx_list) >= 2:
                    # Get properties from first unit
                    base_unit = self.reserve[idx_list[0]]
                    
                    # Create upgraded unit
                    upgraded = Unit(
                        base_unit.name, 
                        base_unit.cost, 
                        base_unit.max_hp, 
                        base_unit.base_atk,
                        base_unit.skill,
                        base_unit.school,
                        base_unit.element
                    )
                    upgraded.star = star
                    upgraded.upgrade()  # Increase star and stats
                    
                    # Remove 3 units from reserve (starting with highest index to avoid shifting issues)
                    for idx in sorted(idx_list[:2], reverse=True):
                        self.reserve.pop(idx)
                    
                    # Add the upgraded unit
                    self.reserve.append(upgraded)
                    
                    print(f"{self.name} successfully merged {upgraded.element}{upgraded.name} to ★{upgraded.star}")
                    
                    # Recursively check for more merges
                    self.try_merge()
                    return
    
    def deploy_units(self):
        '''
        Selects units from the reserve to deploy on the battlefield.
        
        Takes the first MAX_UNITS_ON_FIELD units from the reserve and prepares
        them for battle by resetting their health points to maximum.
        
        Returns:
            None
        '''
        # Reset units list
        self.units = []
        
        # Take up to MAX_UNITS_ON_FIELD from reserve
        deploy_count = min(MAX_UNITS_ON_FIELD, len(self.reserve))
        for i in range(deploy_count):
            unit = self.reserve[i]
            unit.hp = unit.max_hp  # Reset HP for battle
            self.units.append(unit)
        
        # Apply synergy bonuses
        self.apply_synergy_bonus()
    
    def show_units(self):
        '''
        Displays information about all units in the player's reserve.
        
        Prints details about each unit including its name, star level, HP,
        attack, skill, and school for the player to review.
        
        Returns:
            None
        '''
        if not self.reserve:
            print(f"{self.name} has no units.")
            return
        
        print(f"{'No.':<4} {'Name':<12} {'★':<2} {'HP':<5} {'ATK':<5} {'Skill':<10} {'School'}")
        print("-" * 60)
        
        for i, unit in enumerate(self.reserve):
            print(f"{i:<4} {unit.element+unit.name:<12} {unit.star:<2} {unit.max_hp:<5} {unit.atk:<5} {unit.skill:<10} {unit.school}")
    
    def get_synergy(self):
        '''
        Calculates school synergy bonuses based on deployed units.
        
        Counts the number of units from each school and determines which
        synergy bonuses are active (requiring at least 2 units from a school).
        
        Returns:
            list: A list of strings describing active synergy bonuses.
        '''
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1
        
        # Create dictionary recording whether each school has synergy
        synergy_active = {school: count >= 2 for school, count in school_count.items()}
        
        # Return descriptions for display
        bonus_descriptions = [f"{school} synergy(+1 ATK)" for school, active in synergy_active.items() if active]
        
        return bonus_descriptions
    
    def apply_synergy_bonus(self):
        '''
        Applies school synergy bonuses to deployed units.
        
        Updates the attack values of all deployed units based on active
        school synergies, giving +1 attack to units from schools with
        at least 2 representatives on the field.
        
        Returns:
            None
        '''
        # Calculate school unit counts
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1
        
        # Create active synergy set for faster lookup
        active_synergies = {school for school, count in school_count.items() if count >= 2}
        
        # Display active synergiesCOMP9001/project/ba_auto_chess/main.py
        if active_synergies:
            print("\n=== School Synergies ===")
            for school in active_synergies:
                print(f"🔹 {school} synergy active! - All {school} members get +1 ATK")
        
        # Apply synergy bonus
        for u in self.units:
            # First reset to base attack
            original_atk = u.atk
            u.atk = u.base_atk
            
            # If unit's school has synergy, increase attack
            if u.school in active_synergies:
                u.atk += 1
                if u.atk != original_atk:  # Only show if attack changed
                    print(f"  └─ {u.element}{u.name}★{u.star} attack: {u.base_atk} → {u.atk}")