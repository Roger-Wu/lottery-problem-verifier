from typing import Tuple
import math

def calculate_combination_index(combination: Tuple[int, ...], total_numbers: int) -> int:
    """
    Calculate the index of a combination in the list of all combinations
    which is list(combinations(range(total_numbers), combo_length).

    We calculate the index by counting the combinations skipped before the given combination.
    For example, if combination = (5, 10, 17, 28) and total_numbers = 30
    Then we skipped from (0, 1, 2, 3) to (5, 6, 7, 8)
        = skipped comb(29, 3) + comb(28, 3) + comb(27, 3) + comb(26, 3) + comb(25, 3)
        = skipped comb(30 - 0, 4) - comb(30 - 5, 4)
    Then from (5, 6, 7, 8) to (5, 10, 11, 12)
        = skipped comb(30 - 6, 3) - comb(30 - 10, 3)
    Then from (5, 10, 11, 12) to (5, 10, 17, 18)
    Then from (5, 10, 17, 18) to (5, 10, 17, 28)

    We can instantly calculate (comb(n, k) + comb(n+1, k) + ... + comb(m, k))
    using hockey stick theorem (aka hockey-stick identity)
    The sum is (comb(m+1, k+1) - comb(n, k+1))
    """
    combo_length = len(combination)
    combo_index = 0

    for position, current_number in enumerate(combination):
        previous_number = combination[position - 1] if position > 0 else -1
        combo_index += (
            math.comb(total_numbers - previous_number - 1, combo_length - position)
            - math.comb(total_numbers - current_number, combo_length - position)
        )

    return combo_index

def generate_combination_by_index(
    combo_index: int,
    total_numbers: int,
    combo_length: int,
    validate_args: bool = False,
) -> Tuple[int, ...]:
    """
    Generate the combination tuple that is at
    list(combinations(range(total_numbers), combo_length)[combo_index]
    without generating the whole list.

    TODO: Use Binary search to find current_number.
    """
    if validate_args:
        if combo_length > total_numbers:
            raise ValueError("Combination length cannot be greater than the total number of elements.")
        if combo_index < 0:
            raise ValueError("Combo index cannot be negative.")
        total_combinations = math.comb(total_numbers, combo_length)
        if combo_index >= total_combinations:
            raise ValueError("Combo index is out of range for the number of combinations possible.")

    combination = []
    current_number = 0
    current_index = 0

    for position in range(combo_length):
        remaining_length = combo_length - position
        for candidate_number in range(current_number, total_numbers):
            # the amount of combinations starting with candidate_number
            combo_count = math.comb(total_numbers - candidate_number - 1, remaining_length - 1)
            if current_index + combo_count > combo_index:
                combination.append(candidate_number)
                current_number = candidate_number + 1
                break
            current_index += combo_count
    return tuple(combination)
