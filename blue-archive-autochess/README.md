# Blue Archive Auto Chess Game

A text-based auto chess game implemented in Python using Pygame where players strategically purchase, deploy, and battle with units to defeat their opponents.

## 🎮 Game Features
- **Strategic Unit Management**: Buy units, merge identical ones to upgrade stars, and deploy them for battle.
- **Element System**: 🔴 > 🔵 > 🟡 > 🔴 with 2x damage bonus and 0.5x damage penalty.
- **School Synergies**: Units from the same school gain +1 ATK when there are 2+ of them.
- **Various Unit Skills**: AOE attacks, shields, healing, and more.
- **Economy System**: Earn gold through income, interest, and loss streaks.
- **Automatic Battles**: Units fight autonomously using their skills and abilities.

## 🏗️ Project Structure
```
blue-archive-autochess
├── src
│   ├── main.py
│   ├── game
│   │   ├── __init__.py 
│   │   ├── battle.py
│   │   ├── economy.py
│   │   ├── player.py
│   │   └── unit.py
│   ├── gui
│   │   ├── __init__.py
│   │   ├── screens.py
│   │   ├── sprites.py
│   │   └── ui.py
│   ├── assets
│   │   ├── fonts
│   │   ├── images
│   │   └── sounds
│   └── utils
│       ├── __init__.py
│       ├── constants.py
│       └── helpers.py
├── requirements.txt
└── README.md
```

## 🛠️ Installation
1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd blue-archive-autochess
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## 🕹️ How To Play
1. Run the game:
   ```
   python src/main.py
   ```
2. Follow the on-screen prompts to purchase units and engage in battles.

## 📄 License
This project is licensed under the MIT License. See the LICENSE file for details.