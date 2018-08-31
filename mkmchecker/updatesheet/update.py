import typing as t

from mkmchecker.evaluation.evaluate import EvaluatedMarket
from mkmchecker.market.model import Article
from mkmchecker.sheetclient import client


SHEET_ID = '1zhZuAAAYZk_f3lCsi0oFXXiRh5jiSMydurKnMYR6HJ8'
SHEET_NAME = '17'
START_COLUMN = 4
START_ROW = 1


def _num_to_col_letters(num):
	letters = ''

	while num:
		mod = (num - 1) % 26
		letters += chr(mod + 65)
		num = (num - 1) // 26

	return ''.join(reversed(letters))


def _coord_to_string(col, row) -> str:
	return (
		str(
			_num_to_col_letters(
				col
			)
		)
		+ str(row)
	)


def _update_grid(grid: t.Collection[t.Collection[str]]) -> None:
	range_name = '{}!{}:{}'.format(
		SHEET_NAME,
		_coord_to_string(START_COLUMN, START_ROW),
		_coord_to_string(START_COLUMN + len(grid[0]) + 1, START_ROW + len(grid) + 1),
	)

	client.update_sheet(
		sheet_id = SHEET_ID,
		range_name = range_name,
		values = grid,
	)


def _article_to_string(article: t.Optional[Article]) -> str:
	return '' if article is None else (
		str(article.price)
		+ ( f' {article.expansion.code}' if article.expansion is not None else '' )
		+ f' {article.condition.value}'
		+ ( '/ne' if not article.english else '' )
		+ ( '/ps' if article.playset else '' )
		+ ( '/si' if article.signed else '' )
		+ ( '/al' if article.altered else '' )
	)


def update_sheet(evaluated_market: EvaluatedMarket) -> None:
	_sellers = evaluated_market.sellers[:50]

	_update_grid(
		list(
			zip(
				*(
					[seller.seller.name] + [
						_article_to_string(article)
						for article in
						seller.articles
					]
					for seller in
					_sellers
				)
			)
		)
	)