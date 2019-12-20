from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import scoped_session

from mtgorp.db.load import Loader

from mkmcheck import paths


_loader = Loader()

db = _loader.load()

_parser = ConfigParser()
_parser.read(paths.DATABASE_CONFIG_PATH)
_keys = _parser['DEFAULT']

_values_parser = ConfigParser()
_values_parser.read(paths.VALUES_CONFIG_PATH)
_values = _values_parser['DEFAULT']

SHEET_ID = _values['target_sheet_id']

INPUT_SHEET_NAME = _values['input_sheet_name']

OUTPUT_SHEET_NAME = _values['output_sheet_name']
OUTPUT_SHEET_ID = int(_values['output_sheet_id'])

OUTPUT_KNAPSACK_SHEET_NAME = _values['output_knapsack_sheet_name']
OUTPUT_KNAPSACK_SHEET_ID = _values['output_knapsack_sheet_id']

TOP_SELLERS_AMOUNT = int(_values['top_sellers_amount'])
KNAPSACK_SEARCH_SPACE = int(_values['knapsack_search_space'])
KNAPSACK_CAPACITY = int(_values['knapsack_capacity'])


uri = '{dialect}+{driver}://{username}:{password}@{host}/{database}?charset=utf8'.format(**_keys)

print(uri)
engine = create_engine(
    # f'{_keys["dialect"]}+{_keys["driver"]}://'
    # f'{_keys["username"]}:{_keys["password"]}@{_keys["host"]}/{_keys["database"]}?charset=utf8',
    uri,
    pool_size = 32,
    echo = False,
)

session_factory = sessionmaker(bind=engine)
ScopedSession = scoped_session(session_factory)
