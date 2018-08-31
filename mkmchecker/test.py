
import json

import numpy as np

from mtgorp.db.load import Loader as DbLoader
from mtgorp.models.serilization.strategies.jsonid import JsonId

from mkmchecker.market.update import MarketFetcher
from mkmchecker.market.model import Market
from mkmchecker.market.update import Requester
from mkmchecker.values.values import Condition
from mkmchecker.wishlist.wishlist import WishList, SingleCardboardWish
from mkmchecker.wishload.load import WishListLoader
from mkmchecker.wishload.fetch import WishFetcher


def test():

	db_loader = DbLoader()

	db = db_loader.load()

	checker = MarketFetcher(db)

	strategy = JsonId(db)

	cardboard = db.cardboards['Tarmogoyf']

	wish = SingleCardboardWish(cardboard, (), 1.)

	wishes = WishList((wish,))

	market = checker.fetch(wishes)

	# print(
	# 	np.percentile(market.get_prices_for_cardboard(cardboard), 10)
	# )

	s = strategy.serialize(market)

	returned_market = strategy.deserialize(Market, s)

	print(
		list(
			seller.name
			for seller in
			returned_market.sellers
		)
	)


def alt_test():
	db_loader = DbLoader()

	db = db_loader.load()

	wish_fetcher = WishFetcher(db)

	wish_list, cardboards = wish_fetcher.fetch()

	print(wish_list)
	print(cardboards)


if __name__ == '__main__':
	alt_test()