import typing as t

import math
from abc import ABC, abstractmethod
import statistics
import functools
import itertools

import numpy as np

from mkmcheck.values.values import Condition
from mkmcheck.model.models import Market, Seller, Wish, CardboardWish, Article, WishList
from mkmcheck.utilities.algorithms import fill_sack
from mkmcheck.utilities.logging import Timer


class EvaluationStrategy(ABC):

	@classmethod
	@abstractmethod
	def evaluate_wish_article(cls, article: Article, wish: 'ConcludedWish', reasonable_price: float) -> float:
		pass

	@classmethod
	@abstractmethod
	def reasonable_price(cls, cardboard_prices: t.List) -> float:
		pass


class StandardEvaluationStrategy(EvaluationStrategy):

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
	def _get_weight_exponent(cls) -> float:
		return 2.2

	@classmethod
	def _condition_reduction(cls, condition: Condition) -> float:
		return cls._CONDITION_MAP[condition]

	@classmethod
	def _absolute_price_reduction(cls, price: float) -> float:
		try:
			return 1 / (1 + math.e ** (.7 * (price - 4) ) )
		except OverflowError:
			return 0.

	@classmethod
	def _relative_price_multiplier(cls, price: float, reasonable_price: float) -> float:
		try:
			return 1 / ( 1 + math.e ** ( price - reasonable_price ) )
		except OverflowError:
			return 0.

	@classmethod
	def evaluate_wish_article(cls, article: Article, wish: 'ConcludedWish', reasonable_price: float) -> float:
		return (
			wish.wish.weight ** cls._get_weight_exponent()
			* cls._condition_reduction(article.condition)
			* cls._absolute_price_reduction(article.adjusted_price)
			* cls._relative_price_multiplier(article.adjusted_price, reasonable_price)
		)

	@classmethod
	def reasonable_price(cls, cardboard_prices: t.List[float]) -> float:
		try:
			return np.percentile(cardboard_prices, 10)
		except IndexError:
			return 0.


class ConcludedCardboardWish(object):

	def __init__(self, cardboard_wish: CardboardWish, concluded_wish: 'ConcludedWish', evaluator: 'Evaluator'):
		self._cardboard_wish = cardboard_wish
		self._concluded_wish = concluded_wish
		self._evaluator = evaluator

		self._articles = [] #type: t.List[t.Tuple[Article, int]]
		self._initialize_articles()

		self._value = None #type: t.Optional[float]

	def _initialize_articles(self) -> None:
		valid_articles = sorted(
			(
				article
				for article in
				self._concluded_wish.seller.get_articles_for_cardboard(
					self._cardboard_wish.cardboard_name
				)
				if self._cardboard_wish.validate_article(
					article
				)
			),
			key=lambda a:
				a.adjusted_price,
		)

		remaining_requirement = self._cardboard_wish.minimum_amount

		# This could be an actual sack fill, if the performance hit is worth it
		for article in valid_articles:
			if article.is_playset and remaining_requirement >= 4:
				amount = min(article.amount, remaining_requirement) // 4
				self._articles.append(
					(
						article,
						amount,
					)
				)
				remaining_requirement -= amount * 4

			else:
				self._articles.append(
					(
						article,
						min(article.amount, remaining_requirement),
					)
				)
				remaining_requirement -= article.amount

			if remaining_requirement <= 0:
				break

	@property
	def cardboard_amount(self):
		return sum(
			amount
			for article, amount in
			self._articles
		)

	@property
	def articles(self) -> t.Iterable[Article]:
		return (article for article, _ in self._articles)

	@property
	def fulfilled(self) -> bool:
		return self.cardboard_amount >= self._cardboard_wish.minimum_amount

	@property
	def value(self) -> float:
		if self._value is None:
			self._value = (
				0.
				if not self.fulfilled else
				sum(
					self._evaluator.evaluate_wish_article(
						article = article,
						wish = self._concluded_wish,
					) * amount
					for article, amount in
					self._articles
				) / self._cardboard_wish.minimum_amount
			)

		return self._value

	@property
	def price(self) -> float:
		return sum(article.price * amount for article, amount in self._articles)

	def __str__(self):
		return ', '.join(map(str, self.articles))


class ConcludedWish(object):

	def __init__(self, wish: Wish, seller: Seller, evaluator: 'Evaluator'):
		self._wish = wish
		self._seller = seller
		self._evaluator = evaluator

		self._concluded_cardboard_wishes = [] #type: t.List[ConcludedCardboardWish]
		self._initialize_concluded_cardboard_wishes()

		self._value = None #type: t.Optional[float]

	def _initialize_concluded_cardboard_wishes(self):
		self._concluded_cardboard_wishes = [
			ConcludedCardboardWish(
				cardboard_wish = cardboard_wish,
				concluded_wish = self,
				evaluator = self._evaluator,
			)
			for cardboard_wish in
			self._wish.cardboard_wishes
		]

	@property
	def seller(self) -> Seller:
		return self._seller

	@property
	def wish(self) -> Wish:
		return self._wish

	@property
	def fulfilled(self):
		return all(
			concluded_cardboard_wish.fulfilled
			for concluded_cardboard_wish in
			self._concluded_cardboard_wishes
		)

	@property
	def value(self) -> float:
		if self._value is None:
			self._value = (
				0.
				if not self.fulfilled else
				statistics.mean(
					evaluated_cardboard_wish.value
					for evaluated_cardboard_wish in
					self._concluded_cardboard_wishes
				)
			)

		return self._value

	@property
	def price(self) -> float:
		return sum(
			concluded_cardboard_wish.price
			for concluded_cardboard_wish in
			self._concluded_cardboard_wishes
		)

	def __str__(self):
		return ', '.join(
			f'({concluded_cardboard_wish})'
			for concluded_cardboard_wish in
			self._concluded_cardboard_wishes
		)


class ConcludedSeller(object):

	def __init__(self, seller: Seller, evaluator: 'Evaluator'):
		self._seller = seller
		self._evaluator = evaluator

		self._concluded_wishes = [
			ConcludedWish(
				wish = wish,
				seller = self._seller,
				evaluator = self._evaluator,
			)
			for wish in
			self._evaluator.wish_list.wishes
		]

		self._value = None #type: t.Optional[float]
		self._sorted = False

	@property
	def sorted_concluded_wishes(self) -> t.List[ConcludedWish]:
		if not self._sorted:
			self._concluded_wishes.sort(
				key = lambda c: c.value,
				reverse = True,
			)
			self._sorted = True
		return self._concluded_wishes

	@property
	def seller(self) -> Seller:
		return self._seller

	@property
	def value(self) -> float:
		if self._value is None:
			self._value = sum(
				concluded_wish.value
				for concluded_wish in
				self._concluded_wishes
			)

		return self._value

	@functools.lru_cache()
	def get_knapsack_values(self, sack_size: int) -> t.Tuple[float, t.List[ConcludedWish]]:
		value, lst = fill_sack(
			int(sack_size),
			*zip(
				*(
					(int(wish.price), int(wish.value), wish)
					for wish in
					self.sorted_concluded_wishes
				)
			)
		)
		return value, lst

	@property
	def price(self) -> float:
		return sum(
			concluded_wish.price
			for concluded_wish in
			self._concluded_wishes
		)


class Evaluator(object):

	def __init__(
		self,
		market: Market,
		evaluation_strategy: t.Type[EvaluationStrategy],
		wish_list: t.Optional[WishList] = None,
	):
		self._market = market
		self._evaluation_strategy = evaluation_strategy
		self._wish_list = self._market.wish_list if wish_list is None else wish_list

		self._prices_map = {} #type: t.Dict[str, t.List[float]]
		self._reasonable_price_map = {} #type: t.Dict[str, float]

		self._concluded_sellers = [] #type: t.List[ConcludedSeller]

	@property
	def evaluation_strategy(self) -> t.Type[EvaluationStrategy]:
		return self._evaluation_strategy

	@property
	def market(self) -> Market:
		return self._market

	@property
	def wish_list(self) -> WishList:
		return self._wish_list

	@property
	def concluded_sellers(self) -> t.List[ConcludedSeller]:
		return self._concluded_sellers

	def _initialize_price_map(self):

		for cardboard_name in self.wish_list.cardboard_names:
			self._prices_map[cardboard_name] = list(
				itertools.chain(
					*(
						(
							article.adjusted_price
							for article in
							seller.get_articles_for_cardboard(cardboard_name)
						)
						for seller in
						self._market.sellers
					)
				)
			)

		self._reasonable_price_map = {
			key: self._evaluation_strategy.reasonable_price(prices)
			for key, prices in
			self._prices_map.items()
		}

	def _get_reasonable_price(self, cardboard_name: str) -> float:
		return self._reasonable_price_map[cardboard_name]

	def evaluate_wish_article(self, article: Article, wish: ConcludedWish):
		return self._evaluation_strategy.evaluate_wish_article(
			article = article,
			wish = wish,
			reasonable_price = self._get_reasonable_price(
				article.cardboard_name
			)
		)

	def evaluate(self) -> 'Evaluator':

		print('evaluating')
		timer = Timer()

		self._initialize_price_map()

		timer.update('price map initialized')

		self._concluded_sellers = [
			ConcludedSeller(
				seller = seller,
				evaluator = self,
			) for seller in
			self._market.sellers
		]

		timer.update('concluded sellers constructed')

		self._concluded_sellers.sort(
			key = lambda s: s.value,
			reverse = True,
		)

		timer.update('sellers sorted')

		return self