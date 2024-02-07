from typing import List, Iterable
from itertools import combinations
from lottery_problem import LotteryProblem
from lottery_data_types import TicketComboType, TicketIndexType, DrawComboType, DrawIndexType, DrawSetType
from combination_index_utils import calculate_combination_index, generate_combination_by_index
from int_set.native_int_set import NativeIntSet
# from int_set.numpy_int_set import NumpyIntSet


# TODO: cache_covered_draws after initial ticket set is given. to reduce memory usage
class LotteryProblemWithCache(LotteryProblem):
    """
    This class caches data like all the tickets, all the draws, all the draws covered by each ticket, etc.

    Optional caches and their use cases:
    * self.cache_ticket_to_index()
        * When searching for solutions, we may generate unique ticket combos and
          get ticket index from it.
    * self.cache_draw_to_index()
        * When cache_covered_draws, we generate draws and get the indices of them.
    * self.cache_covered_draws()
        * When searching for solutions, we get covered draws of tickets frequently.
        * This may use a lot of spaces.
    """

    # TODO: can choose to cache all_tickets and all_draws
    def __init__(
        self,
        total_num_count: int,
        num_count_in_ticket: int,
        num_count_in_draw: int,
        min_matched_num_count: int,
        which_int_set: str="native",
        cache_all_ticket_combos: bool = False,
        cache_all_draw_combos: bool = False,
        cache_ticket_to_index: bool = False,
        cache_draw_to_index: bool = False,
        cache_covered_draws: bool = False,
    ):
        super().__init__(
            total_num_count,
            num_count_in_ticket,
            num_count_in_draw,
            min_matched_num_count,
        )

        if which_int_set == "native":
            self.IntSet = NativeIntSet
        # elif which_int_set == "numpy":
        #     self.IntSet = NumpyIntSet
        else:
            raise ValueError(f"unexpected value of which_int_set {which_int_set}")

        self.all_ticket_combos = None
        self.all_draw_combos = None

        self.ticket_to_index = None
        self.draw_to_index = None

        self.are_covered_draws_cached: bool = False
        self.ticket_index_to_covered_draws: List[DrawSetType] = []

        if cache_all_ticket_combos:
            self.cache_all_ticket_combos()

        if cache_all_draw_combos:
            self.cache_all_draw_combos()

        if cache_ticket_to_index:
            self.cache_ticket_to_index()

        if cache_draw_to_index:
            self.cache_draw_to_index()

        if cache_covered_draws:
            self.cache_covered_draws()

    """handle ticket combos"""

    def is_all_ticket_combos_cached(self):
        return self.all_ticket_combos is not None

    def cache_all_ticket_combos(self):
        if not self.is_all_ticket_combos_cached():
            self.all_ticket_combos = list(self.yield_all_ticket_combos())

    def yield_all_ticket_combos(self):
        return combinations(
            range(self.total_num_count),
            self.num_count_in_ticket
        )

    def get_ticket_combo(self, ticket_index: TicketIndexType) -> TicketComboType:
        if self.is_all_ticket_combos_cached():
            return self.all_ticket_combos[ticket_index]
        return generate_combination_by_index(
            ticket_index,
            self.total_num_count,
            self.num_count_in_ticket,
        )

    # old interface
    get_ticket = get_ticket_combo

    def get_tickets_by_indices(
        self, ticket_indices: Iterable[TicketIndexType]
    ) -> List[TicketComboType]:
        return [self.get_ticket_combo(ticket_index) for ticket_index in ticket_indices]

    """handle ticket_to_index"""

    def is_ticket_to_index_cached(self) -> bool:
        return self.ticket_to_index is not None

    def get_ticket_index(self, ticket_combo: TicketComboType) -> TicketIndexType:
        if self.is_ticket_to_index_cached():
            return self.ticket_to_index[ticket_combo]
        return calculate_combination_index(ticket_combo, self.total_num_count)

    def get_indices_by_tickets(
        self, tickets: Iterable[TicketComboType]
    ) -> List[TicketIndexType]:
        return [self.get_ticket_index(ticket_combo) for ticket_combo in tickets]

    def cache_ticket_to_index(self) -> None:
        """
        Call this function to cache ticket_to_index,
        if we need to get indices of tickets frequetly.
        In most cases, it's not necessary to call this functions.
        """
        if not self.is_ticket_to_index_cached():
            self.ticket_to_index = self.generate_ticket_to_index()

    def generate_ticket_to_index(self):
        return {
            ticket: i
            for i, ticket in enumerate(self.yield_all_ticket_combos())
        }

    def delete_cache_ticket_to_index(self) -> None:
        self.ticket_to_index = None

    """handle draws"""

    def is_all_draw_combos_cached(self):
        return self.all_draw_combos is not None

    def cache_all_draw_combos(self):
        if not self.is_all_draw_combos_cached():
            self.all_draw_combos = list(self.yield_all_draw_combos())

    def yield_all_draw_combos(self):
        return combinations(
            range(self.total_num_count),
            self.num_count_in_draw
        )

    def get_draw_combo(self, draw_index: DrawIndexType) -> DrawComboType:
        if self.is_all_draw_combos_cached():
            return self.all_draw_combos[draw_index]
        return generate_combination_by_index(
            draw_index,
            self.total_num_count,
            self.num_count_in_draw,
        )

    # old interface
    get_draw = get_draw_combo

    def get_draw_combos_of_draw_set(self, draws: DrawSetType):
        return [
            self.get_draw_combo(draw_index)
            for draw_index in draws.get_items()
        ]

    def is_draw_to_index_cached(self) -> bool:
        return self.draw_to_index is not None

    def get_draw_index(self, draw_combo: DrawComboType) -> DrawIndexType:
        if self.is_draw_to_index_cached():
            return self.draw_to_index[draw_combo]
        return calculate_combination_index(draw_combo, self.total_num_count)

    def cache_draw_to_index(self) -> None:
        """
        Call this function to cache draw_to_index,
        if we need to get indices of draws frequetly.
        In most cases, it's not necessary to call this functions.
        """
        if not self.is_draw_to_index_cached():
            self.draw_to_index = self.generate_draw_to_index()

    def generate_draw_to_index(self):
        return {draw: i for i, draw in enumerate(self.yield_all_draw_combos())}

    def delete_cache_draw_to_index(self) -> None:
        self.draw_to_index = None

    """functions that handle draw set and covered draws"""

    def delete_cached_covered_draws(self) -> None:
        self.are_covered_draws_cached = False
        self.ticket_index_to_covered_draws = []

    def cache_covered_draws(self, temp_cache_draw_to_index: bool=True) -> None:
        """
        Generate and store the draws covered by each tickets.
        This makes the searching for solutions much faster.

        If the total number of tickets and draws are too large,
        we may not be able to cache all the covered draws for each ticket.
        In that case, this function should not be called.
        """
        if self.are_covered_draws_cached:
            return

        is_draw_to_index_already_cached = self.is_draw_to_index_cached()
        # temporarily cache draw_to_index
        if temp_cache_draw_to_index and not is_draw_to_index_already_cached:
            self.cache_draw_to_index()

        self.ticket_index_to_covered_draws = [
            self.generate_covered_draws(ticket_index)
            for ticket_index in range(self.total_ticket_count)
        ]

        if temp_cache_draw_to_index and not is_draw_to_index_already_cached:
            self.delete_cache_draw_to_index()

        self.are_covered_draws_cached = True

    def generate_covered_draws(self, ticket_index: TicketIndexType) -> DrawSetType:
        ticket_combo = self.get_ticket_combo(ticket_index)
        max_matched_num_count = min(self.num_count_in_draw, self.num_count_in_ticket)
        nums_not_in_ticket = list(set(range(self.total_num_count)) - set(ticket_combo))
        return self.create_draw_set(
            [
                self.get_draw_index(tuple(sorted(matched_nums + unmatched_nums)))
                for matched_num_count in range(
                    self.min_matched_num_count, max_matched_num_count + 1
                )
                for matched_nums in combinations(ticket_combo, matched_num_count)
                for unmatched_nums in combinations(
                    nums_not_in_ticket, self.num_count_in_draw - matched_num_count
                )
            ]
        )

    def get_covered_draws(self, ticket_index: TicketIndexType) -> DrawSetType:
        if self.are_covered_draws_cached:
            return self.ticket_index_to_covered_draws[ticket_index]
        return self.generate_covered_draws(ticket_index)

    def get_covered_draws_of_tickets(self, ticket_indices: Iterable[TicketIndexType]):
        covered_draws = self.create_empty_draw_set()
        for ticket_index in ticket_indices:
            covered_draws.update(self.get_covered_draws(ticket_index))
        return covered_draws

    def get_uncovered_draws_of_tickets(self, ticket_indices: Iterable[TicketIndexType]):
        # TODO: check if this is faster
        uncovered_draws = self.create_full_draw_set()
        for ticket_index in ticket_indices:
            uncovered_draws.difference_update(self.get_covered_draws(ticket_index))
        return uncovered_draws
        # uncovered_draws = self.get_covered_draws_of_tickets(ticket_indices)
        # uncovered_draws.negation_update()
        # return uncovered_draws

    def create_draw_set(self, draw_indices: Iterable[DrawIndexType]) -> DrawSetType:
        return self.IntSet(self.total_draw_count, draw_indices)

    def create_empty_draw_set(self) -> DrawSetType:
        return self.create_draw_set([])

    def create_full_draw_set(self) -> DrawSetType:
        return self.create_draw_set(list(range(self.total_draw_count)))

    def get_uncovered_draws_from_covered_draws(self, draw_set: DrawSetType) -> DrawSetType:
        return draw_set.negation()

    def get_draws_containing_specific_number(self, specific_number) -> DrawSetType:
        return self.create_draw_set([
            self.get_draw_index(draw_combo)
            for draw_combo in self.all_draws
            if specific_number in draw_combo
        ])

    def get_tickets_containing_specific_number(self, specific_number) -> List[TicketIndexType]:
        return [
            self.get_ticket_index(ticket_combo)
            for ticket_combo in self.all_tickets
            if specific_number in ticket_combo
        ]

    def is_solution(self, ticket_indices: Iterable[TicketIndexType]):
        return self.get_covered_draws_of_tickets(ticket_indices).is_full()
