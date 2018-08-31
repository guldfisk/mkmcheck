import typing as t

import numpy as np

import requests

from mtgorp.db.database import CardDatabase
from mtgorp.models.persistent.cardboard import Cardboard

from mkmchecker.wishlist.wishlist import (
	WishList,
	Wish,
	IsEnglish,
	IsPlayset,
)


def tsv_to_ndarray(value: str, separator: str = '\t', line_separator: str = '\n') -> np.ndarray:
	rows = value.split(line_separator)

	matrix = [
		row.split(separator)
		for row in
		rows
	]

	row_length = max(map(len, matrix))

	for row in matrix:
		for i in range(row_length - len(row)):
			row.append('')

	return np.asarray(matrix, dtype=str)


class WishFetchException(Exception):
	pass


class WishFetcher(object):

	SHEET_ID = '1zhZuAAAYZk_f3lCsi0oFXXiRh5jiSMydurKnMYR6HJ8'

	def __init__(self, db: CardDatabase):
		self._db = db

	@classmethod
	def _fetch_tsv(cls, sheet_id: str) -> str:
		response = requests.get(
			f'https://docs.google.com/spreadsheets/d/{sheet_id}/pub?gid=965903062&single=true&output=tsv'
		)

		if not response.ok:
			raise WishFetchException(response.status_code)

		return response.content.decode('UTF-8')

	def _parse_wish(self, name: str, weight: str, requirement: str) -> t.Optional[Wish]:
		try:
			cardboard = self._db.cardboards[name]
		except KeyError:
			print(f'invalid cardboard: "{name}"')
			return None

		return Wish(
			cardboard,
			(
				IsEnglish(True),
				IsPlayset(False),
			),
			float(weight),
		)

	def fetch(self) -> WishList:
		wishes = []

		for row in tsv_to_ndarray(self._fetch_tsv(self.SHEET_ID))[1:]:
			parsed = self._parse_wish(*row[:3])
			if parsed:
				wishes.append(parsed)

		return WishList(wishes)