import typing as t


import datetime
import os

from mtgorp.models.serilization.strategies.jsonid import JsonId
from mtgorp.db.database import CardDatabase

from mkmcheck import paths
from mkmcheck.wishlist.wishlist import WishList
from mkmcheck.wishload.fetch import WishFetcher, WishFetchException


class WishLoadException(Exception):
	pass


class WishListLoader(object):

	LOCAL_LISTS_PATH = os.path.join(paths.APP_DATA_DIR, 'wish_lists')
	TIMESTAMP_FORMAT = '%d_%m_%y_%H_%M_%S'

	def __init__(self, db: CardDatabase):
		self._db = db
		self._fetcher = WishFetcher(self._db)
		self._strategy = JsonId(self._db)

	def _get_all_local_lists(self) -> t.Iterator[WishList]:
		if not os.path.exists(self.LOCAL_LISTS_PATH):
			os.makedirs(self.LOCAL_LISTS_PATH)

		lists = os.listdir(self.LOCAL_LISTS_PATH)

		if not lists:
			return

		names_times = []  # type: t.List[t.Tuple[str, datetime.datetime]]

		for wish_list in lists:
			try:
				names_times.append(
					(
						wish_list,
						datetime.datetime.strptime(wish_list, self.TIMESTAMP_FORMAT),
					)
				)
			except ValueError:
				pass

		if not names_times:
			return

		sorted_pairs = sorted(names_times, key=lambda item: item[1], reverse = True)

		for name, time in sorted_pairs:
			with open(os.path.join(self.LOCAL_LISTS_PATH, name), 'r') as f:
				yield self._strategy.deserialize(WishList, f.read())

	def _get_current_local_list(self) -> t.Optional[WishList]:
		try:
			return self._get_all_local_lists().__next__()
		except StopIteration:
			return None

	@classmethod
	def _persist_list(cls, wish_list: WishList) -> None:
		if not os.path.exists(cls.LOCAL_LISTS_PATH):
			os.makedirs(cls.LOCAL_LISTS_PATH)

		with open(
			os.path.join(
				cls.LOCAL_LISTS_PATH,
				datetime.datetime.strftime(
					datetime.datetime.today(),
					cls.TIMESTAMP_FORMAT,
				),
			),
			'w',
		) as f:
			f.write(JsonId.serialize(wish_list))

	def check_and_update(self) -> bool:
		local_list = self._get_current_local_list()
		try:
			remote_list = self._fetcher.fetch()
		except WishFetchException:
			return False

		if local_list is None or local_list != remote_list:
			self._persist_list(remote_list)
			return True

		return False

	def load(self) -> WishList:
		wish_list = self._get_current_local_list()

		if wish_list is None:
			if not self.check_and_update():
				raise WishLoadException()
			return self._get_current_local_list()

		return wish_list

	def all_cubes(self) -> t.Iterator[WishList]:
		if self._get_current_local_list() is None:
			if not self.check_and_update():
				raise WishLoadException()

		return self._get_all_local_lists()