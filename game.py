"""Console game for Lucky Slots."""
import lucky_slots as core
import score as score_mod
import settings as settings_mod
from i18n import t
from sound import Sound


class QuitGame(Exception):
    pass


def _print(text=""):
    print(text)


def show_header(settings):
    _print("=" * 32)
    _print(t(settings["lang"], "title"))
    _print("=" * 32)


def show_help(settings):
    show_header(settings)
    _print(t(settings["lang"], "help_title"))
    _print(t(settings["lang"], "help_text"))
    input(t(settings["lang"], "press_enter"))


def show_scores(settings):
    show_header(settings)
    _print(t(settings["lang"], "scores"))
    scores = score_mod.load()
    if not scores:
        _print(t(settings["lang"], "no_scores"))
    for idx, item in enumerate(scores, 1):
        _print(f"{idx}. {item.get('name', '?')} {item.get('score', 0)} ({item.get('difficulty', '?')})")
    input(t(settings["lang"], "press_enter"))


def settings_menu(settings):
    while True:
        show_header(settings)
        _print(t(settings["lang"], "settings"))
        _print(f"{t(settings['lang'], 'lang')}: {settings['lang']}")
        _print(f"{t(settings['lang'], 'sound')}: {t(settings['lang'], 'on' if settings['sound'] else 'off')}")
        _print(f"{t(settings['lang'], 'volume')}: {settings['volume']}")
        _print(f"{t(settings['lang'], 'difficulty')}: {settings['difficulty']}")
        choice = input(t(settings["lang"], "settings_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "1":
            settings_mod.cycle_lang(settings)
        elif choice == "2":
            settings_mod.toggle_sound(settings)
        elif choice == "3":
            settings_mod.cycle_volume(settings)
        elif choice == "4":
            settings_mod.cycle_difficulty(settings)
        elif choice == "b":
            settings_mod.save(settings)
            return
        else:
            _print(t(settings["lang"], "unknown"))


def play_round(settings):
    lang = settings["lang"]
    difficulty = settings["difficulty"]
    cfg = core.config(difficulty)
    snd = Sound(settings["sound"], settings["volume"])
    state = core.new_state(difficulty)

    show_header(settings)
    while state["spins_left"] > 0 and state["coins"] > 0:
        _print(t(lang, "status", coins=state["coins"], spins=state["spins_left"], bet=cfg["bet"]))
        text = input(t(lang, "prompt")).strip().lower()
        if text == "q":
            raise QuitGame()
        bet = core.parse_bet(text, cfg["bet"])
        result = core.play_spin(state, bet)
        if result is None:
            _print(t(lang, "invalid"))
            snd.incorrect()
            continue
        reels, win = result
        _print(t(lang, "result", reels=core.reels_text(reels), win=win))
        if win:
            snd.correct()
        else:
            snd.incorrect()

    score = core.score_for(state)
    rating_key = core.final_rating(score)
    _print(t(lang, "finished", coins=state["coins"], score=score, rating=t(lang, rating_key)))
    if score > 0:
        snd.win()
    else:
        snd.lose()
    return score


def main_menu():
    settings = settings_mod.load()
    while True:
        show_header(settings)
        choice = input(t(settings["lang"], "main_menu") + "\n" + t(settings["lang"], "choice")).strip().lower()
        if choice == "p":
            try:
                result = play_round(settings)
            except QuitGame:
                result = 0
            if result > 0:
                name = input(t(settings["lang"], "name_prompt")).strip()
                if name:
                    score_mod.add(name, result, settings["difficulty"])
                    _print(t(settings["lang"], "saved"))
                else:
                    _print(t(settings["lang"], "not_saved"))
            input(t(settings["lang"], "press_enter"))
        elif choice == "h":
            show_help(settings)
        elif choice == "s":
            settings_menu(settings)
        elif choice == "c":
            show_scores(settings)
        elif choice == "q":
            _print(t(settings["lang"], "bye"))
            return
        else:
            _print(t(settings["lang"], "unknown"))


if __name__ == "__main__":
    main_menu()
