import typing as t

from abc import ABC, abstractmethod
from itertools import chain

from lazy_property import LazyProperty

from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator, serializeable_value
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.expansion import Expansion
from mtgorp.models.persistent.attributes.borders import Border

from mkmchecker.values.values import Condition
from mkmchecker.market.model import Article, Seller, Market


class Requirement(Serializeable):

	@abstractmethod
	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		pass

	@abstractmethod
	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		pass

	def serialize(self) -> serialization_model:
		return {
			'name': self.__class__.__name__,
			'values': self._serialized_values(),
		}

	@classmethod
	@abstractmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		pass

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Requirement':
		requirement_type = globals()[value['name']]  # type: t.Type[Requirement]
		return requirement_type._deserialize_values(value['values'], inflator)


class FromExpansions(Requirement):

	def __init__(self, expansions: t.Iterable[Expansion]):
		self._expansions = set(expansions)

	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		return article.expansion in self._expansions

	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		return {'expansions': self._expansions}

	@classmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		return cls(inflator.inflate_all(Expansion, values['expansions']))

	def __hash__(self) -> int:
		return hash(self._expansions)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and other._expansions == self._expansions
		)

	def __repr__(self):
		return f'{self.__class__.__name__}({self._expansions})'


class IsBorder(Requirement):

	def __init__(self, border: Border):
		self._border = border

	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		return article.expansion is not None and article.expansion.border == self._border

	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		return {'border': self._border.name}

	@classmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		return cls(Border[values['border']])

	def __hash__(self) -> int:
		return hash(self._border)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and other._border == self._border
		)

	def __repr__(self):
		return f'{self.__class__.__name__}({self._border})'


class IsMinimumCondition(Requirement):

	def __init__(self, condition: Condition):
		self._condition = condition

	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		return article.condition >= self._condition

	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		return {'condition': self._condition.name}

	@classmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		return cls(Condition[values['condition']])

	def __hash__(self) -> int:
		return hash(self._condition)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and other._condition == self._condition
		)

	def __repr__(self):
		return f'{self.__class__.__name__}({self._condition})'


class MinimumAmount(Requirement):

	def __init__(self, amount: int):
		self._amount = amount

	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		return article.count >= self._amount

	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		return {'amount': self._amount}

	@classmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		return cls(values['amount'])

	def __hash__(self) -> int:
		return hash(self._amount)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and other._amount == self._amount
		)

	def __repr__(self):
		return f'{self.__class__.__name__}({self._amount})'


class IsEnglish(Requirement):

	def __init__(self, value: bool):
		self._value = value

	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		return article.english == self._value

	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		return {'value': self._value}

	@classmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		return cls(values['value'])

	def __hash__(self) -> int:
		return hash(self._value)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._value == other._value
		)


class IsPlayset(Requirement):

	def __init__(self, value: bool):
		self._value = value

	def fulfilled(self, article: Article, seller: Seller, market: Market) -> bool:
		return article.playset == self._value

	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
		return {'value': self._value}

	@classmethod
	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Requirement':
		return cls(values['value'])

	def __hash__(self) -> int:
		return hash(self._value)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._value == other._value
		)


class Wish(Serializeable):

	def __init__(self,
		cardboard: Cardboard,
		requirements: t.Iterable[Requirement],
		weight: float = 1,
	 ):
		self._cardboard = cardboard
		self._requirements = frozenset(requirements)
		self._weight = weight

	@property
	def weight(self) -> float:
		return self._weight

	@property
	def cardboard(self):
		return self._cardboard

	@property
	def requirements(self) -> t.FrozenSet[Requirement]:
		return self._requirements

	def serialize(self) -> serialization_model:
		return {
			'cardboard': self._cardboard,
			'requirements': self._requirements,
			'weight': self._weight,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Wish':
		return cls(
			cardboard = inflator.inflate(Cardboard, value['cardboard']),
			requirements = (
				Requirement.deserialize(requirement, inflator)
				for requirement in
				value['requirements']
			),
			weight = value['weight'],
		)

	def __hash__(self) -> int:
		return hash(
			(
				self._cardboard,
				self._requirements,
				self._weight,
			)
		)

	def __eq__(self, other) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._cardboard == other._cardboard
			and self._requirements == other._requirements
			and self._weight == other._weight
		)


# class SingleCardboardWish(Wish):
#
# 	def __init__(self,
# 		cardboard: Cardboard,
# 		requirements: t.Iterable[Requirement],
# 		weight: float = 1,
# 	 ):
# 		super().__init__(weight)
# 		self._cardboard = cardboard
# 		self._requirements = set(requirements)
#
# 		self._cardboards = {cardboard}
#
# 	@property
# 	def cardboards(self) -> t.Set[Cardboard]:
# 		return self._cardboards
#
# 	def _filter_articles(self, articles: t.Iterable[Article], seller: Seller, market: Market) -> t.Iterable[Article]:
# 		return (
# 			article
# 			for article in
# 			articles
# 			if all(
# 				requirement.fulfilled(article, seller, market)
# 				for requirement in
# 				self._requirements
# 			)
# 		)
#
# 	def evaluate(
# 		self,
# 		seller: Seller,
# 		market: Market,
# 		strategy: t.Type[WishingStrategy]
# 	) -> t.Tuple[float, t.List[Article]]:
#
# 		available_articles = list(
# 			self._filter_articles(
# 				seller.articles_for_cardboard(self._cardboard),
# 				seller,
# 				market,
# 			)
# 		)
#
# 		if not available_articles:
# 			return 0., available_articles
#
# 		article = available_articles[0]
#
# 		for _article in available_articles:
# 			if _article.price < article.price:
# 				article = _article
#
# 		value = (
# 			strategy.absolute_price_reduction(article.price)
# 			* strategy.relative_price_multiplier(
# 				article.price,
# 				list(
# 					article.price
# 					for article in
# 					chain(
# 						*(
# 							self._filter_articles(
# 								seller.articles_for_cardboard(self._cardboard),
# 								seller,
# 								market,
# 							)
# 							for seller in
# 							market.sellers
# 						)
# 					)
# 				),
# 			)
# 			* strategy.condition_reduction(article.condition)
# 			* self._weight ** strategy.get_weight_exponent()
# 		)
#
# 		return value, [article]
#
# 	def _serialized_values(self) -> t.Dict[str, serializeable_value]:
# 		return {
# 			'cardboard': self._cardboard,
# 			'requirements': self._requirements,
# 			'weight': self._weight,
# 		}
#
# 	@classmethod
# 	def _deserialize_values(cls, values: t.Dict[str, serializeable_value], inflator: Inflator) -> 'Wish':
# 		return cls(
# 			inflator.inflate(Cardboard, values['cardboard']),
# 			(
# 				Requirement.deserialize(requirement, inflator)
# 				for requirement in
# 				values['requirements']
# 			),
# 			values['weight'],
# 		)
#
# 	def __hash__(self) -> int:
# 		return hash(self._cardboard)
#
# 	def __eq__(self, other) -> bool:
# 		return (
# 			isinstance(other, self.__class__)
# 			and self._cardboard == other._cardboard
# 		)
#
# 	def __repr__(self):
# 		return f'{self.__class__.__name__}({self.cardboards}, {self.weight}, {self._requirements})'


class WishList(Serializeable):

	def __init__(self, wishes: t.Iterable[Wish]):
		self._wishes = tuple(wishes)

	@property
	def wishes(self) -> t.Tuple[Wish, ...]:
		return self._wishes

	@LazyProperty
	def cardboards(self) -> t.Tuple[Cardboard]:
		return tuple(wish.cardboard for wish in self._wishes)

	def serialize(self) -> serialization_model:
		return {
			'wishes': self._wishes,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'WishList':
		return cls(
			Wish.deserialize(wish, inflator)
			for wish in
			value['wishes']
		)

	def __hash__(self) -> int:
		return hash(self._wishes)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and other._wishes == self._wishes
		)

	def __len__(self) -> int:
		return len(self._wishes)

	def __iter__(self) -> t.Iterable[Wish]:
		return self._wishes.__iter__()

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({self._wishes})'
