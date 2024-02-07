import logging
from collections import defaultdict, Counter
from lottery_problem_with_cache import LotteryProblemWithCache


class LotteryProblemVerifier:
    def __init__(
        self,
        lottery_problem_with_cache: "LotteryProblemWithCache",
        logger=None,
    ) -> None:
        self.lpc = lottery_problem_with_cache
        if logger:
            self.logger = logger
        else:
            logging.basicConfig(
                format="%(asctime)s %(levelname)s  %(message)s",
                level=logging.INFO,
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            self.logger = logging.getLogger("LotteryProblemVerifier")

    # check if selected_ticket_idxs covers all draws
    def verify_coverage(
        self, ticket_indices, print_info=True
    ):
        total_draw_count = self.lpc.total_draw_count
        if print_info:
            self.logger.info(f"{total_draw_count} draws in total")

        uncovered_draws = self.lpc.create_full_draw_set()
        for index, ticket_index in enumerate(ticket_indices):
            uncovered_draws.difference_update(
                self.lpc.get_covered_draws(ticket_index)
            )
            if print_info:
                ticket_combo = self.lpc.get_ticket_combo(ticket_index)
                uncovered_draw_count = len(uncovered_draws)
                uncovered_draw_percentage = uncovered_draw_count / total_draw_count * 100
                self.logger.info("----")
                self.logger.info(f"add ticket {index + 1}: {ticket_combo}")
                self.logger.info(f"{uncovered_draw_count} / {total_draw_count} = {uncovered_draw_percentage:.2f}% draws uncovered")

        # print("uncovered draws:", [self.lpc.get_draw_combo(draw_index) for draw_index in uncovered_draws])
        return len(uncovered_draws)

    # check if selected_ticket_idxs covers all draws
    def check_coverage_distribution(
        self, ticket_indices, print_info=True
    ):
        total_draw_count = self.lpc.total_draw_count
        if print_info:
            print(f"{total_draw_count} draws in total")

        draw_index_to_covered_frequency = defaultdict(int)

        for index, ticket_index in enumerate(ticket_indices):
            covered_draw_indices = self.lpc.get_covered_draws(ticket_index)
            for draw_index in covered_draw_indices:
                draw_index_to_covered_frequency[draw_index] += 1

        frequencies = draw_index_to_covered_frequency.values()
        frequency_to_occurence_count = Counter(frequencies)
        if print_info:
            print("covered_frequency_to_occurence_count:", frequency_to_occurence_count)
            # print(frequency_to_occurence_count)

        # print([self.lpc.get_draw_combo(draw_index) for draw_index in uncovered_draws])
        return frequency_to_occurence_count

    # Count the occurrences of each number
    def count_nums(self, ticket_indices, print_info=True):
        ticket_combos = self.lpc.get_tickets_by_indices(ticket_indices)
        counter = Counter([num for combo in ticket_combos for num in combo])
        sorted_counts = sorted(counter.items(), key=lambda item: item[1], reverse=True)
        if print_info:
            for k, v in sorted_counts:
                print(f"number {k} appears {v} times")
        return counter

    def evaluate_redundancy(self, selected_ticket_idxs):
        ticket_redundancies = [0] * len(selected_ticket_idxs)
        draw_idx_to_cover_times = [0] * self.lpc.total_draw_count

        # First pass: Identify covered draws and their covering times
        for ticket_idx in selected_ticket_idxs:
            for draw_idx in self.lpc.get_covered_draws(ticket_idx):
                draw_idx_to_cover_times[draw_idx] += 1

        # Second pass: Calculate redundancy count for each selected ticket
        for i, ticket_idx in enumerate(selected_ticket_idxs):
            for draw_idx in self.lpc.get_covered_draws(ticket_idx):
                # If this draw combination is covered by more than one ticket, it's redundant for this ticket
                if draw_idx_to_cover_times[draw_idx] > 1:
                    ticket_redundancies[i] += 1

        return ticket_redundancies

    def sort_and_print_tickets_by_redundancy(self, selected_ticket_idxs):
        ticket_redundancies = self.evaluate_redundancy(selected_ticket_idxs)

        # Sort the selected tickets by their redundancy count, in descending order
        sorted_ticket_redundancies_idxs = sorted(zip(ticket_redundancies, selected_ticket_idxs), reverse=True)
        sorted_ticket_idxs = [ticket_idx for _, ticket_idx in sorted_ticket_redundancies_idxs]

        # Print the sorted tickets along with their redundancy count
        print("Sorted tickets by redundancy:")
        print(sorted_ticket_idxs)
        print(sorted_ticket_redundancies_idxs)
        for redundancy, ticket_idx in sorted_ticket_redundancies_idxs:
            print(f"Ticket {ticket_idx}, Combo: {self.lpc.get_ticket_combo(ticket_idx)}, Redundancy Count: {redundancy}/{self.lpc.covered_draw_count_per_ticket}")

    def count_overlap(self, ticket_indices, print_info=True):
        ticket_combos = self.lpc.get_tickets_by_indices(ticket_indices)

        counter = defaultdict(int)
        for i in range(len(ticket_combos)):
            combo_1 = ticket_combos[i]
            for j in range(i + 1, len(ticket_combos)):
                combo_2 = ticket_combos[j]
                overlap_count = len(set(combo_1) & set(combo_2))
                counter[overlap_count] += 1

        sorted_counts = sorted(counter.items(), key=lambda item: item[0], reverse=True)
        if print_info:
            for k, v in sorted_counts:
                print(f"overlap {k} appears {v} times")
        return counter
