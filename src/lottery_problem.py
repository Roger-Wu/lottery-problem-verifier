import math


class LotteryProblem:
    """
    Represents a (n, k, p, t) lottery problem and performs basic calculations.

    n = total_num_count
    k = num_count_in_ticket
    p = num_count_in_draw
    t = min_matched_num_count
        To win a prize, at least `t` numbers on a ticket must match the numbers drawn.
    """

    def __init__(
        self,
        total_num_count: int,
        num_count_in_ticket: int,
        num_count_in_draw: int,
        min_matched_num_count: int,
    ) -> None:
        """
        Initializes a LotteryProblem object.

        :param total_num_count: Total number of possible numbers.
        :param num_count_in_draw: Number of numbers drawn in each draw.
        :param num_count_in_ticket: Number of numbers on a ticket.
        :param min_matched_num_count: Minimum number of matching numbers to win.
        """
        self._validate_inputs(total_num_count, num_count_in_ticket, num_count_in_draw, min_matched_num_count)

        self.total_num_count: int = total_num_count
        self.num_count_in_ticket: int = num_count_in_ticket
        self.num_count_in_draw: int = num_count_in_draw
        self.min_matched_num_count: int = min_matched_num_count

        self.total_ticket_count: int = math.comb(
            self.total_num_count, self.num_count_in_ticket
        )
        self.total_draw_count: int = math.comb(
            self.total_num_count, self.num_count_in_draw
        )

    def _validate_inputs(
        self,
        total_num_count: int,
        num_count_in_ticket: int,
        num_count_in_draw: int,
        min_matched_num_count: int,
    ):
        """Validates the input parameters."""
        if not (
            total_num_count >= num_count_in_ticket >= min_matched_num_count
            and total_num_count >= num_count_in_draw >= min_matched_num_count
        ):
            raise ValueError("Invalid input values")

    @property
    def covered_draw_count_per_ticket(self) -> int:
        max_matched_num_count = min(self.num_count_in_draw, self.num_count_in_ticket)
        return sum(
            self._count_draws_with_n_matches(matched_num_count)
            for matched_num_count in range(
                self.min_matched_num_count, max_matched_num_count + 1
            )
        )

    def _count_draws_with_n_matches(self, matched_num_count):
        """
        Calculate how many draws have `matched_num_count` numbers in common with a ticket.
        """
        num_count_not_in_ticket = self.total_num_count - self.num_count_in_ticket
        matched_combination_count = math.comb(
            self.num_count_in_ticket, matched_num_count
        )
        unmatched_combination_count = math.comb(
            num_count_not_in_ticket, self.num_count_in_draw - matched_num_count
        )
        return matched_combination_count * unmatched_combination_count

    @property
    def solution_size_lower_bound(self) -> float:
        return self.total_draw_count / self.covered_draw_count_per_ticket


def generate_problem_signature(lottery: LotteryProblem) -> str:
    """Generate a unique signature for the problem based on its parameters."""
    return ",".join(
        map(
            str,
            [
                lottery.total_num_count,
                lottery.num_count_in_ticket,
                lottery.num_count_in_draw,
                lottery.min_matched_num_count,
            ],
        )
    )

def print_lottery_problem_info(lottery: LotteryProblem):
    """Prints a summary of the lottery problem."""
    print(f"A lottery problem with")
    print(f"    {lottery.total_num_count} numbers,")
    print(f"    {lottery.num_count_in_ticket} numbers in a ticket,")
    print(f"    {lottery.num_count_in_draw} numbers in a draw,")
    print(
        f"    {lottery.min_matched_num_count} or more numbers matched to win a prize."
    )
    print(f"{lottery.total_draw_count:,} draws in total")
    print(f"{lottery.total_ticket_count:,} tickets in total")
    print(f"{lottery.covered_draw_count_per_ticket:,} draws covered by each ticket")
    print(f"{lottery.covered_draw_count_per_ticket * lottery.total_ticket_count:,} entries of cached covered draws")
    print(f"solution size lower bound: {lottery.solution_size_lower_bound}")
