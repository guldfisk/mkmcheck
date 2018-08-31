import typing as t

from lazy_property import LazyProperty

from mtgorp.models.serilization.serializeable import Serializeable, serialization_model, Inflator
from mtgorp.models.persistent.cardboard import Cardboard
from mtgorp.models.persistent.expansion import Expansion

from mkmchecker.values.values import Condition


class Article(Serializeable):

	def __init__(
		self,
		cardboard: Cardboard,
		price: float,
		condition: Condition,
		foil: bool,
		signed: bool,
		altered: bool,
		english: bool,
		playset: bool,
		expansion: t.Optional[Expansion] = None,
		count: int = 1,
	):
		self._cardboard = cardboard
		self._price = price
		self._condition = condition
		self._foil = foil
		self._signed = signed
		self._altered = altered
		self._english = english
		self._playset = playset
		self._expansion = expansion

		self._count = count

	@property
	def cardboard(self) -> Cardboard:
		return self._cardboard

	@property
	def price(self) -> float:
		return self._price

	@property
	def condition(self) -> Condition:
		return self._condition

	@property
	def foil(self) -> bool:
		return self._foil

	@property
	def signed(self) -> bool:
		return self._signed

	@property
	def altered(self) -> bool:
		return self._altered

	@property
	def english(self) -> bool:
		return self._english

	@property
	def playset(self) -> bool:
		return self._playset

	@property
	def expansion(self) -> t.Optional[Expansion]:
		return self._expansion

	@property
	def count(self) -> int:
		return self._count

	def serialize(self) -> serialization_model:
		return {
				'cardboard': self._cardboard,
				'price': self._price,
				'condition': self._condition.name,
				'foil': self._foil,
				'signed': self._signed,
				'altered': self._altered,
				'language': self._english,
				'playset': self._playset,
				'expansion': self._expansion,
				'count': self._count,
			}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Article':
		return Article(
			cardboard = inflator.inflate(Cardboard, value['cardboard']),
			price = value['price'],
			condition = Condition[value['condition']],
			foil = value['foil'],
			signed = value['signed'],
			altered = value['altered'],
			english= value['language'],
			playset = value['playset'],
			expansion =
				None
				if value['expansion'] is None else
				inflator.inflate(Expansion, value['expansion']),
			count = value['count'],
		)

	def __hash__(self) -> int:
		return hash(
			(
				self._cardboard,
				self._condition,
				self._foil,
				self._signed,
				self._altered,
				self._english,
				self._playset,
				self._expansion,
			)
		)

	def __eq__(self, other) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._cardboard == other._cardboard
			and self._condition == other._condition
			and self._foil == other._foil
			and self._signed == other._signed
			and self._altered == other._altered
			and self._english == other._english
			and self._playset == other._playset
			and self._expansion == other._expansion
		)

	def __repr__(self) -> str:
		return (
			'{}({}, {}, {}, {}, {}, {}, {}, {}, {})'.format(
				self.__class__.__name__,
				self._cardboard,
				self._price,
				self._expansion,
				self._count,
				self._condition,
				self._foil,
				self._signed,
				self._altered,
				self._playset,
			)
		)


class Seller(Serializeable):

	def __init__(self, name: str, articles: t.Iterable[Article]):
		self._name = name
		self._articles = set(articles)

		self._articles_for_cardboard = {} #type: t.Dict[Cardboard, t.List[Article]]

		for article in self._articles:
			try:
				self._articles_for_cardboard[article.cardboard].append(article)
			except KeyError:
				self._articles_for_cardboard[article.cardboard] = [article]

	@property
	def name(self) -> str:
		return self._name

	@property
	def articles(self) -> t.Set[Article]:
		return self._articles

	@LazyProperty
	def cardboards(self) -> t.Dict[Cardboard, t.List[Article]]:
		d = {}

		for article in self._articles:
			try:
				d[article.cardboard].append(article)
			except KeyError:
				d[article.cardboard] = [article]

		return d

	def articles_for_cardboard(self, cardboard: Cardboard) -> t.List[Article]:
		return self._articles_for_cardboard.get(cardboard, [])

	def serialize(self) -> serialization_model:
		return {
			'name': self._name,
			'articles': self._articles,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Seller':
		return Seller(
			name = value['name'],
			articles = (
				Article.deserialize(_value, inflator)
				for _value in
				value['articles']
			),
		)

	def __hash__(self) -> int:
		return hash(self._name)

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._name == other._name
		)

	def __repr__(self) -> str:
		return f'{self.__class__.__name__}({self._name})'


class Market(Serializeable):

	def __init__(self, sellers: t.Iterable[Seller], cardboards: t.Iterable[Cardboard]):
		self._sellers = frozenset(sellers)
		self._cardboards = frozenset(cardboards)

		self._seller_map = {seller.name: seller for seller in self._sellers} #type: t.Dict[str, Seller]
		self._cardboard_articles = {} #type: t.Dict[Cardboard, t.List[Article]]

	@property
	def sellers(self) -> t.AbstractSet[Seller]:
		return self._sellers

	@property
	def cardboards(self) -> t.AbstractSet[Cardboard]:
		return self._cardboards

	@LazyProperty
	def articles(self) -> t.Tuple[Article, ...]:
		return tuple(
			article
			for seller in
			self._sellers
			for article
			in seller.articles
		)

	def get_articles_for_cardboard(self, cardboard: Cardboard) -> t.List[Article]:
		try:
			return self._cardboard_articles[cardboard]
		except KeyError:
			self._cardboard_articles[cardboard] = list(
				article
				for article in
				self.articles
				if article.cardboard == cardboard
			)
			return self._cardboard_articles[cardboard]

	def get_prices_for_cardboard(self, cardboard: Cardboard) -> t.List[float]:
		return list(article.price for article in self.get_articles_for_cardboard(cardboard))

	def serialize(self) -> serialization_model:
		return {
			'sellers': self._sellers,
			'cardboards': self._cardboards,
		}

	@classmethod
	def deserialize(cls, value: serialization_model, inflator: Inflator) -> 'Market':
		return cls(
			(
				Seller.deserialize(seller, inflator)
				for seller in
				value['sellers']
			),
			inflator.inflate_all(Cardboard, value['cardboards']),
		)

	def __getitem__(self, item: str) -> Seller:
		return self._seller_map[item]

	def __hash__(self) -> int:
		return hash((self._sellers, self._cardboards))

	def __eq__(self, other: object) -> bool:
		return (
			isinstance(other, self.__class__)
			and self._sellers == other._sellers
			and self._cardboards == other._cardboards
		)

