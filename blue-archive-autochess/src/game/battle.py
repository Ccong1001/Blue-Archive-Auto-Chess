class Battle:
    def __init__(self, player_units, enemy_units):
        self.player_units = player_units
        self.enemy_units = enemy_units

    def start_battle(self):
        while self.player_units and self.enemy_units:
            self.player_attack()
            if self.enemy_units:
                self.enemy_attack()

    def player_attack(self):
        for unit in self.player_units:
            if self.enemy_units:
                target = self.enemy_units[0]  # Attack the first enemy unit
                damage = unit.attack()
                target.take_damage(damage)
                if target.is_defeated():
                    self.enemy_units.remove(target)

    def enemy_attack(self):
        for unit in self.enemy_units:
            if self.player_units:
                target = self.player_units[0]  # Attack the first player unit
                damage = unit.attack()
                target.take_damage(damage)
                if target.is_defeated():
                    self.player_units.remove(target)