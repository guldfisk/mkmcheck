
import time

from mtgorp.db.load import Loader as DbLoader

from mtgorp.models.persistent.attributes.borders import Border

from mkmchecker.market.load import MarketLoader
from mkmchecker.wishload.fetch import WishFetcher
from mkmchecker.wishload.load import WishListLoader
from mkmchecker.evaluation.evaluate import Evaluator, StandardWishingStrategy, EvaluationPersistor
from mkmchecker.updatesheet import update


class Timer(object):

	def __init__(self):
		self._current_time = 0

	def middle_time(self):
		v = time.time() - self._current_time
		self._current_time = time.time()
		return v


def full_check():

	timer = Timer()
	timer.middle_time()

	db_loader = DbLoader()
	db = db_loader.load()

	print('db loaded', timer.middle_time())

	wish_loader = WishListLoader(db)

	if wish_loader.check_and_update():
		print('wish list updated')

	wish_list = wish_loader.load()

	print('wishes fetched', timer.middle_time())

	market_loader = MarketLoader(db)
	market = market_loader.update(wish_list.cardboards, clear_cache_when_done = True)

	print('market loaded', timer.middle_time())

	evaluator = Evaluator(market, wish_list, StandardWishingStrategy)
	evaluated_market = evaluator.evaluate()

	print('market evaluated', timer.middle_time())

	update.update_sheet(evaluated_market)

	print('sheet updated', timer.middle_time())


if __name__ == '__main__':
	full_check()
