
import os

import appdirs


APP_DATA_DIR = appdirs.AppDirs('mkmcheck', 'mkmcheck').user_data_dir

RESOURCE_DIR = os.path.join(
	os.path.dirname(__file__),
	'resources',
)

CLIENT_SECRET_FILE = os.path.join(
	RESOURCE_DIR,
	'client_secret.json',
)

CREDENTIAL_PATH = os.path.join(
	RESOURCE_DIR,
	'storage.json'
)

CONFIG_PATH = os.path.join(
	RESOURCE_DIR,
	'mkmapikeys.cfg',
)