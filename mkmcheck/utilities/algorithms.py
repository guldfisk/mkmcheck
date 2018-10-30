import typing as t

import numpy as np


T = t.TypeVar('T')


def fill_sack(
	capacity: int,
	weights: t.Sequence[int],
	values: t.Sequence[int],
	items: t.Sequence[T],
) -> t.Tuple[int, t.List[T]]:
	n = len(weights)

	matrix = np.zeros((n + 1, capacity + 1), dtype=int)

	for i in range(n + 1):
		for w in range(capacity + 1):

			if i == 0 or w == 0:
				matrix[i][w] = 0

			elif weights[i - 1] <= w:
				matrix[i][w] = max(
					values[i - 1] + matrix[i - 1][w - weights[i - 1]],
					matrix[i - 1][w],
				)

			else:
				matrix[i][w] = matrix[i - 1][w]

	result = matrix[n][capacity]
	remaining_capacity = capacity
	selected_items = []

	for i in range(n, 0, -1):
		if result <= 0:
			break

		if result == matrix[i - 1][remaining_capacity]:
			continue

		else:
			selected_items.append(items[i - 1])

			result = result - values[i - 1]
			remaining_capacity = remaining_capacity - weights[i - 1]

	return matrix[n][capacity], selected_items