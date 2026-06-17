import unittest

import lucky_slots as core


class FixedRng:
    def __init__(self, values):
        self.values = list(values)

    def choice(self, seq):
        return self.values.pop(0)


class TestCore(unittest.TestCase):
    def test_config_fallback(self):
        self.assertEqual(core.config("bad"), core.config("normal"))

    def test_new_state(self):
        state = core.new_state("easy")
        self.assertEqual(state["coins"], 30)
        self.assertEqual(state["spins_left"], 10)

    def test_spin(self):
        self.assertEqual(core.spin(FixedRng(["CHERRY", "BELL", "SEVEN"])), ("CHERRY", "BELL", "SEVEN"))

    def test_payout(self):
        self.assertEqual(core.payout(("SEVEN", "SEVEN", "SEVEN"), 2), 20)
        self.assertEqual(core.payout(("BELL", "BELL", "BELL"), 2), 12)
        self.assertEqual(core.payout(("BELL", "BELL", "STAR"), 2), 4)
        self.assertEqual(core.payout(("CHERRY", "BELL", "STAR"), 2), 2)
        self.assertEqual(core.payout(("LEMON", "BELL", "STAR"), 2), 0)

    def test_bet_and_play_spin(self):
        state = core.new_state("easy")
        self.assertTrue(core.can_bet(state, 2))
        self.assertFalse(core.can_bet(state, 99))
        result = core.play_spin(state, 2, FixedRng(["SEVEN", "SEVEN", "SEVEN"]))
        self.assertEqual(result[1], 20)
        self.assertEqual(state["coins"], 48)
        self.assertEqual(state["spins_left"], 9)
        self.assertIsNone(core.play_spin(state, 99))

    def test_parse_bet(self):
        self.assertEqual(core.parse_bet("", 3), 3)
        self.assertEqual(core.parse_bet("spin", 3), 3)
        self.assertEqual(core.parse_bet("5", 3), 5)
        self.assertIsNone(core.parse_bet("0", 3))
        self.assertIsNone(core.parse_bet("x", 3))

    def test_text_score_rating(self):
        self.assertEqual(core.reels_text(("A", "B", "C")), "A | B | C")
        state = core.new_state("easy")
        state["coins"] = 45
        self.assertEqual(core.score_for(state), 15)
        self.assertEqual(core.final_rating(100), "jackpot")
        self.assertEqual(core.final_rating(30), "winner")
        self.assertEqual(core.final_rating(1), "lucky")
        self.assertEqual(core.final_rating(0), "bust")


if __name__ == "__main__":
    unittest.main()
