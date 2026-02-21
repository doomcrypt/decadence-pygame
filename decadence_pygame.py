import pygame
import random
import sys
import math
from constants import demons, pair_scores, BLACK, CRIMSON, GOLD, WHITE, DARK_RED, ABYSS_BLUE, SHADOW, GLOW, CARD_WIDTH, CARD_HEIGHT, CARD_RADIUS, CROSS_POS, SET2_POS, POSITION_LABELS, SUITS, SUIT_COLORS

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Fonts
FONT_LARGE = pygame.font.Font(None, 72)
FONT_MED = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 32)
FONT_TINY = pygame.font.Font(None, 24)

class Card:
    def __init__(self, rank, suit_idx):
        self.rank = rank
        self.suit_idx = suit_idx
        self.suit = SUITS[suit_idx]
        self.suit_color = SUIT_COLORS[suit_idx]
        self.rect = pygame.Rect(0, 0, CARD_WIDTH, CARD_HEIGHT)
        self.face_up = False
        self.paired = False
        self.flip_progress = 0.0  # for flip animation

    def draw(self, screen, pos, highlight=False):
        x, y = pos
        self.rect.topleft = (x, y)

        # Card background
        color = GOLD if highlight else (200, 150, 50)
        pygame.draw.rect(screen, color, self.rect, border_radius=CARD_RADIUS)
        pygame.draw.rect(screen, BLACK, self.rect, 4, border_radius=CARD_RADIUS)

        if self.face_up or self.flip_progress > 0:
            # Flip effect: scale width by sin(progress)
            flip_scale = abs(math.sin(self.flip_progress * math.pi))
            flip_rect = self.rect.copy()
            flip_rect.width *= flip_scale
            flip_rect.centerx = self.rect.centerx
            pygame.draw.rect(screen, color, flip_rect, border_radius=CARD_RADIUS)
            pygame.draw.rect(screen, BLACK, flip_rect, 4, border_radius=CARD_RADIUS)

            if flip_scale > 0.1:  # Only draw text if somewhat flipped
                # Rank
                rank_text = FONT_MED.render(str(self.rank), True, BLACK)
                screen.blit(rank_text, (x + 10, y + 10))

                # Suit
                suit_text = FONT_LARGE.render(self.suit, True, self.suit_color)
                suit_rect = suit_text.get_rect(center=(self.rect.centerx, self.rect.centery))
                screen.blit(suit_text, suit_rect)

        else:
            # Back: pattern or symbol
            pygame.draw.rect(screen, DARK_RED, self.rect, border_radius=CARD_RADIUS)
            pygame.draw.rect(screen, BLACK, self.rect, 4, border_radius=CARD_RADIUS)
            # CCRU symbol placeholder
            back_text = FONT_SMALL.render("CCRU", True, GOLD)
            screen.blit(back_text, (x + 20, y + 60))

    def update_flip(self, dt):
        if self.flip_progress < 1.0:
            self.flip_progress += dt * 2  # flip speed
            if self.flip_progress >= 1.0:
                self.flip_progress = 1.0
                self.face_up = True

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

class DecadenceGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Decadence: CCRU Lemurian Sorcery")
        self.clock = pygame.time.Clock()
        self.state = "menu"  # menu, playing, round_end, aeon_end
        self.deck = []
        self.set1 = [None] * 5
        self.set2 = [None] * 5
        self.unpaired = [True] * 5
        self.current_flip_idx = -1  # which set2 card is flipping
        self.bonus = 0
        self.cumulative = 0
        self.round_num = 1
        self.possibles = []
        self.selected_demon = None
        self.reset_deck()

    def reset_deck(self):
        self.deck = []
        ranks = list(range(1, 10))
        suits = list(range(4))
        for rank in ranks:
            for suit in suits:
                self.deck.append(Card(rank, suit))
        random.shuffle(self.deck)

    def deal_round(self):
        if len(self.deck) < 10:
            self.state = "aeon_end"
            return
        self.set1 = [self.deck.pop() for _ in range(5)]
        self.set2 = [self.deck.pop() for _ in range(5)]
        for card in self.set1:
            card.face_up = True
            card.flip_progress = 1.0
        self.unpaired = [True] * 5
        self.bonus = 0
        self.current_flip_idx = 0
        self.possibles = []

    def start_round(self):
        self.deal_round()
        self.state = "playing"

    def flip_next(self):
        if self.current_flip_idx < 5:
            self.set2[self.current_flip_idx].face_up = False  # reset for anim
            self.set2[self.current_flip_idx].flip_progress = 0.0
            self.update_possibles()
            self.current_flip_idx += 1

    def update_possibles(self):
        flipped = self.set2[self.current_flip_idx - 1]
        self.possibles = []
        for i in range(5):
            if self.unpaired[i] and (flipped.rank + self.set1[i].rank == 10):
                self.possibles.append(i)

    def pair_card(self, idx):
        if idx in self.possibles:
            self.unpaired[idx] = False
            flipped_rank = self.set2[self.current_flip_idx - 1].rank
            pair_key = tuple(sorted([flipped_rank, self.set1[idx].rank]))
            pair_bonus = pair_scores.get(pair_key, 0)
            self.bonus += pair_bonus
            self.possibles = []  # clear
            return True
        return False

    def end_round(self):
        penalty = sum(-self.set1[i].rank for i in range(5) if self.unpaired[i])
        self.round_score = self.bonus + penalty
        self.cumulative += self.round_score
        if self.cumulative > 0 and len(self.deck) >= 10:
            self.state = "round_end_continue"
        else:
            self.state = "aeon_end"

    def draw_menu(self):
        self.screen.fill(ABYSS_BLUE)
        title = FONT_LARGE.render("DECADENCE", True, CRIMSON)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 200))
        self.screen.blit(title, title_rect)

        play_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, 400, 300, 80)
        pygame.draw.rect(self.screen, GOLD, play_btn, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, play_btn, 4, border_radius=10)
        play_text = FONT_MED.render("Play Solitaire", True, BLACK)
        play_rect = play_text.get_rect(center=play_btn.center)
        self.screen.blit(play_text, play_rect)

        # Quit btn
        quit_btn = pygame.Rect(SCREEN_WIDTH//2 - 150, 500, 300, 80)
        pygame.draw.rect(self.screen, DARK_RED, quit_btn, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, quit_btn, 4, border_radius=10)
        quit_text = FONT_MED.render("Quit", True, WHITE)
        quit_rect = quit_text.get_rect(center=quit_btn.center)
        self.screen.blit(quit_text, quit_rect)

        return play_btn, quit_btn

    def draw_playing(self):
        self.screen.fill(BLACK)

        # Title
        round_text = FONT_SMALL.render(f"Round {self.round_num} - Aeon: {self.cumulative:+}", True, GOLD)
        self.screen.blit(round_text, (20, 20))

        # Set-1 Cross
        for i, (pos, label) in enumerate(zip(CROSS_POS, POSITION_LABELS)):
            self.set1[i].draw(self.screen, pos, i in self.possibles)
            # Label
            label_surf = FONT_TINY.render(label, True, WHITE)
            self.screen.blit(label_surf, (pos[0] - 100, pos[1] - 30))

        # Set-2 below
        for i, pos in enumerate(SET2_POS):
            card = self.set2[i]
            highlight = (i == self.current_flip_idx - 1)
            card.draw(self.screen, pos, highlight)

        # Instructions
        if self.possibles:
            instr = FONT_SMALL.render("Click a highlighted card to pair", True, GOLD)
        else:
            instr = FONT_SMALL.render("No pairs possible. Next flip auto.", True, GOLD)
        self.screen.blit(instr, (20, SCREEN_HEIGHT - 60))

        # Flip button if needed
        if self.current_flip_idx < 5 and len(self.possibles) == 0:
            flip_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 100, 200, 50)
            pygame.draw.rect(self.screen, CRIMSON, flip_btn, border_radius=10)
            flip_text = FONT_SMALL.render("Next Flip", True, WHITE)
            self.screen.blit(flip_text, (flip_btn.x + 40, flip_btn.y + 10))
            return flip_btn

    def draw_round_end(self):
        self.screen.fill(ABYSS_BLUE)
        score_text = FONT_MED.render(f"Round Score: {self.round_score:+}", True, GOLD)
        self.screen.blit(score_text, (SCREEN_WIDTH//2 - 150, 300))
        cont_text = FONT_SMALL.render("Click to Continue", True, WHITE)
        self.screen.blit(cont_text, (SCREEN_WIDTH//2 - 100, 400))

    def draw_aeon_end(self):
        self.screen.fill(BLACK)
        if self.cumulative > 0:
            title = FONT_LARGE.render("POSITIVE AEON", True, GOLD)
            desc = FONT_MED.render("Angelic vector open. Hyperstition flows.", True, WHITE)
        else:
            mesh = abs(self.cumulative) if self.cumulative < 0 else 0
            if mesh > 44:
                title = FONT_LARGE.render("BEYOND PANDEMONIUM", True, CRIMSON)
                desc = FONT_MED.render("Gt-45 Cataclysm", True, WHITE)
            else:
                demon = demons[mesh]
                title = FONT_LARGE.render(demon["name"].upper(), True, CRIMSON)
                type_text = FONT_MED.render(demon["type"], True, GOLD)
                attr_text = FONT_SMALL.render(demon["attributes"], True, WHITE)

                self.screen.blit(title, (SCREEN_WIDTH//2 - 300, 200))
                self.screen.blit(type_text, (SCREEN_WIDTH//2 - 250, 300))
                attr_rect = attr_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
                self.screen.blit(attr_text, attr_rect)
                desc = None

        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        self.screen.blit(title, title_rect)
        if desc:
            desc_rect = desc.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(desc, desc_rect)

        restart_text = FONT_SMALL.render("Click to Play Again", True, GOLD)
        self.screen.blit(restart_text, (SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT - 50))

    def handle_click(self, pos):
        if self.state == "menu":
            pass  # handled in draw
        elif self.state == "playing":
            for i in self.possibles:
                card_rect = pygame.Rect(CROSS_POS[i][0], CROSS_POS[i][1], CARD_WIDTH, CARD_HEIGHT)
                if card_rect.collidepoint(pos):
                    if self.pair_card(i):
                        if self.current_flip_idx == 5:
                            self.end_round()
                    return
        elif self.state == "round_end_continue" or self.state == "aeon_end":
            self.state = "menu"  # restart

    def update(self, dt):
        if self.state == "playing":
            if self.current_flip_idx < 5:
                self.set2[self.current_flip_idx].update_flip(dt)
                if self.set2[self.current_flip_idx].flip_progress >= 1.0 and len(self.possibles) == 0:
                    # Auto next if no pairs
                    pygame.time.wait(500)
                    self.flip_next()

            if self.current_flip_idx >= 5:
                self.end_round()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000.0
            mouse_pos = pygame.mouse.get_pos()
            clicked = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                    self.handle_click(mouse_pos)

            self.update(dt)

            if self.state == "menu":
                play_btn, quit_btn = self.draw_menu()
                if clicked:
                    if play_btn.collidepoint(mouse_pos):
                        self.round_num = 1
                        self.cumulative = 0
                        self.reset_deck()
                        self.start_round()
                    elif quit_btn.collidepoint(mouse_pos):
                        running = False
            elif self.state == "playing":
                flip_btn = self.draw_playing()
                if clicked and flip_btn and flip_btn.collidepoint(mouse_pos):
                    self.flip_next()
            elif self.state == "round_end_continue":
                self.draw_round_end()
                if clicked:
                    self.round_num += 1
                    self.start_round()
            elif self.state == "aeon_end":
                self.draw_aeon_end()

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = DecadenceGame()
    game.run()







