"""
Shop class definition
"""

import random
import copy
from models.unit import Unit
from core.constants import UNIT_POOL

class Shop:
    '''
    Represents the in-game shop where players can purchase units.
    
    The Shop class manages the available units for purchase and provides
    a selection mechanism for players to choose from.
    
    Parameters:
        pool (list): A list of Unit objects available for purchase in the game.
    '''
    
    def __init__(self, pool=None):
        self.pool = pool if pool is not None else []
        # If no pool provided, create units from UNIT_POOL constants
        if not self.pool:
            for unit_data in UNIT_POOL:
                self.pool.append(Unit(
                    unit_data["name"],
                    unit_data["cost"],
                    unit_data["hp"],
                    unit_data["atk"],
                    unit_data["skill"],
                    unit_data["school"],
                    unit_data["element"]
                ))
    
    def get_choices(self):
        '''
        Generates a random selection of units for purchase.
        
        Picks a random subset of units from the pool to offer to the player
        during their shopping phase.
        
        Returns:
            list: A list of up to 5 Unit objects randomly selected from the shop's pool.
        '''
        # Choose up to 5 units randomly
        choices_count = min(5, len(self.pool))
        choices = random.sample(self.pool, choices_count)
        
        # Return deep copies to avoid modifying the original units
        return [copy.deepcopy(unit) for unit in choices]