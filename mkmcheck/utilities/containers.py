import typing as t

from collections import OrderedDict as _OrderedDict


K = t.TypeVar('K')
V = t.TypeVar('T')


class OrderedDict(_OrderedDict, t.Generic[K, V]):

	def __getitem__(self, item: K) -> V:
		return super().__getitem__(item)

	def __iter__(self) -> t.Iterable[K]:
		return super().__iter__()

	def keys(self) -> t.KeysView[K]:
		return super().keys()

	def values(self) -> t.ValuesView[V]:
		return super().values()

	def items(self) -> t.ItemsView[K, V]:
		return super().items()
