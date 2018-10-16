import typing as t

import re
import requests

import numpy as np

from mtgorp.models.persistent.attributes.borders import Border
from mtgorp.db.database import CardDatabase
from mtgorp.models.persistent.cardboard import Cardboard

from mkmcheck.values.values import Condition
from mkmcheck.wishlist import wishlist
from mkmcheck.wishlist.wishlist import (
	WishList,
	Wish,
	Requirement,
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


class WishParseException(WishFetchException):
	pass


class WishFetcher(object):

	SHEET_ID = '1zhZuAAAYZk_f3lCsi0oFXXiRh5jiSMydurKnMYR6HJ8'

	_REQUIREMENT_PATTERN = re.compile('\s*(\w+)(:\s*([\w;]+))?')

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

	def _parse_requirements(self, requirements: str) -> t.Iterable[Requirement]:
		_requirements = []
		has_to_be_english = True
		can_be_playset = False
		can_be_foil = False
		can_be_signed = False
		can_be_altered = False

		for requirement in requirements.split(','):
			match = self._REQUIREMENT_PATTERN.match(requirement)

			if not match:
				raise WishParseException(f'Invalid requirement {match}')

			restriction = match.groups()[0].lower()
			value = match.groups()[2]

			if restriction == 'any_language':
				has_to_be_english = False

			elif restriction == 'playset_ok':
				can_be_playset = True

			elif restriction == 'foil_ok':
				can_be_foil = True

			elif restriction == 'signed_ok':
				can_be_signed = True

			elif restriction == 'alter_ok':
				can_be_altered = True

			elif restriction == 'minimum_amount':
				try:
					amount = int(value)
				except (TypeError, ValueError):
					raise WishParseException(f'Invalid amount {value}')

				_requirements.append(wishlist.MinimumAmount(amount))

			elif restriction == 'black_border_only':
				_requirements.append(wishlist.IsBorder(Border.BLACK))

			elif restriction == 'minimum_condition':
				try:
					condition = Condition(value)
				except ValueError:
					raise WishParseException(f'Invalid condition {value}')

				_requirements.append(wishlist.IsMinimumCondition(condition))

			elif restriction == 'from_expansions':

				if not value:
					raise WishParseException('No expansions specified')

				try:
					expansions = [self._db.expansions[code] for code in value.split(';')]
				except KeyError:
					raise WishParseException(f'Invalid expansion code in {value}')

				_requirements.append(wishlist.FromExpansions(expansions))

		if has_to_be_english:
			_requirements.append(wishlist.IsEnglish(True))

		if not can_be_playset:
			_requirements.append(wishlist.IsPlayset(False))

		if not can_be_foil:
			_requirements.append(wishlist.IsFoil(False))

		if not can_be_signed:
			_requirements.append(wishlist.IsSigned(False))

		if not can_be_altered:
			_requirements.append(wishlist.IsAltered(False))

		return _requirements


	def _parse_wish(self, name: str, weight: str, requirement: str) -> t.Optional[Wish]:
		try:
			cardboard = self._db.cardboards[name]
		except KeyError:
			print(f'invalid cardboard: "{name}"')
			return None

		return Wish(
			cardboard,
			self._parse_requirements(requirement),
			float(weight),
		)

	def fetch(self) -> WishList:
		wishes = []

		for row in tsv_to_ndarray(self._fetch_tsv(self.SHEET_ID))[1:]:
			parsed = self._parse_wish(*row[:3])
			if parsed:
				wishes.append(parsed)

		return WishList(wishes)