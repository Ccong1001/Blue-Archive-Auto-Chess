# Blue Archive Auto Chess Game
A text-based auto chess game implemented in Python where players strategically purchase, deploy, and battle with units to defeat their opponents.

## 🎮 Game Features
- **Strategic Unit Management**: Buy units, merge identical ones to upgrade stars, and deploy them for battle
- **Element System**: 🔴 > 🔵 > 🟡 > 🔴 with 2x damage bonus and 0.5x damage penalty
- **school Synergies**: Units from the same school gain +1 ATK when there are 2+ of them
- **Various Unit Skills**: AOE attacks, shields, healing, and more
- **Economy System**: Earn gold through income, interest, and loss streaks
- Automatic Battles**: Units fight autonomously using their skills and abilities

## 🏗️ Project Structure
### 🎲 Gameplay
1. **Income Phase**: Receive gold based on base income, interest, and loss streak
2. **Shopping Phase**: Purchase units to add to your reserve
3. **Deployment**: First 10 units in your reserve are automatically deployed
4. **Battle**: Units automatically attack and use skills in combat
5. **Results**: Win/lose based on which team has more surviving units
### 💡 Strategic Elements
- **Unit Merging**: Combine 2 identical units to create a stronger ⭐⭐ unit
- **School Planning**: Deploy units from the same school to gain attack bonuses
3. **Element Matching**: Use favorable element matchups against your opponent
4. **Economy Management**: Balance spending versus saving for interest income
## 🕹️ How To Play
### Run the game:
Follow the prompts to:
1. View the tutorial (optional)
2. Enter your name
3. Purchase units by entering their indices
4. Watch the battle unfold between your units and the AI opponent
5. Repeat for 5 rounds to determine the overall winner

## 🛠️ Unit Skills
- AOE-all: Deal half ATK damage to all enemies
- AOE-3: Deal one-third ATK damage to 3 random enemies
- AOE-2: Deal half ATK damage to 2 random enemies
- shield: Provide shield equal to half your ATK
- heal: Restore half ATK worth of HP to all friendly units

## 🌟 Available Units
The game includes units from schools like Millennium, Trinity, Gehenna, and Abydos, each with unique stats and abilities.

## Pygame Version
coming soon