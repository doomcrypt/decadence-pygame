import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1400
SCREEN_HEIGHT = 900
FPS = 60

# Colors (occult theme: black void, crimson, gold, abyssal blue)
BLACK = (0, 0, 0)
CRIMSON = (139, 0, 0)
GOLD = (255, 215, 0)
WHITE = (255, 255, 255)
DARK_RED = (100, 0, 0)
ABYSS_BLUE = (10, 20, 40)
SHADOW = (20, 20, 20)
GLOW = (255, 100, 100, 128)  # semi-transparent for highlights

CARD_WIDTH = 100
CARD_HEIGHT = 150
CARD_RADIUS = 10  # rounded corners

# Fonts
FONT_LARGE = pygame.font.Font(None, 72)
FONT_MED = pygame.font.Font(None, 48)
FONT_SMALL = pygame.font.Font(None, 32)
FONT_TINY = pygame.font.Font(None, 24)

# Suits unicode
SUITS = ['♣', '♦', '♥', '♠']
SUIT_COLORS = {0: BLACK, 1: CRIMSON, 2: CRIMSON, 3: BLACK}  # Clubs/Spades black, Diamonds/Hearts red

# Demons dict (same as before)
demons = {
    0: {"name": "Lurgo (Legba)", "type": "Amphidemon of Openings", "attributes": "Terminal Initiator, Door of Doors, Spinal-voyage rites."},
    1: {"name": "Duoddod", "type": "Amphidemon of Abstract Addiction", "attributes": "Duplicitous Redoubler, Pineal-regression, digital exactitude."},
    2: {"name": "Doogu (The Blob)", "type": "Cyclic Chronodemon of Splitting-Waters", "attributes": "Original-Schism, primordial breath, ambivalent capture."},
    3: {"name": "Ixix (Yix)", "type": "Chaotic Xenodemon of Cosmic Indifference", "attributes": "Abductor, occult terrestrial history."},
    4: {"name": "Ixigool (Djinn of the Magi)", "type": "Amphidemon of Tridentity", "attributes": "Over-Ghoul, unimpeded ascent, ultimate implications."},
    5: {"name": "Ixidod (King Sid)", "type": "Amphidemon of Escape-velocity", "attributes": "Zombie-Maker, crises through excess, illusion of progress."},
    6: {"name": "Krako (Kru, Karak-oa)", "type": "Amphidemon of Burning-Hail", "attributes": "Croaking Curse, subsidence, heaviness of fatality."},
    7: {"name": "Sukugool (Old Skug)", "type": "Cyclic Chronodemon of Deluge and Implosion", "attributes": "Sucking-Ghoul, cycle of creation/destruction, submersion."},
    8: {"name": "Skoodu (Li'l Scud)", "type": "Cyclic Chronodemon of Switch-Crazes", "attributes": "Fashioner, historical time, passage through the deep."},
    9: {"name": "Skarkix (Sharky, Scar-head)", "type": "Amphidemon of Anti-evolution", "attributes": "Buzz-Cutter, hermetic abbreviations, apocalyptic rapture."},
    10: {"name": "Tokhatto (Old Toker, Top Cat)", "type": "Amphidemon of Talismania", "attributes": "Decimal Camouflage, number as destiny, Angel of the Cards."},
    11: {"name": "Tukkamu", "type": "Cyclic Chronodemon of Pathogenesis", "attributes": "Occulturation, optimal maturation, rapid deterioration."},
    12: {"name": "Kuttadid (Kitty)", "type": "Cyclic Chronodemon of Precarious States", "attributes": "Ticking Machines, maintaining balance, exhaustive vigilance."},
    13: {"name": "Tikkitix (Tickler)", "type": "Amphidemon of Vortical Delirium", "attributes": "Clicking Menaces, swirl-patterns, mysterious disappearances."},
    14: {"name": "Katak", "type": "Syzygetic Chronodemon of Cataclysmic Convergence", "attributes": "Desolator, tail-chasing, panic and religious fervor."},
    15: {"name": "Tchu (Tchanul)", "type": "Chaotic Xenodemon of Ultimate Outsideness", "attributes": "Source of Subnothingness, cosmic deletions."},
    16: {"name": "Djungo", "type": "Amphidemon of Subtle Involvements", "attributes": "Infiltrator, turbular fluids, surreptitious invasions."},
    17: {"name": "Djuddha (Judd Dread)", "type": "Amphidemon of Artificial Turbulence", "attributes": "Decentred Threat, machine-vortex, storm peripheries."},
    18: {"name": "Djynxx (Ching, The Jinn)", "type": "Syzygetic Xenodemon of Time-Lapse", "attributes": "Child Stealer, abstract cyclones, dust spirals."},
    19: {"name": "Tchakki (Chuckles)", "type": "Amphidemon of Combustion", "attributes": "Bag of Tricks, quenching accidents, conflagrations."},
    20: {"name": "Tchattuk (One Eyed Jack, Djatka)", "type": "Amphidemon of Unscreened Matrix", "attributes": "Pseudo-Basis, zero-gravity, cut-outs and UFO cover-ups."},
    21: {"name": "Puppo (The Pup)", "type": "Amphidemon of Larval Regression", "attributes": "Break-Outs, dissolving into slime, chthonic swallowings."},
    22: {"name": "Bubbamu (Bubs)", "type": "Cyclic Chronodemon of Relapse", "attributes": "After Babylon, hypersea, aquassassins."},
    23: {"name": "Oddubb (Odba)", "type": "Syzygetic Chronodemon of Swamp-Labyrinths", "attributes": "Broken Mirror, time loops, glamour."},
    24: {"name": "Pabbakis (Pabz)", "type": "Amphidemon of Crossroads", "attributes": "The Weaver, tangled paths, fateful decisions."},
    25: {"name": "Ababbatok (Abracadabra)", "type": "Cyclic Chronodemon of Suspended Decay", "attributes": "Frankensteinian experimentation, purifications."},
    26: {"name": "Papatakoo (Pataku)", "type": "Cyclic Chronodemon of Calendric Time", "attributes": "Ultimate success, rituals becoming nature."},
    27: {"name": "Bobobja (Bubbles, Beelzebub)", "type": "Amphidemon of Teeming Pestilence", "attributes": "Strange lights in the swamp, swarmachines."},
    28: {"name": "Minommo", "type": "Amphidemon of Submergance", "attributes": "Shamanic voyage, dream sorcery."},
    29: {"name": "Mur Mur (Murrumur, Mu(mu))", "type": "Syzygetic Chronodemon of the Deep Ones", "attributes": "Oceanic sensation, gilled-unlife."},
    30: {"name": "Nammamad", "type": "Cyclic Chronodemon of Subterranean Commerce", "attributes": "Voodoo in cyberspace, emergences."},
    31: {"name": "Mummumix (Mix-Up)", "type": "Amphidemon of Insidious Fog", "attributes": "Ocean storms, diseases from outer-space."},
    32: {"name": "Numko (Old Nuk)", "type": "Cyclic Chronodemon of Autochthony", "attributes": "Necrospeleology, vulcanism."},
    33: {"name": "Muntuk (Manta, Manitou)", "type": "Cyclic Chronodemon of Arid Seabeds", "attributes": "Ancient rivers, cloud-vaults."},
    34: {"name": "Mommoljo (Mama Jo)", "type": "Amphidemon of Xenogenesis", "attributes": "Cosmobacterial exogermination, extraterrestrial residues."},
    35: {"name": "Mombbo", "type": "Cyclic Chronodemon of Hybridity", "attributes": "Ophidian transmutation, surreptitious colonization."},
    36: {"name": "Uttunul", "type": "Syzygetic Xenodemon of Atonality", "attributes": "Crossing the iron-ocean, plutonics."},
    37: {"name": "Tutagool (Yettuk)", "type": "Amphidemon of Punctuality", "attributes": "The dark arts, rusting iron."},
    38: {"name": "Unnunddo (The False Nun)", "type": "Amphidemon of Endless Uncasing", "attributes": "Crypt-traffic, communication-grids."},
    39: {"name": "Ununuttix (Tick-Tock)", "type": "Chaotic Xenodemon of Absolute Coincidence", "attributes": "Numerical connection through absence."},
    40: {"name": "Ununak (Nuke)", "type": "Amphidemon of Convulsions", "attributes": "Secrets of the blacksmiths, subterranean impulses."},
    41: {"name": "Tukutu (Killer-Kate)", "type": "Amphidemon of Death-Strokes", "attributes": "Crash-signals, barkerian scarring."},
    42: {"name": "Unnutchi (Outch, T'ai Chi)", "type": "Chaotic Xenodemon of Coiling Outsideness", "attributes": "Asymmetric zygopoise, cybernetic anomalies."},
    43: {"name": "Nuttubab (Nut-Cracker)", "type": "Amphidemon of Metaloid Unlife", "attributes": "Lunacies, dragon-lines."},
    44: {"name": "Ummnu (Om, Omni, Amen, Omen)", "type": "Amphidemon of Earth-Screams", "attributes": "Crust-friction, anorganic tension."}
}
# Note: In full code, include the entire demons dict as provided earlier.

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

# Positions for Atlantean Cross (adjusted for screen)
CROSS_POS = [
    (650, 200),  # 0: North (Far Future)
    (500, 500),  # 1: West (Destructive)
    (800, 500),  # 2: East (Creative)
    (650, 650),  # 3: South (Deep Past)
    (650, 800)   # 4: Memories & Dreams (below South)
]

SET2_POS = [
    (200, 750),
    (350, 750),
    (950, 750),
    (1100, 750),
    (725, 750)  # center for last?
]

POSITION_LABELS = [
    "North: Far Future",
    "West: Destructive Influences",
    "East: Creative Influences",
    "South: Deep Past",
    "Memories & Dreams"
]

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
            global pair_scores
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

# Pair scores global
pair_scores = {
    (1,9): 8, (9,1): 8,
    (2,8): 6, (8,2): 6,
    (3,7): 4, (7,3): 4,
    (4,6): 2, (6,4): 2,
    (5,5): 0
}

if __name__ == "__main__":
    game = DecadenceGame()
    game.run()
