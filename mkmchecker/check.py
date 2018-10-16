import time

from mtgorp.db.load import Loader as DbLoader

from mkmchecker.evaluation.evaluate import Evaluator, StandardWishingStrategy
from mkmchecker.market.load import MarketLoader
from mkmchecker.updatesheet import update
from mkmchecker.wishload.load import WishListLoader


class Timer(object):

	def __init__(self):
		self._current_time = 0

	def middle_time(self):
		v = time.time() - self._current_time
		self._current_time = time.time()
		return v


def check(update_market: bool = True, update_wish_list: bool = True) -> None:
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

	print('wishes fetched', timer.middle_time())

	market_loader = MarketLoader(db)

	if update_market:
		market = market_loader.update(wish_list.cardboards, clear_cache_when_done = True)
	else:
		market = market_loader.load()

	print('market loaded', timer.middle_time())

	evaluator = Evaluator(market, wish_list, StandardWishingStrategy)
	evaluated_market = evaluator.evaluate()

	print('market evaluated', timer.middle_time())

	# update.update_sheet(evaluated_market)
	#
	# print('sheet updated', timer.middle_time())


def run() -> None:
	check(
		update_market = False,
		update_wish_list = False,
	)


if __name__ == '__main__':
	run()