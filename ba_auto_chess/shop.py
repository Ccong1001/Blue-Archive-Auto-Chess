# shop.py
import random
from unit import Unit

class Shop:
    def __init__(self, pool):
        self.pool = pool

    def get_choices(self, level):
        return [Unit(u.name, u.cost, u.max_hp, u.atk, u.skill, u.school, u.element) for u in random.sample(self.pool, min(5, len(self.pool)))]
