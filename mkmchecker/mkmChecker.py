import urllib.parse
import random
import time
import hmac
import base64
import hashlib
import json
import re
import os
import csv
import io
import math

import typing as t
import configparser as cfg

import requests
import numpy as np

import appdirs

from mkmchecker.sheetclient import client as gsclient

from mtgorp.db.load import Loader

from mkmchecker.paths import CONFIG_PATH


class Requester(object):

	config_path = CONFIG_PATH

	config = cfg.ConfigParser()
	config.read(config_path)

	# keys = config['DEFAULT']
	keys = config['Oliver']

	appToken = keys['appToken']
	appSecret = keys['appSecret']
	bAppSecret = appSecret.encode('UTF-8')
	accessToken = keys['accessToken']
	accessTokenSecret = keys['accessTokenSecret']
	bAccessTokenSecret = accessTokenSecret.encode('UTF-8')

	signature_key = bAppSecret + b'&' + bAccessTokenSecret

	user = 'guldfisk'

	order = [
		'oauth_consumer_key',
		'oauth_token',
		'oauth_nonce',
		'oauth_timestamp',
		'oauth_signature_method',
		'oauth_version', 'realm',
		'oauth_signature'
	]

	CHARS = 'abcdefghijklmnopqrstuvwxyz0123456789'

	@classmethod
	def get_nonce(cls, length: int = 13) -> str:
		# return ''.join(random.choice(cls.CHARS) for _ in range(length))

		u = ''
		for i in range(length):
			u+=random.choice(cls.CHARS)
		return u

	@classmethod
	def url_encode(cls, d: dict) -> str:
		# return ''.join(
		# 	urllib.parse.quote_plus(
		# 		f'{key}={d[key]}&'
		# 		for key in
		# 		sorted(d)
		# 	)
		# )[:-3]

		u = ''
		for key in sorted(d):
			u += urllib.parse.quote_plus(key + '=' + str(d[key]) + '&')
		return u[:-3]

	@classmethod
	def oauth_header_from_dict(cls, d: dict) -> str:
		# return 'OAuth ' + ', '.join(f'{key}="{value}"' for key, value in d.items())

		us = 'OAuth '

		for key in Requester.order:
			us += key + '="' + d[key]+ '", '

		return us[:-1]

	@classmethod
	def api_request(cls, resource: str) -> t.Any:
		print('requesting', resource)

		t_params = {
			'oauth_consumer_key': cls.appToken,
			'oauth_nonce': cls.get_nonce(),
			'oauth_signature_method': 'HMAC-SHA1',
			'oauth_timestamp': str(int(time.time())),
			'oauth_token': cls.accessToken,
			'oauth_version': '1.0'
		}

		uri = 'https://www.mkmapi.eu/ws/v1.1/output.json/' + resource
		params = cls.url_encode(t_params)

		auth = 'GET&' + urllib.parse.quote_plus(uri) + '&' + params
		signature = base64.b64encode(hmac.new(cls.signature_key, auth.encode('utf-8'), hashlib.sha1).digest())
		t_params['oauth_signature'] = signature.decode('utf-8')
		t_params['realm'] = uri

		header = {'Authorization': Requester.oauth_header_from_dict(t_params)}

		print(uri, header)

		response = requests.get(uri, headers=header)

		if not response.ok:
			raise Exception(response.status_code)

		print('request done', response)

		return response.json()


class Product(object):

	def __init__(self, name, weight=0):
		self.name = name
		self.sub_products = []
		self.weight = weight

	def populate_ids(self):
		self.sub_products = [
			{
				'id': str(item['idProduct']),
				'avg': item['priceGuide']['AVG']
			}
			for item in
			Requester.api_request('products/'+self.name+'/1/1/1')['product']
			if not item['expansion'][0:3]=='WCD'
		]
		if not self.sub_products:
			return
		min_avg = min(sub_product['avg'] for sub_product in self.sub_products)
		for sub_product in self.sub_products:
			sub_product['avg'] = min_avg

	def get_articles(self):
		if not self.sub_products:
			self.populate_ids()

		for sub_product in self.sub_products:
			for article in Requester.api_request('articles/'+sub_product['id'])['article']:
				current_article = Article(
					self.name,
					self.weight,
					article,
					sub_product['avg']
				)
				if filter_article(current_article):
					yield current_article

	def __str__(self):
		return f'{self.__class__.__name__}({self.name}, {self.weight})'

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name

	def __hash__(self):
		return hash((self.__class__, self.name))


class Article(object):

	def __init__(self, name, weight, values, avr_price=10):
		self.name = name
		self._weight = weight
		self.values = values
		self.avr_price = avr_price

	def __getitem__(self, key):
		return self.values[key]

	def get_seller(self):
		return self['seller']['username']

	@property
	def price(self):
		return self.values['price']

	@property
	def weight(self):
		return (
			1 / (1 + math.e ** ( - (self.avr_price - self.price) / 4))
			* 1 / (1 + math.e ** (self.price / 4 - 4))
			* self._weight ** 2.2
		)


class Seller(object):

	def __init__(self, name):
		self.name = name
		self.articles = dict()

	def add_article(self, article: Article):
		if article.name in self.articles:
			if article.weight > self.articles[article.name].weight:
				self.articles[article.name] = article
		else:
			self.articles[article.name] = article

	def get_total_weight(self):
		return np.sum([article.weight for article in self.articles.values()])

	def get_sorted_article_list(self):
		return sorted(
			sorted(
				self.articles.values(),
				key = lambda o: o.name,
			),
			key = lambda o: o.weight,
			reverse=True,
		)

	def __eq__(self, other):
		return isinstance(other, self.__class__) and self.name == other.name

	def __hash__(self):
		return hash(self.name)


def filter_article(article):
	conditions = {'MT': 1, 'NM': 0.9, 'EX': 0.8}
	if (
		not article['isAltered']
		and not article['isFoil']
		and not article['isSigned']
		and not article['isPlayset']
		and article['condition'] in conditions
		and article['language']['idLanguage']==1
		and article['price']<=article.avr_price*1.1+2
	):
		return article
	else:
		return None


SHEET_ID = '1zhZuAAAYZk_f3lCsi0oFXXiRh5jiSMydurKnMYR6HJ8'


def get_tsv():
	print('Get tsv')
	link = 'https://docs.google.com/spreadsheets/d/'+SHEET_ID+'/pub?gid=965903062&single=true&output=tsv'
	return requests.get(link)


def load_products():
	tsv = get_tsv()
	cardboards = Loader.load().cardboards
	print('cardboards loaded', len(cardboards))

	for row in csv.reader(io.StringIO(tsv.content.decode('UTF-8')), delimiter='\t'):
		name, weight = row[0:2]
		try:
			if not name in cardboards:
				print(name, 'not a cardboard!')
			yield Product(re.sub('[^a-z]', '', name, flags=re.IGNORECASE), int(weight))

		except (ValueError, IndexError) as e:
			print(name, 'not a cardboard', e)


def sorted_sellers(sellers: t.Iterable[Seller]) -> t.List[Seller]:
	return sorted(tuple(sellers), key=lambda o: o.get_total_weight(), reverse=True)


def sellers_to_json(sellers: t.Iterable[Seller]) -> str:
	return json.dumps(
		[
			(
				seller.name,
				{
					'weight': str(seller.get_total_weight()),
					'cards': [
						{
							'name': article.name,
							'price': article.values.get('price', '-')
						}
						for article in
						seller.get_sorted_article_list()
					],
				},
			)
			for seller in
			sorted_sellers(sellers)
		]
	)


def sellers_to_grid(sellers: t.Iterable[Seller], products: t.Iterable[Product]):
	return [[seller.name for seller in sellers]]+[
		[
			seller.articles[product.name].values.get('price', '-') if product.name in seller.articles else ''
			for seller in
			sellers
		]
		for product in
		products
	]


SHEET_NAME = '17'
START_COLUMN = 3
START_ROW = 1


def num_to_col_letters(num):
	letters = ''

	while num:
		mod = (num - 1) % 26
		letters += chr(mod + 65)
		num = (num - 1) // 26

	return ''.join(reversed(letters))


def coord_to_string(col, row) -> str:
	return (
		str(
			num_to_col_letters(
				col
			)
		)
		+ str(row)
	)


def update_grid(grid):
	range_name = '{}!{}:{}'.format(
		SHEET_NAME,
		coord_to_string(START_COLUMN, START_ROW),
		coord_to_string(START_COLUMN+len(grid[0])+1, START_ROW+len(grid)+1),
	)

	gsclient.update_sheet(
		sheet_id = SHEET_ID,
		range_name = range_name,
		values = grid,
	)


def download():
	random.seed()
	sellers = dict()
	products = tuple(load_products())

	for product in products:

		for article in product.get_articles():

			if not article.get_seller() in sellers:
				sellers[article.get_seller()] = Seller(article.get_seller())

			sellers[article.get_seller()].add_article(article)

	print('\nfinished requests\n')

	# if not os.path.exists(APP_PATH):
	# 	os.makedirs(APP_PATH)

	result = sellers.values(), products

	# with open(SELLERS_PATH, 'wb') as f:
	# 	pickle.dump(result, f)

	return result


def update_sheets(sellers: t.Iterable[Seller], products: t.Iterable[Product]):
	grid = sellers_to_grid(
		sorted_sellers(sellers)[0:50],
		products,
	)

	update_grid(grid)


def main():
	update_sheets(
		*download()
	)


def test():
	print(list(load_products()))


if __name__=='__main__':
	main()