import sys
sys.path.append('src')
sys.path.append('src/int_set')
from lottery_problem_with_cache import LotteryProblemWithCache
from lottery_problem_verifier import LotteryProblemVerifier


if __name__ == "__main__":
    problem_tuple = (39, 5, 5, 2)
    ticket_combos = [(0, 1, 2, 3, 4), (0, 1, 2, 5, 6), (0, 1, 7, 8, 9), (2, 6, 7, 8, 9), (3, 4, 5, 6, 7), (3, 4, 5, 8, 9), (10, 11, 12, 13, 14), (10, 11, 12, 15, 16), (10, 11, 17, 18, 19), (12, 16, 17, 18, 19), (13, 14, 15, 16, 17), (13, 14, 15, 18, 19), (20, 21, 22, 23, 24), (20, 21, 22, 25, 26), (20, 21, 27, 28, 29), (22, 26, 27, 28, 29), (23, 24, 25, 26, 27), (23, 24, 25, 28, 29), (30, 31, 32, 33, 34), (30, 35, 36, 37, 38), (31, 32, 33, 35, 36), (31, 32, 33, 37, 38), (34, 35, 36, 37, 38)]

    print(f"Verifying coverage of {len(ticket_combos)} tickets of lottery {problem_tuple}...")

    lpc = LotteryProblemWithCache(*problem_tuple)
    ticket_indices = lpc.get_indices_by_tickets(
        [tuple(combo) for combo in ticket_combos]
    )

    verifier = LotteryProblemVerifier(lpc)
    verifier.verify_coverage(ticket_indices)
