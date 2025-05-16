class Economy:
    def __init__(self):
        self.gold = 0
        self.base_income = 5
        self.interest_rate = 0.05

    def generate_income(self):
        self.gold += self.base_income

    def calculate_interest(self):
        interest = int(self.gold * self.interest_rate)
        self.gold += interest

    def spend_gold(self, amount):
        if amount <= self.gold:
            self.gold -= amount
            return True
        return False

    def earn_gold(self, amount):
        self.gold += amount

    def get_gold(self):
        return self.gold