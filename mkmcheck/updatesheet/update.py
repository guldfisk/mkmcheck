
import typing as t

import itertools

from sheetclient.client import GoogleSheetClient

from mkmcheck.evaluation.evaluate import Evaluator, ConcludedWish
from mkmcheck.model.models import Wish
from mkmcheck.wishload.fetch import WishListFetcher
from mkmcheck import (
	SHEET_ID,
	OUTPUT_SHEET_NAME,
	TOP_SELLERS_AMOUNT,
	OUTPUT_SHEET_ID,
	OUTPUT_KNAPSACK_SHEET_NAME,
	OUTPUT_KNAPSACK_SHEET_ID,
	KNAPSACK_SEARCH_SPACE,
	KNAPSACK_CAPACITY,
	INPUT_SHEET_NAME,
)


def _seller_to_grid(
	concluded_wishes: t.Iterable[ConcludedWish],
	name: str,
	price: float,
	value: float,
) -> t.List[t.Tuple[str, str, str]]:
	return [
		(
			name,
			str(round(price, 1)),
			str(round(value, 1)),
		),
	] + [
		(
			str(concluded_wish.wish),
			str(concluded_wish),
			str(round(concluded_wish.value, 1)),
		)
		for concluded_wish in
		concluded_wishes
		if concluded_wish.include
	]


class SheetsUpdater(object):

	def __init__(self, evaluator: Evaluator, wish_list_fetcher: WishListFetcher):
		self._evaluator = evaluator
		self._wish_list_fetcher = wish_list_fetcher
		self._client = GoogleSheetClient(SHEET_ID)

	def _update_output_sheet(self) -> None:
		values = [
			list(
				itertools.chain(
					*row
				)
			)
			for row in
			itertools.zip_longest(
				*(
					_seller_to_grid(
						concluded_seller.sorted_concluded_wishes,
						concluded_seller.seller.name,
						concluded_seller.price,
						concluded_seller.value,
					)
					for concluded_seller in
					self._evaluator.concluded_sellers[:TOP_SELLERS_AMOUNT]
				),
				fillvalue=('', '', ''),
			)
		]

		self._client.clear_sheet(OUTPUT_SHEET_ID)
		self._client.update_sheet(
			sheet_name = OUTPUT_SHEET_NAME,
			start_column = 1,
			start_row = 1,
			values = values,
		)

		print('wish list sheet update done')

	def _update_knapsack_output_sheet(self) -> None:
		values = [
			list(
				itertools.chain(
					*row
				)
			)
			for row in
			itertools.zip_longest(
				*(
					_seller_to_grid(
						sorted(
							concluded_seller.get_knapsack_values(
								KNAPSACK_CAPACITY
							)[1],
							key=lambda w: w.value,
							reverse=True,
						),
						concluded_seller.seller.name,
						sum(
							concluded_wish.price
							for concluded_wish in
							concluded_seller.get_knapsack_values(
								KNAPSACK_CAPACITY
							)[1]
						),
						sum(
							concluded_wish.value
							for concluded_wish in
							concluded_seller.get_knapsack_values(
								KNAPSACK_CAPACITY
							)[1]
						),
					)
					for concluded_seller in
					sorted(
						self._evaluator.concluded_sellers[:KNAPSACK_SEARCH_SPACE],
						key=lambda s: s.get_knapsack_values(KNAPSACK_CAPACITY)[0],
						reverse=True,
					)[:TOP_SELLERS_AMOUNT]
				),
				fillvalue=('', '', ''),
			)
		]

		self._client.clear_sheet(OUTPUT_KNAPSACK_SHEET_ID)

		self._client.update_sheet(
			sheet_name = OUTPUT_KNAPSACK_SHEET_NAME,
			start_column = 1,
			start_row = 1,
			values = values,
		)

		print('knapsack sheet updated')

	def _update_wish_list(self) -> None:
		wishes = list(
			self._wish_list_fetcher.fetch_wishes(
				included_suspended = True,
				collect_errors = False,
			)
		)

		grid = []

		for concluded_seller in self._evaluator.concluded_sellers[:TOP_SELLERS_AMOUNT]:

			wish_map = {
				concluded_wish.wish:
					concluded_wish
				for concluded_wish in
				concluded_seller.concluded_wishes
			}  # type: t.Dict[Wish, ConcludedWish]

			column = [concluded_seller.seller.name, '']

			for wish in wishes:
				if wish is None:
					column.append('')
					continue

				concluded_wish = wish_map.get(wish, None)

				if concluded_wish is None:
					column.append('not in wish_list')
					continue

				if not concluded_wish.include:
					column.append('')
					continue

				column.append(str(concluded_wish))

			grid.append(column)

		start_column = 5
		start_row = 2

		self._client.update_sheet(
			INPUT_SHEET_NAME,
			start_column = start_column,
			start_row = start_row,
			values = list(zip(*grid)),
		)

		print('wish list input sheet updated')

	def update_sheets(
		self,
		update_output_sheet: bool = True,
		update_knapsack_output_sheet: bool = True,
		update_wish_list: bool = True,
	):
		if update_output_sheet:
			self._update_output_sheet()

		if update_knapsack_output_sheet:
			self._update_knapsack_output_sheet()

		if update_wish_list:
			self._update_wish_list()


