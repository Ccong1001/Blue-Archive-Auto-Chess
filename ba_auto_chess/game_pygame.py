import pygame
import sys
import random
from unit import Unit, ELEMENT_DAMAGE_MULTIPLIER, MAX_UNITS_ON_FIELD
from player import Player
from shop import Shop
from battle import battle
from unit_pool import unit_pool

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Auto Chess Pygame Demo")
font = pygame.font.SysFont("consolas", 20)
clock = pygame.time.Clock()

# color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARKGRAY = (150, 150, 150)
GREEN = (0, 180, 0)
DARKGREEN = (0, 120, 0)
RED = (200, 0, 0)
DARKRED = (120, 0, 0)
BLUE = (0, 0, 200)
LIGHTBLUE = (100, 100, 255)

# 简单点击音效
# click_sound = pygame.mixer.Sound(pygame.mixer.Sound.buffer(b'\x00' * 100))

class Button:
    def __init__(self, rect, text, color=GRAY, hover_color=DARKGRAY, text_color=BLACK):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        pygame.draw.rect(surface, BLACK, self.rect, 2, border_radius=8)
        txt_surf = font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        surface.blit(txt_surf, txt_rect)

    def update_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class GameUI:
    def __init__(self, player_name):
        self.shop = Shop(unit_pool)
        self.player1 = Player(player_name)
        self.player2 = Player("AI")
        self.round_id = 1
        self.phase = "shop"
        self.shop_choices = []
        self.message = ""
        self.battle_log = []
        self.winner = None

        self.refresh_shop_choices()
        self.create_buttons()

    def create_buttons(self):
        self.buy_buttons = []
        base_x, base_y = 650, 350
        for i in range(len(self.shop_choices)):
            btn = Button((base_x, base_y + 25 * (i + 1) - 5, 80, 30), "Buy", color=GREEN, hover_color=DARKGREEN, text_color=WHITE)
            self.buy_buttons.append(btn)
        self.battle_button = Button((650, 550, 140, 50), "Start Battle", GREEN, DARKGREEN, WHITE)

    def refresh_shop_choices(self):
        self.shop_choices = self.shop.get_choices(self.player1.level)
        self.create_buttons()

    def draw(self):
        screen.fill(WHITE)

        # 标题栏
        pygame.draw.rect(screen, LIGHTBLUE, (0, 0, WIDTH, 80))
        title_surf = font.render(f"Round {self.round_id} - Player Gold: {self.player1.gold}", True, BLACK)
        phase_surf = font.render(f"Phase: {self.phase.upper()}", True, BLACK)
        screen.blit(title_surf, (20, 20))
        screen.blit(phase_surf, (20, 50))

        # 玩家单位区块
        pygame.draw.rect(screen, GRAY, (10, 90, 400, 200), border_radius=10)
        screen.blit(font.render(f"{self.player1.name} Units:", True, BLUE), (20, 100))
        for i, unit in enumerate(self.player1.reserve):
            text = f"{unit.name} ★{unit.star} HP:{unit.hp}/{unit.max_hp} ATK:{unit.atk} Skill:{unit.skill}"
            screen.blit(font.render(text, True, BLACK), (40, 125 + 25 * i))

        # 商店区块
        pygame.draw.rect(screen, GRAY, (10, 340, 600, 160), border_radius=10)
        screen.blit(font.render("Shop - Click unit to buy:", True, RED), (20, 350))
        for i, unit in enumerate(self.shop_choices):
            text = f"[{i}] {unit.name} (Cost:{unit.cost}) HP:{unit.max_hp} ATK:{unit.atk} Skill:{unit.skill}"
            screen.blit(font.render(text, True, BLACK), (40, 375 + 25 * i))
            self.buy_buttons[i].draw(screen)

        # 战斗按钮
        self.battle_button.draw(screen)

        # 战斗日志区域
        pygame.draw.rect(screen, GRAY, (430, 90, 450, 440), border_radius=10)
        screen.blit(font.render("Battle Log:", True, BLACK), (440, 100))
        max_logs = 20
        logs = self.battle_log[-max_logs:]
        for i, line in enumerate(logs):
            screen.blit(font.render(line, True, BLACK), (440, 125 + 20 * i))

        # 消息显示
        msg_color = RED if self.phase == "shop" else BLUE
        msg_surf = font.render(self.message, True, msg_color)
        screen.blit(msg_surf, (20, 520))

    def update_hover_states(self, mouse_pos):
        for btn in self.buy_buttons:
            btn.update_hover(mouse_pos)
        self.battle_button.update_hover(mouse_pos)

    def buy_unit(self, idx):
        if idx < 0 or idx >= len(self.shop_choices):
            self.message = "Invalid choice!"
            return
        unit = self.shop_choices[idx]
        if self.player1.gold >= unit.cost:
            self.player1.buy_unit(unit)
            self.message = f"Bought {unit.name}"
            # click_sound.play()
            self.refresh_shop_choices()
        else:
            self.message = "Not enough gold!"

    def start_battle(self):
        self.phase = "battle"
        self.battle_log.clear()
        # 省略战斗过程，和你原代码类似...

    def next_round(self):
        if self.phase == "result":
            self.round_id += 1
            self.player1.income()
            self.player2.income()
            self.refresh_shop_choices()
            self.phase = "shop"
            self.message = ""
            self.winner = None


def main():
    player_name = input("Enter your player name: ")
    ui = GameUI(player_name)

    while True:
        mouse_pos = pygame.mouse.get_pos()
        ui.update_hover_states(mouse_pos)
        ui.draw()
        pygame.display.flip()
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if ui.phase == "shop":
                    for i, btn in enumerate(ui.buy_buttons):
                        if btn.is_clicked(pos):
                            ui.buy_unit(i)
                    if ui.battle_button.is_clicked(pos):
                        ui.start_battle()
                elif ui.phase == "result":
                    if ui.battle_button.is_clicked(pos):
                        ui.next_round()

if __name__ == "__main__":
    main()
