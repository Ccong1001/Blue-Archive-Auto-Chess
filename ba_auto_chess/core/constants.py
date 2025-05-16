"""
Game constants definition
"""

# Element damage multiplier table
ELEMENT_DAMAGE_MULTIPLIER = {
    "🔴": {"🔴": 2.0, "🟡": 1.0, "🔵": 0.5},
    "🟡": {"🔴": 0.5, "🟡": 2.0, "🔵": 1.0},
    "🔵": {"🔴": 1.0, "🟡": 0.5, "🔵": 2.0},
}

# Maximum number of units on the field
MAX_UNITS_ON_FIELD = 10

# Unit pool - templates for all available units
UNIT_POOL = [
    {"name": "Momoi", "cost": 4, "hp": 6, "atk": 6, "skill": "AOE-2", "school": "Millennium", "element": "🟡"},
    {"name": "Yuuka", "cost": 4, "hp": 15, "atk": 3, "skill": "shield", "school": "Millennium", "element": "🔴"},
    {"name": "Alice", "cost": 4, "hp": 5, "atk": 6, "skill": "AOE-3", "school": "Millennium", "element": "🔵"},
    {"name": "Asuna", "cost": 3, "hp": 8, "atk": 5, "skill": "/", "school": "Millennium", "element": "🔵"},
    
    {"name": "Mika", "cost": 7, "hp": 10, "atk": 8, "skill": "/", "school": "Trinity", "element": "🟡"},
    {"name": "Koharu", "cost": 4, "hp": 6, "atk": 3, "skill": "heal", "school": "Trinity", "element": "🔴"},
    {"name": "Natsu", "cost": 5, "hp": 12, "atk": 5, "skill": "shield", "school": "Trinity", "element": "🔵"},
    {"name": "Hanako", "cost": 3, "hp": 5, "atk": 4, "skill": "AOE-all", "school": "Trinity", "element": "🔵"},
    
    {"name": "Hina", "cost": 6, "hp": 8, "atk": 9, "skill": "/", "school": "Gehenna", "element": "🔴"},
    {"name": "Mutsuki", "cost": 5, "hp": 6, "atk": 6, "skill": "AOE-3", "school": "Gehenna", "element": "🔴"},
    {"name": "Iroha", "cost": 10, "hp": 6, "atk": 6, "skill": "AOE-all", "school": "Gehenna", "element": "🔵"},
    {"name": "Iori", "cost": 4, "hp": 6, "atk": 4, "skill": "/", "school": "Gehenna", "element": "🟡"},
    
    {"name": "Hoshino", "cost": 5, "hp": 14, "atk": 4, "skill": "shield", "school": "Abydos", "element": "🟡"},
    {"name": "Shiroko", "cost": 3, "hp": 8, "atk": 4, "skill": "/", "school": "Abydos", "element": "🔴"},
    {"name": "Mizu", "cost": 4, "hp": 7, "atk": 5, "skill": "/", "school": "SRT", "element": "🟡"},
]