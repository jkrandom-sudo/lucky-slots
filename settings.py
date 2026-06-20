"""Settings persistence."""
import json
from pathlib import Path

DEFAULT_PATH = Path.home() / ".lucky_slots_settings.json"
DIFFICULTIES = ("easy", "normal", "hard")
LANG_ALIASES = {"cn": "zh", "zh-CN": "zh", "zh-TW": "zh", "en-US": "en", "en-GB": "en"}
DEFAULTS = {"lang": "zh", "sound": True, "volume": 1, "difficulty": "normal"}


def load(path=None):
    if path is None:
        path = DEFAULT_PATH
    settings = DEFAULTS.copy()
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            settings.update(data)
    except FileNotFoundError:
        pass
    lang = settings.get("lang", DEFAULTS["lang"])
    settings["lang"] = LANG_ALIASES.get(lang, lang)
    if settings["lang"] not in ("zh", "en"):
        settings["lang"] = DEFAULTS["lang"]
    if not isinstance(settings["sound"], bool):
        settings["sound"] = DEFAULTS["sound"]
    if settings["volume"] not in (0, 1, 2, 3):
        settings["volume"] = DEFAULTS["volume"]
    if settings["difficulty"] not in DIFFICULTIES:
        settings["difficulty"] = DEFAULTS["difficulty"]
    return settings


def save(settings, path=None):
    if path is None:
        path = DEFAULT_PATH
    with open(path, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def cycle_lang(settings):
    settings["lang"] = "en" if settings.get("lang") == "zh" else "zh"


def toggle_sound(settings):
    settings["sound"] = not settings.get("sound", True)


def cycle_volume(settings):
    settings["volume"] = (settings.get("volume", 1) + 1) % 4


def cycle_difficulty(settings):
    current = settings.get("difficulty", "normal")
    idx = DIFFICULTIES.index(current) if current in DIFFICULTIES else 1
    settings["difficulty"] = DIFFICULTIES[(idx + 1) % len(DIFFICULTIES)]
