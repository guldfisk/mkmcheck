

from mkmcheck import ScopedSession, SHEET_ID, INPUT_SHEET_NAME, db, engine

from mkmcheck.model import models
from mkmcheck.wishload.fetch import WishListFetcher
from mkmcheck.market.update import MarketFetcher
from mkmcheck.evaluation.evaluate import Evaluator, StandardEvaluationStrategy
from mkmcheck.updatesheet.update import SheetsUpdater
from mkmcheck.utilities.logging import Timer




def check(
	recheck_wish_list: bool = True,
	recheck_market: bool = False,
	update_output_sheet: bool = True,
	update_knapsack_sheet: bool = True,
	update_wish_list_sheet: bool = True,
):

	timer = Timer()

	models.create(engine)

	session = ScopedSession()

	wish_list = session.query(models.WishList).order_by(models.WishList.created_date.desc()).first()

	timer.update('local wish_list loaded')

	wish_list_fetcher = WishListFetcher(
		db = db,
		spreadsheet_id = SHEET_ID,
		sheet_name = INPUT_SHEET_NAME,
	)

	if recheck_wish_list or wish_list is None:

		fetched_wish_list = wish_list_fetcher.fetch()

		timer.update('wish_list fetched')

		if wish_list != fetched_wish_list:
			print('new wish_list')

			session.add(fetched_wish_list)
			session.commit()

			wish_list = fetched_wish_list

			print('wish_list persisted', timer.middle_time())

	print('wish_list:', wish_list)

	if recheck_market:
		market_fetcher = MarketFetcher(db)

		market = market_fetcher.fetch(wish_list)

		timer.update('remote market fetched')

		session.add(market)

		session.commit()

		timer.update('remote marked persisted')


	else:
		market = session.query(models.Market).order_by(models.Market.created_date.desc()).first()

		timer.update('local market loaded')

		if market is None:
			raise Exception('No local market')


	evaluator = Evaluator(
		market = market,
		evaluation_strategy = StandardEvaluationStrategy,
		wish_list = wish_list,
	)

	evaluator.evaluate()

	print('market evaluated', timer.middle_time())


	if update_output_sheet:
		sheet_updater = SheetsUpdater(evaluator, wish_list_fetcher)
		sheet_updater.update_sheets(
			update_output_sheet = update_output_sheet,
			update_knapsack_output_sheet = update_knapsack_sheet,
			update_wish_list = update_wish_list_sheet
		)

		print('sheets updated', timer.middle_time())

	print(f'check complete. total time: {timer.time()}')



def _check():
	check(
		recheck_wish_list = True,
		recheck_market = False,
		update_output_sheet = True,
		update_knapsack_sheet = True,
		update_wish_list_sheet = True,
	)


if __name__ == '__main__':
	_check()