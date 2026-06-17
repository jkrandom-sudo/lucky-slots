# Lucky Slots / 幸运老虎机

A bilingual console slot-machine game written with the Python standard library.

一个使用 Python 标准库编写的双语控制台老虎机小游戏。

## Features / 功能

- Spin three reels with five symbols.
- Three-of-a-kind pays big, pairs pay double, and cherry refunds the bet.
- Choose custom bets or use the difficulty default.
- Three difficulty levels with different coin counts, spins, bets, and score bonuses.
- Bilingual UI: English and Chinese.
- Persistent JSON settings and top scores.
- Optional terminal bell sound with adjustable volume.
- Automated tests for core logic, persistence modules, sound, and menu gameplay.

## Requirements / 环境要求

- Python 3.9+
- No third-party dependencies.

## Run / 启动

```bash
python3 game.py
```

## Test / 测试

```bash
python3 -m py_compile game.py lucky_slots.py i18n.py settings.py score.py sound.py
python3 tests/run_tests.py
```

## How to Play / 玩法

1. Choose Play from the main menu.
2. Enter `spin` to use the default bet, or enter a positive number as the bet.
3. Watch the three reels and collect payouts.
4. The game ends when spins or coins run out.
5. Profit becomes your score.
6. Type `q` to quit the current game.

## Difficulty / 难度

| Difficulty | Coins | Spins | Default bet | Score bonus |
| --- | ---: | ---: | ---: | ---: |
| easy | 30 | 10 | 2 | 1x |
| normal | 40 | 12 | 3 | 2x |
| hard | 50 | 15 | 5 | 3x |

## Files / 文件

- `game.py` — console UI and menus.
- `lucky_slots.py` — core reels, payout, betting, scoring, and rating logic.
- `i18n.py` — bilingual strings.
- `settings.py` — JSON settings persistence.
- `score.py` — JSON score persistence.
- `sound.py` — terminal bell sound helper.
- `tests/` — automated unit tests.
