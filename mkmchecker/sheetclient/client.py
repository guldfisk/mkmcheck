import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
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
APPLICATION_NAME = 'mkmchk'


def get_credentials():
	store = Storage(CREDENTIAL_PATH)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store)
	return credentials

def update_sheet(sheet_id: str, range_name: str, values):
	discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build(
		'sheets',
		'v4',
		http=http,
		discoveryServiceUrl=discovery_url,
	)
	update_values = {
		'values': values
	}
	result = service.spreadsheets().values().update(
		spreadsheetId = sheet_id,
		range = range_name,
		valueInputOption = 'RAW',
		body = update_values,
	).execute()
	print(result)


if __name__ == '__main__':
	pass
