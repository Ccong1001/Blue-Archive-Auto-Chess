class Player:
    def __init__(self, name):
        self.name = name
        self.gold = 0
        self.units = []

    def earn_gold(self, amount):
        self.gold += amount

    def spend_gold(self, amount):
        if amount <= self.gold:
            self.gold -= amount
            return True
        return False

    def add_unit(self, unit):
        self.units.append(unit)

    def remove_unit(self, unit):
        if unit in self.units:
            self.units.remove(unit)