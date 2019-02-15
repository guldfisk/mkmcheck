import typing as t

from mtgorp.db.database import CardDatabase

from mkmcheck.wishlist.parse import WishParser, WishParseException, Wish
from mkmcheck.model.models import WishList
from sheetclient.client import GoogleSheetClient

class WishFetchException(Exception):
	pass


class WishListFetcher(object):

	_START_COLUMN = 2
	_START_ROW = 4
	_END_COLUMN = _START_COLUMN + 2
	_END_ROW = 1000

	def __init__(self, db: CardDatabase, spreadsheet_id: str, sheet_name: str):
		self._wish_parser = WishParser(db)
		self._sheet_client = GoogleSheetClient(spreadsheet_id)

		self._sheet_name = sheet_name

	def fetch_wishes(self, included_suspended: bool = False, collect_errors: bool = True) -> t.Iterable[t.Optional[Wish]]:
		exceptions = []

		for values in self._sheet_client.read_sheet(
			sheet_name=self._sheet_name,
			start_column=self._START_COLUMN,
			start_row=self._START_ROW,
			end_column=self._END_COLUMN,
			end_row=self._END_ROW,
		):
			s, weight = values[:2]
			status = values[2] if len(values) >= 3 else ''

			if status == 'suspended' or status == 'ignored':
				if included_suspended:
					yield None
				continue

			try:
				weight = int(weight)
			except ValueError:
				e = WishParseException(f'Invalid weight "{weight}"')
				if collect_errors:
					exceptions.append((s, weight, e))
				else:
					raise e
				continue

			try:
				wish = self._wish_parser.parse(s)
			except WishParseException as e:
				if collect_errors:
					exceptions.append((s, weight, e))
				else:
					raise e
				continue

			wish.weight = weight
			yield wish

		if exceptions:
			raise WishParseException('\n'.join(str(item) for item in exceptions))

	def fetch(self) -> WishList:
		return WishList(
			wishes = list(
				self.fetch_wishes(
					included_suspended = False,
					collect_errors = True,
				)
			)
		)