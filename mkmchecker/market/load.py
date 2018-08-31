import typing as t

import datetime
import os

from mtgorp.models.serilization.strategies.jsonid import JsonId
from mtgorp.db.database import CardDatabase
from mtgorp.models.persistent.cardboard import Cardboard

from mkmchecker import paths
from mkmchecker.market.model import Market
from mkmchecker.market.update import MarketFetcher


class MarketLoadException(Exception):
	pass


class MarketLoader(object):

	LOCAL_MARKETS_PATH = os.path.join(paths.APP_DATA_DIR, 'markets')
	TIMESTAMP_FORMAT = '%d_%m_%y_%H_%M_%S'

	def __init__(self, db: CardDatabase):
		self._db = db
		self._fetcher = MarketFetcher(self._db)
		self._strategy = JsonId(self._db)

	def _get_all_local_lists(self) -> t.Iterator[Market]:
		if not os.path.exists(self.LOCAL_MARKETS_PATH):
			os.makedirs(self.LOCAL_MARKETS_PATH)

		markets = os.listdir(self.LOCAL_MARKETS_PATH)

		if not markets:
			return

		names_times = []  # type: t.List[t.Tuple[str, datetime.datetime]]

		for market in markets:
			try:
				names_times.append(
					(
						market,
						datetime.datetime.strptime(market, self.TIMESTAMP_FORMAT),
					)
				)
			except ValueError:
				pass

		if not names_times:
			return

		sorted_pairs = sorted(names_times, key=lambda item: item[1], reverse = True)

		for name, time in sorted_pairs:
			with open(os.path.join(self.LOCAL_MARKETS_PATH, name), 'r') as f:
				yield self._strategy.deserialize(Market, f.read())

	def _get_current_local_list(self) -> t.Optional[Market]:
		try:
			return self._get_all_local_lists().__next__()
		except StopIteration:
			return None

	@classmethod
	def _persist_market(cls, market: Market) -> None:
		if not os.path.exists(cls.LOCAL_MARKETS_PATH):
			os.makedirs(cls.LOCAL_MARKETS_PATH)

		with open(
			os.path.join(
				cls.LOCAL_MARKETS_PATH,
				datetime.datetime.strftime(
					datetime.datetime.today(),
					cls.TIMESTAMP_FORMAT,
				),
			),
			'w',
		) as f:
			f.write(JsonId.serialize(market))

	def update(self, cardboards: t.Iterable[Cardboard], clear_cache_when_done: bool = True) -> Market:
		market = self._fetcher.fetch(cardboards, clear_cache_when_done = clear_cache_when_done)
		self._persist_market(market)
		return market

	def load(self, cardboards: t.Optional[t.Iterable[Cardboard]] = None) -> Market:
		wish_list = self._get_current_local_list()

		if wish_list is None:
			if cardboards is None:
				raise MarketLoadException()

			self.update(cardboards)
			return self._get_current_local_list()

		return wish_list

	def all_local_markets(self) -> t.Iterator[Market]:
		return self._get_all_local_lists()