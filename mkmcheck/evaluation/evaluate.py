import typing as t

import os
from abc import ABC, abstractmethod
import math
from itertools import chain

import numpy as np

from lazy_property import LazyProperty

from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator
from mtgorp.models.serilization.strategies.picklestrategy import PickleStrategy
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.db.database import CardDatabase

from mkmcheck.values.values import Condition
from mkmcheck.wishlist.wishlist import WishList, Wish, Requirement
from mkmcheck.market.model import Market, Seller, Article
from mkmcheck import paths
from mkmcheck.utilities.algorithms import fill_sack


class WishingStrategy(ABC):

	@classmethod
	@abstractmethod
	def get_weight_exponent(cls) -> float:
		pass

	@classmethod
	@abstractmethod
	def condition_reduction(cls, condition: Condition) -> float:
		pass

	@classmethod
	@abstractmethod
	def absolute_price_reduction(cls, price: float) -> float:
		pass

	@classmethod
	@abstractmethod
	def reasonable_price(cls, cardboard_prices: t.List) -> float:
		pass

	@classmethod
	@abstractmethod
	def relative_price_multiplier(cls, price: float, reasonable_price: float) -> float:
		pass


class StandardWishingStrategy(WishingStrategy):

	_CONDITION_MAP = {
		Condition.MINT: 1.,
		Condition.NEAR_MINT: 1.,
		Condition.EXCELLENT: 1.,
		Condition.GOOD: .9,
		Condition.LIGHT_PLAYED: .8,
		Condition.PLAYED: .7,
		Condition.POOR: .4,
	}

	@classmethod
	def get_weight_exponent(cls) -> float:
		return 1.9

	@classmethod
	def condition_reduction(cls, condition: Condition) -> float:
		return cls._CONDITION_MAP[condition]

	@classmethod
	def absolute_price_reduction(cls, price: float) -> float:
		try:
			return 1 / (1 + math.e ** (.2 * (price - 10) ) )
		except OverflowError:
			return 0.

	@classmethod
	def reasonable_price(cls, cardboard_prices: t.List[float]) -> float:
		try:
			return np.percentile(cardboard_prices, 10)
		except IndexError:
			return 0.

	@classmethod
	def relative_price_multiplier(cls, price: float, reasonable_price: float) -> float:
		try:
			return 1 / ( 1 + math.e ** ( 5 * ( ( price / reasonable_price ) - 1.5 ) ) )
		except OverflowError:
			return 0.


class EvaluatedWish(Serializeable):

	def __init__(self, wish: Wish, article: t.Optional[Article], value: float):
		self._wish = wish
		self._article = article
		self._value = value

	@property
	def wish(self) -> Wish:
		return self._wish

	@property
	def article(self) -> t.Optional[Article]:
		return self._article

	@property
	def value(self) -> float:
		return (
			self._value
			if self._article else
			0
		)

	@property
	def fulfilled(self) -> bool:
		return bool(self._article)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._wish == other._wish
			and self._article == other._article
		)

	def __hash__(self) -> int:
		return hash((self._wish, self._article))

	def serialize(self) -> serialization_model:
		return {
			'wish': self._wish,
			'article': self._article,
			'value': self._value,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'EvaluatedWish':
		return cls(
			Wish.deserialize(value['wish'], inflator),
			Article.deserialize(value['article'], inflator),
			value['value'],
		)

	def __str__(self) -> str:
		return f'{self.__class__.__name__}({self._wish}, {self._article}, {self._value})'


class EvaluatedSeller(Serializeable):

	def __init__(
		self,
		seller: Seller,
		wishes: t.Optional[t.List[EvaluatedWish]] = None,
	):
		self._seller = seller
		self._wishes = [] if wishes is None else wishes #type: t.List[EvaluatedWish]

	@property
	def seller(self) -> Seller:
		return self._seller

	@property
	def wishes(self) -> t.List[EvaluatedWish]:
		return self._wishes

	@LazyProperty
	def value(self) -> float:
		return sum(wish.value for wish in self._wishes)

	@classmethod
	def _float_to_int(cls, value: float) -> int:
		return int(value * 100)

	@classmethod
	def _int_to_float(cls, value: int) -> float:
		return value / 100

	def max_value_for_price(self, price: float) -> t.Tuple[float, t.List[EvaluatedWish]]:
		value, wishes = fill_sack(
			self._float_to_int(price),
			*zip(
				*(
					(
						self._float_to_int(wish.article.price),
						self._float_to_int(wish.value),
						wish,
					)
					for wish in
					self._wishes
					if wish.fulfilled
				)
			)
		)
		return self._int_to_float(value), wishes

	def serialize(self) -> serialization_model:
		return {
			'seller': self._seller,
			'wishes': self._wishes,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'EvaluatedSeller':
		return cls(
			Seller.deserialize(value['seller'], inflator),
			[
				EvaluatedWish.deserialize(evaluated_wish, inflator)
				for evaluated_wish in
				value['wishes']
			],
		)

	def __hash__(self) -> int:
		return hash(self._seller)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._seller == other.seller
		)


class EvaluatedSellers(Serializeable):

	def __init__(self, wish_list: WishList, sellers: t.List[EvaluatedSeller]):
		self._wish_list = wish_list
		self._sellers = sellers

	@property
	def wish_list(self) -> WishList:
		return self._wish_list

	@property
	def sellers(self) -> t.List[EvaluatedSeller]:
		return self._sellers

	def serialize(self) -> serialization_model:
		return {
			'wish_list': self._wish_list,
			'sellers': self._sellers,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'EvaluatedSellers':
		return cls(
			WishList.deserialize(value['wish_list'], inflator),
			[
				EvaluatedSeller.deserialize(seller, inflator)
				for seller in
				value['sellers']
			],
		)

	def __hash__(self) -> int:
		return hash((self._wish_list, self._sellers))

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._wish_list == other._wish_list
			and self._sellers == other._sellers
		)

	def __iter__(self) -> t.Iterable[EvaluatedSeller]:
		return self._sellers.__iter__()


class Evaluator(object):

	def __init__(self, market: Market, wish_list: WishList, wish_strategy: t.Type[WishingStrategy]):
		self._market = market
		self._wish_list = wish_list
		self._wishing_strategy = wish_strategy

		self._reasonable_prices = {} #type: t.Dict[t.Tuple[Cardboard, t.FrozenSet[Requirement]], float]

	def _get_reasonable_price(
		self,
		cardboard: Cardboard,
		requirements: t.FrozenSet[Requirement],
	) -> float:
		key = cardboard, requirements

		try:
			return self._reasonable_prices[key]
		except KeyError:
			value = self._wishing_strategy.reasonable_price(
				list(
					article.price
					for article in
					chain(
						*(
							self._filter_articles(
								seller.articles_for_cardboard(cardboard),
								requirements,
								seller,
								self._market,
							)
							for seller in
							self._market.sellers
						)
					)
				)
			)
			self._reasonable_prices[key] = value
			return value

	@classmethod
	def _filter_articles(
		cls,
		articles: t.Iterable[Article],
		requirements: t.FrozenSet[Requirement],
		seller: Seller,
		market: Market,
	) -> t.Iterable[Article]:
		return (
			article
			for article in
			articles
			if all(
				requirement.fulfilled(article, seller, market)
				for requirement in
				requirements
			)
		)

	def _evaluate_wish(
		self,
		wish: Wish,
		seller: Seller,
		market: Market,
		strategy: t.Type[WishingStrategy]
	) -> t.Tuple[t.Optional[Article], float]:

		available_articles = list(
			self._filter_articles(
				seller.articles_for_cardboard(wish.cardboard),
				wish.requirements,
				seller,
				market,
			)
		)

		if not available_articles:
			return None, 0.

		article = available_articles[0]

		for _article in available_articles:
			if _article.price < article.price:
				article = _article

		return article, (
			strategy.absolute_price_reduction(article.price)
			* strategy.relative_price_multiplier(
				article.price,
				self._get_reasonable_price(
					wish.cardboard,
					wish.requirements,
				),
			)
			* strategy.condition_reduction(article.condition)
			* wish.weight ** strategy.get_weight_exponent()
		)

	def evaluate(self) -> EvaluatedSellers:
		evaluated_sellers = []

		for seller in self._market.sellers:

			evaluated_seller = EvaluatedSeller(seller)

			for wish in self._wish_list:
				article, value = self._evaluate_wish(
					wish = wish,
					seller = seller,
					market = self._market,
					strategy = self._wishing_strategy,
				)

				evaluated_seller.wishes.append(
					EvaluatedWish(
						wish,
						article,
						value,
					)
				)

			evaluated_sellers.append(evaluated_seller)

		return EvaluatedSellers(
			self._wish_list,
			sorted(
				evaluated_sellers,
				key = lambda _evaluated_seller: _evaluated_seller.value,
				reverse = True,
			),
		)


class EvaluationPersistor(object):

	_EVALUATION_PATH = os.path.join(
		paths.APP_DATA_DIR,
		'evaluations',
	)

	def __init__(self, db: CardDatabase):
		self._db = db
		self._strategy = PickleStrategy(db)

		if not os.path.exists(self._EVALUATION_PATH):
			os.makedirs(self._EVALUATION_PATH)

	def save(self, evaluated_sellers: EvaluatedSellers, name: str) -> None:
		with open(os.path.join(self._EVALUATION_PATH, name), 'wb') as f:
			f.write(
				self._strategy.serialize(evaluated_sellers)
			)

	def load(self, name: str) -> EvaluatedSellers:
		with open(os.path.join(self._EVALUATION_PATH, name), 'rb') as f:
			return self._strategy.deserialize(
				EvaluatedSellers,
				f.read(),
			)