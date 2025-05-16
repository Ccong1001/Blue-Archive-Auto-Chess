class Unit:
    def __init__(self, name, atk, hp, skills):
        self.name = name
        self.atk = atk
        self.hp = hp
        self.skills = skills

    def use_skill(self, skill_name, target):
        if skill_name in self.skills:
            skill = self.skills[skill_name]
            skill.apply(self, target)

    def take_damage(self, amount):
        self.hp -= amount
        if self.hp < 0:
            self.hp = 0

    def is_alive(self):
        return self.hp > 0

    def __str__(self):
        return f"{self.name} - ATK: {self.atk}, HP: {self.hp}"