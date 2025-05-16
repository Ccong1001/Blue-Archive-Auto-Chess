"""
Game tutorial text and display functionality
"""

def show_tutorial(language="en"):
    '''
    Displays the game tutorial in the selected language.
    
    Parameters:
        language (str): Language choice, "en" for English, "zh" for Chinese
        
    Returns:
        None
    '''
    tutorial_en = '''
╔════════════════════════════════════════════════════════════╗
║                  Blue Archive AUTO CHESS GUIDE             ║
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
• AOE-2: Deal half ATK damage to 2 random enemies
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
║                   蔚蓝档案自走棋游戏指南                      ║
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
• 备战区前10个单位会自动上场，注意调整顺序

祝您游戏愉快！
'''
    
    if language == "en":
        print(tutorial_en)
    else:
        print(tutorial_zh)
    
    input("\nPress Enter to return to game... / 按Enter键返回游戏...\n")