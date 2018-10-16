from enum import Enum
from functools import total_ordering


@total_ordering
class Condition(Enum):
	MINT = 'MT'
	NEAR_MINT = 'NM'
	EXCELLENT = 'EX'
	GOOD = 'GD'
	LIGHT_PLAYED = 'LP'
	PLAYED = 'PL'
	POOR = 'PO'

	def __le__(self, other) -> bool:
		return (
			_CONDITION_VALUE_MAP[self]
			< _CONDITION_VALUE_MAP[other]
		)


_CONDITION_VALUE_MAP = {
	condition: value
	for value, condition in
	enumerate(
		reversed(
			list(
				Condition.__iter__()
			)
		)
	)
}


APPLICATION_NAME = 'mkmchk'