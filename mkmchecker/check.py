
import time

from mtgorp.db.load import Loader as DbLoader

from mtgorp.models.persistent.attributes.borders import Border

from mkmchecker.market.load import MarketLoader
from mkmchecker.wishload.fetch import WishFetcher
from mkmchecker.evaluation.evaluate import Evaluator, StandardWishingStrategy, EvaluationPersistor
from mkmchecker.updatesheet import update


class Timer(object):

	def __init__(self):
		self._current_time = 0

	def middle_time(self):
		v = time.time() - self._current_time
		self._current_time = time.time()
		return v


def check():

	timer = Timer()
	timer.middle_time()

	db_loader = DbLoader()
	db = db_loader.load()

	evaluation_persistor = EvaluationPersistor(db)

	print('db loaded', timer.middle_time())

	wish_fetcher = WishFetcher(db)
	wish_list = wish_fetcher.fetch()

	print('wishes fetched', timer.middle_time())

	# cardboard = db.cardboards['The Rack']
	# wish = SingleCardboardWish(cardboard, (IsEnglish(True), IsBorder(Border.BLACK), IsPlayset(False)), 1.)
	# wish_list = WishList((wish,))
	# cardboards = [cardboard]

	market_loader = MarketLoader(db)
	# market = market_loader.update(wish_list.cardboards, clear_cache_when_done = False)
	market = market_loader.load()

	print('market loaded', timer.middle_time())

	evaluator = Evaluator(market, wish_list, StandardWishingStrategy)

	evaluated_market = evaluator.evaluate()

	print('market evaluated', timer.middle_time())

	evaluation_persistor.save(evaluated_market, 'test')

	print('evaluation persisted', timer.middle_time())

	# evaluated_market = evaluation_persistor.load('test')
	#
	# print('evaluation loaded', timer.middle_time())

	# for seller in evaluated_market.sellers:
	# 	print(len(seller.articles))

	# update.update_sheet(evaluated_market)
	#
	# print('sheet updated', timer.middle_time())


if __name__ == '__main__':
	check()
