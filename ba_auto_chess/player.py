# player.py
from collections import defaultdict
from unit import Unit, MAX_UNITS_ON_FIELD

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
            print(f"[{i}] {u.name}★{u.star} - HP: {u.get_health_bar()}, ATK: {u.atk}, skill: {u.skill}, school: {u.school}")

    def get_synergy(self):
        from collections import defaultdict
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1
        bonuses = []
        for r, c in school_count.items():
            if c >= 2: bonuses.append(f"{r} synergy(+1 ATK)")
        return bonuses
    
    def apply_synergy_bonus(self):
        from collections import defaultdict
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1
        for u in self.units:
            u.atk = u.base_atk
            if school_count[u.school] >= 2:
                u.atk += 1
