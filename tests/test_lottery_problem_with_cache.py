import sys
sys.path.append('src')
sys.path.append('src/int_set')
import unittest
from lottery_problem_with_cache import LotteryProblemWithCache


class TestLotteryProblemWithCache(unittest.TestCase):
    def test_init(self):
        lp = LotteryProblemWithCache(
            18, 6, 4, 3,
            cache_all_ticket_combos = True,
            cache_all_draw_combos = True,
        )
        self.assertEqual(len(lp.all_ticket_combos), lp.total_ticket_count)
        self.assertEqual(len(lp.all_draw_combos), lp.total_draw_count)

    def test_cache_covered_draws(self):
        lp = LotteryProblemWithCache(
            18, 6, 4, 3,
            cache_all_ticket_combos = True,
            cache_all_draw_combos = True,
            cache_ticket_to_index = True,
            cache_draw_to_index = True,
            cache_covered_draws = True,
        )
        lp.cache_covered_draws()
        self.assertTrue(lp.are_covered_draws_cached)
        self.assertEqual(
            len(lp.get_covered_draws(0)),
            lp.covered_draw_count_per_ticket
        )

    def test_get_combination_index(self):
        total_num_count = 18
        num_count_in_ticket = 6
        num_count_in_draw = 4
        min_matched_num_count = 3

        lp = LotteryProblemWithCache(
            total_num_count=total_num_count,
            num_count_in_ticket=num_count_in_ticket,
            num_count_in_draw=num_count_in_draw,
            min_matched_num_count=min_matched_num_count,
            cache_all_ticket_combos = True,
            cache_all_draw_combos = True,
            cache_ticket_to_index = True,
            cache_draw_to_index = True,
            cache_covered_draws = False,
        )

        ticket_to_index = {ticket: i for i, ticket in enumerate(lp.all_ticket_combos)}
        draw_to_index = {draw: i for i, draw in enumerate(lp.all_draw_combos)}

        self._test_ticket_index((0, 1, 2, 3, 4, 5), ticket_to_index, lp)
        self._test_ticket_index((3, 4, 8, 10, 11, 16), ticket_to_index, lp)
        self._test_ticket_index((12, 13, 14, 15, 16, 17), ticket_to_index, lp)

        self._test_draw_index((0, 1, 2, 3), draw_to_index, lp)
        self._test_draw_index((1, 2, 13, 17), draw_to_index, lp)
        self._test_draw_index((14, 15, 16, 17), draw_to_index, lp)

    def _test_ticket_index(self, ticket, ticket_to_index, lp):
        expected_index = ticket_to_index[ticket]
        calculated_index = lp.get_ticket_index(ticket)
        self.assertEqual(calculated_index, expected_index)

    def _test_draw_index(self, draw, draw_to_index, lp):
        expected_index = draw_to_index[draw]
        calculated_index = lp.get_draw_index(draw)
        self.assertEqual(calculated_index, expected_index)
