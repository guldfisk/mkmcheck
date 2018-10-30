import time

from mtgorp.db.load import Loader as DbLoader

from mkmcheck.evaluation.evaluate import Evaluator, StandardWishingStrategy, EvaluationPersistor, EvaluatedSellers
from mkmcheck.market.load import MarketLoader
from mkmcheck.updatesheet import update
from mkmcheck.wishload.load import WishListLoader, WishFetchException


class Timer(object):

	def __init__(self):
		self._current_time = 0

	def middle_time(self):
		v = time.time() - self._current_time
		self._current_time = time.time()
		return v


_LAST_EVALUATION_NAME = '.last_evaluation'


class CheckException(Exception):
	pass


def check(
	update_market: bool = True,
	update_wish_list: bool = True,
	update_sheet: bool = True,
	persist_evaluation: bool = False,
	clear_cache_when_done: bool = True,
) -> EvaluatedSellers:

	timer = Timer()
	timer.middle_time()

	db_loader = DbLoader()
	db = db_loader.load()

	print('db loaded', timer.middle_time())

	wish_loader = WishListLoader(db)

	if update_wish_list:
		if wish_loader.check_and_update():
			print('wish list updated')

	wish_list = wish_loader.load()

	print('wishes loaded', timer.middle_time())

	market_loader = MarketLoader(db)

	if update_market:
		market = market_loader.update(
			wish_list.cardboards,
			clear_cache_when_done = clear_cache_when_done,
		)
	else:
		market = market_loader.load()

	print('market loaded', timer.middle_time())

	evaluated_sellers = Evaluator(market, wish_list, StandardWishingStrategy).evaluate()

	print('market evaluated', timer.middle_time())

	if persist_evaluation:
		evaluation_persistor = EvaluationPersistor(db=db)

		evaluation_persistor.save(evaluated_sellers, _LAST_EVALUATION_NAME)

		print('market persisted', timer.middle_time())

	if update_sheet:
		if update_wish_list:
			try:
				changed = wish_loader.check_and_update()
			except WishFetchException:
				changed = True

			if changed:
				raise CheckException('Attempting to update sheet with modified wish list')

		update.update_sheet(evaluated_sellers)

		print('sheet updated', timer.middle_time())

	return evaluated_sellers


def run() -> None:
	check(
		update_market = False,
		update_wish_list = False,
		update_sheet = False,
		persist_evaluation = False,
		clear_cache_when_done = False,
	)


if __name__ == '__main__':
	run()