import typing as t

import re
import urllib.parse
import random
import time
import hmac
import base64
import hashlib
import requests
import datetime
import ast

import configparser as cfg
from promise import Promise
from concurrent.futures import ThreadPoolExecutor, Executor

from mtgorp.db.database import CardDatabase

from mkmcheck import paths
from mkmcheck.model.models import Article, Seller, Market, WishList, RequestCache
from mkmcheck.values.values import Condition, Language

from mkmcheck import ScopedSession


class Requester(object):

    CONFIG = cfg.ConfigParser()
    CONFIG.read(paths.CONFIG_PATH)

    KEYS = CONFIG['CURRENT']

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


class MarketFetcher(object):

    _MKM_NAMEIFYER_PATTERN = re.compile('[^a-z]', flags=re.IGNORECASE)

    def __init__(self, db: CardDatabase, executor: t.Optional[Executor] = None):
        self._db = CardDatabase
        self._executor = ThreadPoolExecutor(32) if executor is None else executor

        self._expansion_name_map = {
            expansion.name if expansion.mkm_name is None else expansion.mkm_name:
                expansion.code
            for expansion in
            db.expansions.values()
        }

        self._start_time = datetime.datetime.utcnow()
        self._max_cache_age = datetime.timedelta(days=1)

    @classmethod
    def _cardboard_name_to_mkm_name(cls, cardboard_name: str) -> str:
        return cls._MKM_NAMEIFYER_PATTERN.sub('', cardboard_name)

    def _cached_request(self, resource: str) -> t.Any:
        session = ScopedSession()
        cache = (
            session
                .query(RequestCache)
                .filter(RequestCache.request == resource)
                .one_or_none()
        ) #type: t.Optional[RequestCache]

        if cache is None or self._start_time - cache.time_stamp > self._max_cache_age:
            cache = RequestCache(
                request = resource,
                response = Requester.api_request(resource),
            )
            session.merge(cache)
            session.commit()
            return cache.response

        return ast.literal_eval(cache.response)

    def _get_printing_products(
        self,
        cardboard_name: str,
    ) -> t.Iterable[t.Tuple[str, str, t.Dict[str, t.Any]]]:
        for product in (
            self._cached_request(
                f'products/{self._cardboard_name_to_mkm_name(cardboard_name)}/1/1/1'
            )['product']
        ):
            expansion_name = product['expansion']
            if not expansion_name[:3] == 'WCD':
                yield cardboard_name, expansion_name, product

    def _get_articles(
        self,
        cardboard_name: str,
        expansion_code: str,
        printing_product: t.Dict,
    ) -> t.Iterable[t.Dict[str, t.Any]]:
        response = self._cached_request(f'articles/{printing_product["idProduct"]}')
        for article in response['article']:
            article['cardboard_name'] = cardboard_name
            article['expansion_code'] = self._expansion_name_map.get(expansion_code)
            yield article

    @classmethod
    def _article(cls, d: t.Dict[str, t.Any]) -> Article:
        return Article(
            cardboard_name = d['cardboard_name'],
            price = d['price'],
            amount = d['count'],
            expansion_code = d['expansion_code'],
            condition = Condition(d['condition']),
            is_foil = d['isFoil'],
            is_signed = d['isSigned'],
            is_altered = d['isAltered'],
            language = Language(d['language']['idLanguage']),
            is_playset = d['isPlayset'],
        )

    def fetch(self, wish_list: WishList) -> Market:

        unique_cardboard_names = set(wish_list.cardboard_names)

        printing_product_sets = Promise.all(
            [
                Promise.resolve(
                    self._executor.submit(
                        lambda _cardboard: list(self._get_printing_products(_cardboard)),
                        cardboard,
                    )
                )
                for cardboard in
                unique_cardboard_names
            ]
        ).get() #type: t.List[t.List[t.Tuple[str, str, t.Dict[str, t.Any]]]]

        # printing_product_sets = [
        # 	list(self._get_printing_products(cardboard))
        # 	for cardboard in
        # 	unique_cardboard_names
        # ] #type: t.List[t.List[t.Tuple[str, str, t.Dict[str, t.Any]]]]

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

        # article_sets = [
        # 	list(self._get_articles(*printing_product))
        # 	for printing_product_set in
        # 	printing_product_sets
        # 	for printing_product in
        # 	printing_product_set
        # ]

        sellers = {} #type: t.Dict[str, t.List[Article]]

        for article in (article for article_set in article_sets for article in article_set):
            _article = self._article(article)

            try:
                sellers[article['seller']['username']].append(_article)
            except KeyError:
                sellers[article['seller']['username']] = [_article]

        _sellers = list(
            Seller(
                name = name,
                articles = articles,
            )
            for name, articles in
            sellers.items()
        )

        return Market(
            sellers = _sellers,
            wish_list = wish_list,
        )