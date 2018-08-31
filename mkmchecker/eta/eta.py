import time


class EtaContext(object):

	def __init__(self, amount: int):
		self._amount = amount
		self._st = time.time()

		self._current = 0
		self._previous_length = 0

	def update(self) -> None:
		self._current += 1

		eta = (self._amount - self._current) * (time.time() - self._st) / self._current

		printing = f'{self._current}/{self._amount} eta: {eta}'

		print('\b' * self._previous_length + printing)

		self._previous_length = len(printing) + 1

	def __enter__(self) -> 'EtaContext':
		return self

	def __exit__(self, exc_type, exc_val, exc_tb) -> None:
		print('\b' * self._previous_length)