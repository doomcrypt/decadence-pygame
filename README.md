# Decadence

**Lemurian Time-Sorcery Engine – Pandemonium Matrix Solitaire**  
A ritual card game built in Pygame, channeling the CCRU's Decadology and abyssal numerics.

Two sets of five cards are drawn across the aeonic cross.  
Pair currents whose ranks sum to 10.  
Syzygetic alignments (1+9, 2+8, 3+7, 4+6) grant bonus vectors.  
Unpaired positions erode your score with penalties.  
When the cumulative aeon collapses to ≤ 0, a demon emerges from the negative Mesh (00–44).

## Gameplay

- **Deck**: 36 cards (ranks 1–9, suits ♣ ♦ ♥ ♠)
- **Layout**: Atlantean Cross (Set-1) + linear Set-2 below
- **Objective**: Survive as many rounds as possible without letting the cumulative score reach zero or below
- **Pairing**: Click a highlighted (gold) Set-1 card to bind it to the current flipped card
- **Bonuses**:

  | Pair | Bonus |
  |------|-------|
  | 1+9  | +8    |
  | 2+8  | +6    |
  | 3+7  | +4    |
  | 4+6  | +2    |
  | 5+5  | 0     |

- **Collapse**: Negative cumulative score indexes a Pandemonium demon

## Installation & Run

Requires **Python 3.8+** and **Pygame**.

```bash
# Clone the repo
git clone https://github.com/doomcrypt/decadence-pygame.git
cd decadence-pygame
python main.py

# Install dependencies (only pygame needed)
pip install -r requirements.txt

# Run the ritual
python main.py
# or: python decadence.py (depending on what you named the entry file)
