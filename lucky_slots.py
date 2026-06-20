"""Core logic for Lucky Slots."""
import random

SYMBOLS = ("CHERRY", "LEMON", "BELL", "STAR", "SEVEN")
DIFFICULTY_CONFIG = {
    "easy": {"coins": 30, "spins": 10, "bet": 2, "bonus": 1},
    "normal": {"coins": 40, "spins": 12, "bet": 3, "bonus": 2},
    "hard": {"coins": 50, "spins": 15, "bet": 5, "bonus": 3},
}


def config(difficulty):
    return DIFFICULTY_CONFIG.get(difficulty, DIFFICULTY_CONFIG["normal"])


def new_state(difficulty):
    cfg = config(difficulty)
    return {"coins": cfg["coins"], "spins_left": cfg["spins"], "difficulty": difficulty, "last": ()}


def spin(rng=None):
    rng = rng or random
    return tuple(rng.choice(SYMBOLS) for _ in range(3))


def payout(reels, bet):
    unique = len(set(reels))
    if unique == 1:
        return bet * (10 if reels[0] == "SEVEN" else 6)
    if unique == 2:
        return bet * 2
    if "CHERRY" in reels:
        return bet
    return 0


def can_bet(state, bet):
    if not isinstance(bet, int) or bet <= 0:
        return False
    if bet > state["coins"]:
        return False
    if state["spins_left"] <= 0:
        return False
    return True


def validate_bet(state, bet):
    """Returns reason string if invalid, True if valid."""
    if not isinstance(bet, int) or bet <= 0:
        return "invalid"
    if bet > state["coins"]:
        return "too_high"
    if state["spins_left"] <= 0:
        return "no_spins"
    return True


def play_spin(state, bet, rng=None):
    valid = validate_bet(state, bet)
    if valid is not True:
        return None
    state["coins"] -= bet
    reels = spin(rng)
    win = payout(reels, bet)
    state["coins"] += win
    state["spins_left"] -= 1
    state["last"] = reels
    return reels, win


def parse_bet(text, default_bet):
    text = text.strip().lower()
    if text in ("", "spin", "s"):
        return default_bet
    if not text.isdigit():
        return None
    value = int(text)
    return value if value > 0 else None


def reels_text(reels):
    return " | ".join(reels) if reels else "-"


def score_for(state):
    start = config(state["difficulty"])["coins"]
    return max(0, state["coins"] - start) * config(state["difficulty"])["bonus"]


def final_rating(score):
    if score >= 100:
        return "jackpot"
    if score >= 30:
        return "winner"
    if score > 0:
        return "lucky"
    return "bust"
