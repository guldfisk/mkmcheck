import typing as t

import re
import urllib.parse
import random
import time
import hmac
import base64
import hashlib
import requests

import configparser as cfg
from promise import Promise
from concurrent.futures import ThreadPoolExecutor, Executor

from mtgorp.db.database import CardDatabase
from mtgorp.models.persistent.expansion import Expansion
from mtgorp.models.persistent.cardboard import Cardboard

from mkmcheck import paths
from mkmcheck.market.model import Article, Seller, Market
from mkmcheck.values.values import Condition
from mkmcheck.market.cache import Cacher


class Requester(object):

	CONFIG = cfg.ConfigParser()
	CONFIG.read(paths.CONFIG_PATH)

	KEYS = CONFIG['Oliver']

	APP_TOKEN = KEYS['appToken']
	APP_SECRET = KEYS['appSecret']
	B_APP_SECRET = APP_SECRET.encode('UTF-8')
	ACCESS_TOKEN = KEYS['accessToken']
	ACCESS_TOKEN_SECRET = KEYS['accessTokenSecret']
	B_ACCESS_TOKEN_SECRET = ACCESS_TOKEN_SECRET.encode('UTF-8')

	SIGNATURE_KEY = B_APP_SECRET + b'&' + B_ACCESS_TOKEN_SECRET

	ORDER = [
		'oauth_consumer_key',
		'oauth_token',
		'oauth_nonce',
		'oauth_timestamp',
		'oauth_signature_method',
		'oauth_version', 'realm',
		'oauth_signature'
	]

	CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'

	CACHER = Cacher()

	@classmethod
	def _get_nonce(cls, length: int = 13) -> str:
		return ''.join(random.choice(cls.CHARS) for _ in range(length))

	@classmethod
	def _url_encode(cls, d: t.Dict) -> str:
		return ''.join(
			urllib.parse.quote_plus(key + '=' + str(d[key]) + '&')
			for key in
			sorted(d)
		)[:-3]

	@classmethod
	def _oauth_header_from_dict(cls, d: dict) -> str:
		return 'OAuth ' + ', '.join(f'{key}="{value}"' for key, value in d.items())

	@classmethod
	def api_request(cls, resource: str) -> t.Any:
		t_params = {
			'oauth_consumer_key': cls.APP_TOKEN,
			'oauth_nonce': cls._get_nonce(),
			'oauth_signature_method': 'HMAC-SHA1',
			'oauth_timestamp': str(int(time.time())),
			'oauth_token': cls.ACCESS_TOKEN,
			'oauth_version': '1.0'
		}

		uri = 'https://api.cardmarket.com/ws/v1.1/output.json/' + resource
		params = cls._url_encode(t_params)

		auth = 'GET&' + urllib.parse.quote_plus(uri) + '&' + params
		signature = base64.b64encode(hmac.new(cls.SIGNATURE_KEY, auth.encode('utf-8'), hashlib.sha1).digest())
		t_params['oauth_signature'] = signature.decode('utf-8')
		t_params['realm'] = uri

		header = {'Authorization': Requester._oauth_header_from_dict(t_params)}

		while True:
			try:
				response = requests.get(uri, headers=header)
				break
			except requests.ConnectionError as e:
				print(e)

		if not response.ok:
			raise Exception(response.status_code)

		return response.json()

	@staticmethod
	@CACHER
	def cached_request(resource: str) -> t.Any:
		return Requester.api_request(resource)

	@classmethod
	def clear_cache(cls) -> None:
		cls.CACHER.clear()


class MarketFetcher(object):

	def __init__(self, db: CardDatabase, executor: t.Optional[Executor] = None):
		self._db = CardDatabase
		self._executor = ThreadPoolExecutor(32) if executor is None else executor

		self._expansion_name_map = {
			expansion.name if expansion.mkm_name is None else expansion.mkm_name:
				expansion
			for expansion in
			db.expansions.values()
		}

	@classmethod
	def _cardboard_to_mkm_name(cls, cardboard: Cardboard) -> str:
		return re.sub('[^a-z]', '', cardboard.name, flags=re.IGNORECASE)

	def _get_printing_products(
		self,
		cardboard: Cardboard,
	) -> t.Iterable[t.Tuple[Cardboard, t.Optional[Expansion], t.Dict]]:
		for product in (
			Requester.cached_request(
				f'products/{self._cardboard_to_mkm_name(cardboard)}/1/1/1'
			)['product']
		):
			expansion_name = product['expansion']
			if not expansion_name[:3] == 'WCD':
				yield cardboard, self._expansion_name_map.get(expansion_name), product

	@classmethod
	def _get_articles(
		cls,
		cardboard: Cardboard,
		expansion: t.Optional[Expansion],
		printing_product: t.Dict,
	) -> t.Iterable[t.Dict]:
		response = Requester.cached_request(f'articles/{printing_product["idProduct"]}')
		for article in response['article']:
			article['cardboard'] = cardboard
			article['expansion'] = expansion
			yield article

	@classmethod
	def _article(cls, d: t.Dict) -> Article:
		return Article(
			cardboard = d['cardboard'],
			price = d['price'],
			condition = Condition(d['condition']),
			foil = d['isFoil'],
			signed = d['isSigned'],
			altered = d['isAltered'],
			english = d['language']['idLanguage'] == 1,
			playset = d['isPlayset'],
			expansion = d['expansion'],
			count = d['count'],
		)

	def fetch(self, cardboards: t.Iterable[Cardboard], *, clear_cache_when_done: bool = True) -> Market:
		cardboards = list(cardboards)

		printing_product_sets = Promise.all(
			[
				Promise.resolve(
					self._executor.submit(
						lambda _cardboard: list(self._get_printing_products(_cardboard)),
						cardboard,
					)
				)
				for cardboard in
				cardboards
			]
		).get()

		article_sets = Promise.all(
			[
				Promise.resolve(
					self._executor.submit(
						lambda _printing_product: list(self._get_articles(*_printing_product)),
						printing_product,
					)
				)
				for printing_product_set in
				printing_product_sets
				for printing_product in
				printing_product_set
			]
		).get()

		sellers = {} #type: t.Dict[str, t.List[Article]]

		for article in (article for article_set in article_sets for article in article_set):
			_article = self._article(article)

			try:
				sellers[article['seller']['username']].append(_article)
			except KeyError:
				sellers[article['seller']['username']] = [_article]

		_sellers = (Seller(name, articles) for name, articles in sellers.items())

		if clear_cache_when_done:
			Requester.clear_cache()

		return Market(_sellers, cardboards)