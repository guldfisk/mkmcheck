import os

import appdirs

from secretresources import paths


APP_DATA_DIR = appdirs.AppDirs('mkmcheck', 'mkmcheck').user_data_dir

SECRETS_PATH = paths.project_name_to_secret_dir('mkmcheck')

CLIENT_SECRET_FILE = os.path.join(
	SECRETS_PATH,
	'client_secret.json',
)

CREDENTIAL_PATH = os.path.join(
	SECRETS_PATH,
	'storage.json'
)

CONFIG_PATH = os.path.join(
	SECRETS_PATH,
	'mkmapikeys.cfg',
)