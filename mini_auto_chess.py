'''
This is a text-based auto chess game.
The game consists of two players, each with a pool of units to buy and deploy on the battlefield.
The players take turns to buy units, deploy them, and battle against each other.
The game includes unit attributes, skills, and school synergies that affect the gameplay.
'''

import random
import time
from collections import defaultdict

# === Element Damage Multiplier ===
ELEMENT_DAMAGE_MULTIPLIER = {
    "🔴": {"🔴": 2.0, "🟡": 1.0, "🔵": 0.5},
    "🟡": {"🔴": 0.5, "🟡": 2.0, "🔵": 1.0},
    "🔵": {"🔴": 1.0, "🟡": 0.5, "🔵": 2.0},
}


MAX_UNITS_ON_FIELD = 10


# Unit Class
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
        self.max_hp = int(self.max_hp * 1.8)
        self.base_atk = int(self.base_atk * 1.5)
        self.atk = self.base_atk
        self.hp = self.max_hp
        print(f"{self.name} goes up to {self.star} STR!")



    def attack(self, enemies, allies, owner_name):
        '''
        Activates the unit's special ability in battle.
        
        Executes the unit's special skill based on its type, targeting either
        enemies or allies depending on the skill's function.
        
        Parameters:
            enemies (list): A list of enemy Unit objects that can be targeted.
            allies (list): A list of allied Unit objects that can be targeted or affected.
            
        Returns:
            None
        '''

        if self.skill == "AOE-all" and enemies:
            print(f"{owner_name}'s [{self.name}] cast AOE, make attack to all enemies.")
            for e in enemies:
                multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][e.element]
                damage =  int(self.atk * multiplier)
                e.hp -= damage // 2
                print(f"{owner_name}'s [{self.element}{self.name}] attack [{e.element}{e.name}] make {damage} point damage (HP {e.hp}).")
        
        elif self.skill == "AOE-3" and enemies:
            targets = random.sample(enemies, min(3, len(enemies)))
            print(f"{owner_name}'s [{self.name}] cast AOE-3, make attack to {len(targets)} enemies.")
            for e in targets:
                multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][e.element]
                damage =  int(self.atk * multiplier)
                e.hp -= damage // 3
                print(f"{owner_name}'s [{self.element}{self.name}] attack [{e.element}{e.name}] make {damage} point damage (HP {e.hp}).")

        elif self.skill == "AOE-2" and enemies:
            targets = random.sample(enemies, min(2, len(enemies)))
            print(f"{owner_name}'s [{self.element}{self.name}] cast AOE-2, make attack to {len(targets)} enemies.")
            for e in targets:
                multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][e.element]
                damage =  int(self.atk * multiplier)
                e.hp -= damage // 2
                print(f"{owner_name}'s [{self.element}{self.name}] attack [{e.element}{e.name}] make {damage} point damage (HP {e.hp}).")

        else:
            if self.skill == "shield":
                print(f"{owner_name}'s [{self.name}] cast shield, get {self.atk // 2} shield.")
                self.hp += self.atk // 2
                if self.hp > self.max_hp:
                    self.hp = self.max_hp
            
            if self.skill == "heal":
                print(f"{owner_name}'s [{self.name}] casts heal-all, teammates recover {self.atk // 2} HP.")
                for ally in allies:
                    if ally.is_alive():
                        ally.hp += self.atk // 2
                        if ally.hp > ally.max_hp:
                            ally.hp = ally.max_hp

            target = random.choice(enemies)
            multiplier = ELEMENT_DAMAGE_MULTIPLIER[self.element][target.element]
            damage =  int(self.atk * multiplier)
            target.hp -= damage
            target.hp = max(0, target.hp)
            print(f"{owner_name}'s [{self.element}{self.name}] attack [{target.element}{target.name}] make {damage} point damage (HP {target.hp}).")
    


# === Shop Class ===
class Shop:
    '''
    Represents the in-game shop where players can purchase units.
    
    The Shop class manages the available units for purchase and provides
    a selection mechanism for players to choose from.
    
    Parameters:
        pool (list): A list of Unit objects available for purchase in the game.
    '''
    def __init__(self, pool):
        self.pool = pool

    def get_choices(self):
        '''
        Generates a random selection of units for purchase.
        
        Picks a random subset of units from the pool to offer to the player
        during their shopping phase.
        
        Returns:
            list: A list of up to 5 Unit objects randomly selected from the shop's pool.
        '''
        return [Unit(u.name, u.cost, u.max_hp, u.atk, u.skill, u.school, u.element) for u in random.sample(self.pool, min(5, len(self.pool)))]

# === Player Class ===
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
        self.fail = 0
        self.units = []
        self.reserve = []
        self.unit_counter = defaultdict(int)

    def income(self):
        '''
        Calculates and adds income to the player's gold at the start of their turn.
        
        Determines the player's income based on base income, interest on current gold,
        and bonus gold for consecutive losses, then adds it to the player's total.
        
        Returns:
            None
        '''
        base_income = 5
        interest = self.gold // 10
        fail_bonus = self.fail * 1
        self.gold += base_income + interest + fail_bonus
        print(f"{self.name} get income: base {base_income} + interest {interest} + fail bonus {fail_bonus} = {base_income + interest + fail_bonus} gold.")

    def buy_unit(self, unit: Unit):
        '''
        Purchases a unit from the shop and adds it to the player's reserve.
        
        Checks if the player has enough gold, deducts the cost if possible,
        and adds a new copy of the unit to the player's reserve. Also triggers
        the merge check to combine identical units if possible.
        
        Parameters:
            unit (Unit): The unit to purchase.
            
        Returns:
            None
        '''
        if self.gold >= unit.cost:
            self.gold -= unit.cost
            new_unit = Unit(unit.name, unit.cost, unit.max_hp, unit.atk, unit.skill, unit.school, unit.element)
            self.reserve.append(new_unit)
            print(f"{self.name} bought {new_unit.name}")
            self.try_merge()
        else:
            print(f"{self.name} hasn't enough gold, can't buy {unit.name}")

    def try_merge(self):
        '''
        Attempts to merge three identical units into an upgraded version.
        
        Checks the player's reserve for sets of three identical units with the same name,
        removes them, and adds a new unit with increased star level.
        
        Returns:
            None
        '''
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
        '''
        Selects units from the reserve to deploy on the battlefield.
        
        Takes the first MAX_UNITS_ON_FIELD units from the reserve and prepares
        them for battle by resetting their health points to maximum.
        
        Returns:
            None
        '''
        self.units = self.reserve[:MAX_UNITS_ON_FIELD]  # simply take first 10 units
        for u in self.units: 
            u.hp = u.max_hp

    def show_units(self):
        '''
        Displays information about all units in the player's reserve.
        
        Prints details about each unit including its name, star level, HP,
        attack, skill, and school for the player to review.
        
        Returns:
            None
        '''
        if self.reserve == []:
            print(f"{self.name} has no units.")
        else:
            for i, u in enumerate(self.reserve):
                print(f"[{i}] {u.element}{u.name}★{u.star} - HP: {u.get_health_bar()}, ATK: {u.atk}, skill: {u.skill}, school: {u.school}")

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

        synergy_active = {school: count >= 2 for school, count in school_count.items()}
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
        school_count = defaultdict(int)
        for u in self.units:
            school_count[u.school] += 1

        active_synergies = {school for school, count in school_count.items() if count >= 2}

        for u in self.units:
            u.atk = u.base_atk

            if u.school in active_synergies:
                u.atk += 1
                # print(f"{u.name} gets +1 ATK from {u.school} synergy boost!")


# === Battle ===
def battle(p1: Player, p2: Player):
    '''
    Simulates a battle between two players' deployed units.
    
    Handles the combat sequence where units from both sides attack
    each other and use their skills until one team is defeated.
    
    Parameters:
        p1 (Player): The first player.
        p2 (Player): The second player.
        
    Returns:
        None
    '''
    input("Press Enter to start the battle...")
    print("\n=== Auto Battle Start ===")
    p1.deploy_units()
    p2.deploy_units()

    p1.apply_synergy_bonus()
    p2.apply_synergy_bonus()

    team1 = p1.units.copy()
    team2 = p2.units.copy()
    round_num = 1

    while any(u.is_alive() for u in team1) and any(u.is_alive() for u in team2):
        print(f"\n--- Battle {round_num} ---")
        for u in team1:
            if u.is_alive():
                enemies = [e for e in team2 if e.is_alive()]
                if enemies:
                    u.attack(enemies=enemies, allies=team1, owner_name=p1.name)
                    print()

        for u in team2:
            if u.is_alive():
                enemies = [e for e in team1 if e.is_alive()]
                if enemies:
                    u.attack(enemies=enemies, allies=team1, owner_name=p2.name)
                    print()

        round_num += 1
        time.sleep(1)

    alive1 = sum(1 for u in team1 if u.is_alive())
    alive2 = sum(1 for u in team2 if u.is_alive())
    if alive1 > alive2:
        print(f"\n🏆 {p1.name} Win!")
        p1.fail = 0
        p2.fail += 1
    elif alive2 > alive1:
        print(f"\n🏆 {p2.name} Win!")
        p2.fail = 0
        p1.fail += 1
    else:
        print("\n🤝 Equal!")

    print(f"\n{p1.name}'s Current Units:")
    p1.show_units()
    print(f"\n{p2.name}'s Current Units:")
    p2.show_units()
    input("Press Enter to continue...")

def display_units_list(units):
        '''
        Displays a list of units with formatted attributes.
        
        Parameters:
            units (list of Unit): Units to be displayed.
        '''
        print(f"{'Idx':<4} {'Name':<12} {'Gold':<5} {'HP':<5} {'ATK':<5} {'Skill':<15} {'School'}")
        print("-" * 60)
        for i, u in enumerate(units):
            print(f"{i:<4} {u.element + u.name:<12} {u.cost:<5} {u.max_hp:<5} {u.atk:<5} {u.skill:<15} {u.school}")
        print()

# === One Round Process ===
def game_round(p1, p2, shop):
    '''
    Manages a complete game round including shopping and battle phases.
    
    Handles the income calculation, unit shopping for both the human player
    and AI opponent, and displays relevant information about units and synergies.
    
    Parameters:
        p1 (Player): The human player.
        p2 (Player): The AI player.
        shop (Shop): The shop providing units for purchase.
        
    Returns:
        None
    '''
    print(f"\n===== {p1.name}'s Shopping Phase =====")
    p1.income()

    while True:
        print(f"\n{p1.name}'s Current Units:")
        p1.show_units()
        print(f"Gold: {p1.gold}")

        choices = shop.get_choices()
        display_units_list(choices)

        buy = input("Input the number(s) to buy (space-separated), or press Enter to finish buying: ").strip()
        if not buy:
            break

        try:
            indices = list(map(int, buy.split()))
            for idx in indices:
                if 0 <= idx < len(choices):
                    p1.buy_unit(choices[idx])
                else:
                    print(f"Index {idx} is out of range.")
        except ValueError:
            print("Invalid input! Please enter numbers separated by spaces.")

    print(f"\n== {p1.name}'s Final Units After Shopping ==")
    p1.show_units()
    print("Recent synergy:", ", ".join(p1.get_synergy()))
    print()

    # AI Player Phase
    print(f"===== {p2.name}'s Turn (AI) =====")
    p2.income()
    for u in shop.get_choices():
        if len(p2.reserve) < 20 and p2.gold >= u.cost:
            p2.buy_unit(u)

    print(f"\n== {p2.name}'s Final Units After Shopping ==")
    p2.show_units()
    print("Recent synergy:", ", ".join(p2.get_synergy()))
    print()



# === Unit Pool ===
unit_pool = [
    Unit("Momoi", 4, 6, 6, "AOE-2", "Millennium", "🟡"),
    Unit("Yuuka", 4, 15, 3, "shield", "Millennium", "🔴"),
    Unit("Alice", 4, 5, 6, "AOE-3", "Millennium", "🔵"),
    Unit("Asuna", 3, 8, 5, "/", "Millennium", "🔵"),

    Unit("Mika", 7, 10, 8, "/", "Trinity", "🟡"),
    Unit("Koharu", 4, 6, 3, "heal", "Trinity", "🔴"),
    Unit("Natsu", 5, 12, 5, "shield", "Trinity", "🔵"),
    Unit("Hanako", 3, 5, 4, "AOE-all", "Trinity", "🔵"),

    Unit("Hina", 6, 8, 9, "/", "Gehenna", "🔴"),
    Unit("Mutsuki", 5, 6, 4, "AOE-3", "Gehenna", "🔴"),
    Unit("Iroha", 10, 6, 6, "AOE-all", "Gehenna", "🔵"),
    Unit("Iori", 4, 6, 4, "/", "Gehenna", "🟡"),

    Unit("Hoshino", 5, 14, 4, "shield", "Abydos", "🟡"),
    Unit("Shiroko", 3, 8, 4, "/", "Abydos", "🔴"),
    Unit("Mizu", 4, 7, 5, "/", "SRT", "🟡"),

]

def show_tutorial(language="en"):
    '''
    Show the game tutorial in the selected language.
    
    Parameters:
        language (str): The language for the tutorial, either "en" for English or "zh" for Chinese.
        
    Returns:
        None
    '''

    tutorial_en = '''
╔════════════════════════════════════════════════════════════╗
║                  Mini AUTO CHESS GUIDE                     ║
╚════════════════════════════════════════════════════════════╝

【GAME CONCEPT】
Auto Chess is a strategic board game where you need to purchase units, upgrade them, 
and arrange your lineup wisely to defeat your opponent.

【BASIC CONCEPTS】
• Units: Each unit has Name, HP, ATK, Skill, School, and Element
• Element System: 🔴>🔵>🟡>🔴 (2x damage bonus, 0.5x damage penalty)
• Star Level: Combine three identical units to level up, increasing HP by 80% and ATK by 50%
• School Synergy: Having 2+ units from the same school gives +1 ATK bonus

【GAME FLOW】
1. At the start of each round, get basic gold + interest (current gold÷10) + failure compensation
2. Purchase units and add them to your reserve
3. The first 10 units in your reserve will automatically enter battle
4. Units automatically attack enemies and use skills during battle
5. Play for 5 rounds, victory determined by number of wins

【UNIT SKILLS】
• AOE-all: Deal half ATK damage to all enemies
• AOE-3: Deal one-third ATK damage to 3 random enemies
• AOE-2: Deal half ATK damage to

• shield: Provide shield equal to half your ATK
• heal: Restore half ATK worth of HP to all friendly units

【STRATEGY TIPS】
• Actively collect identical units to upgrade stars
• Try to activate school synergy effects
• Pay attention to element relationships for favorable matchups
• Prioritize upgrading high-star units for significant power boosts
• Maintain a good amount of gold to earn more interest

【CONTROLS】
• Buy units: Enter corresponding numbers (space-separated for multiple purchases)
• End shopping: Press Enter directly
• The first 10 units in your reserve will automatically deploy, so arrange them carefully

Enjoy the game!
'''


    tutorial_zh = '''
╔════════════════════════════════════════════════════════════╗
║                   迷你自走棋游戏指南                          ║
╚════════════════════════════════════════════════════════════╝

【游戏概念】
自走棋是一种策略性战棋游戏，您需要通过购买单位、升级单位并合理安排阵容来击败对手。

【基本概念】
• 单位：每个单位都有名称、生命值(HP)、攻击力(ATK)、技能(Skill)、学院(School)和元素(Element)
• 元素相克系统：🔴>🔵>🟡>🔴 (伤害加成为2倍，减成为0.5倍)
• 星级：通过合成三个相同单位可以提升星级，升级后HP增加80%，攻击力增加50%
• 学院协同效应：场上同一学院的单位达到2个或以上时，获得+1攻击力加成

【游戏流程】
1. 每回合开始时获得基础金币+利息(当前金币÷10)+失败补偿
2. 购买单位并添加到备战区
3. 备战区前10个单位会自动上场参战
4. 战斗环节中单位会自动攻击对方并使用技能
5. 连续进行5个回合，胜负由胜场数决定

【单位技能】
• AOE-all：对所有敌人造成一半攻击力的伤害
• AOE-3：随机对3个敌人造成三分之一攻击力的伤害
• AOE-2：随机对2个敌人造成二分之一攻击力的伤害
• shield：为自己提供攻击力一半的护盾
• heal：为所有友方单位恢复攻击力一半的生命值

【战略提示】
• 积极收集相同单位进行合成升星
• 尽可能激活学院协同效应
• 注意元素相克关系，合理配置不同元素的单位
• 优先合成高星级单位，它们的战斗力提升显著
• 保持适当的金币量可以获得更多利息收入

【操作方法】
• 购买单位：输入对应的数字(用空格分隔多个购买)
• 结束购买：直接按下回车键

祝您游戏愉快！

'''
    
    if language == "en":
        print(tutorial_en)
    else:
        print(tutorial_zh)

    input("\nPress Enter to return to game... / 按Enter键返回游戏...\n")

# === Game Main ===
def main():
    '''
    The main game loop that initializes the game and runs multiple rounds.
    
    Sets up the game environment with players and shop, then runs a fixed
    number of game rounds before ending the game.
    
    Returns:
        None
    '''
    print("\n=== Welcome to Mini Auto Chess Game! ===")

    show_help = input("Would you like to see the game tutorial? (y/n): ").lower().strip()
    if show_help == 'y' or show_help == 'yes':
        language_choice = input("Choose language / 选择语言 (en/zh): ").lower().strip()
        language = "en" if language_choice != "zh" else "zh"
    
    
        show_tutorial(language)

    shop = Shop(unit_pool)
    player_name = input("Enter your name: ")
    player1 = Player(player_name)
    player2 = Player("AI")

    for round_id in range(1, 6):
        print(f"\n\n🌟🌟 Round {round_id} 🌟🌟")
        game_round(player1, player2, shop)
        battle(player1, player2)

    print("\n🎮 Game Over! Thanks for Playing!")

if __name__ == "__main__":
    main()
