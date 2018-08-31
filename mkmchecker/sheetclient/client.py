import typing as t

import httplib2

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

from mkmchecker.paths import CLIENT_SECRET_FILE, CREDENTIAL_PATH
from mkmchecker.values.values import APPLICATION_NAME


SCOPES = 'https://www.googleapis.com/auth/spreadsheets'


def get_credentials() -> t.Any:
	store = Storage(CREDENTIAL_PATH)
	credentials = store.get()

	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		credentials = tools.run_flow(flow, store)

	return credentials


def update_sheet(sheet_id: str, range_name: str, values: t.Iterable[t.Iterable[str]]) -> None:
	discovery_url = 'https://sheets.googleapis.com/$discovery/rest?version=v4'

	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())

	service = discovery.build(
		'sheets',
		'v4',
		http = http,
		discoveryServiceUrl = discovery_url,
	)

	update_values = {'values': values}

	(
		service
		.spreadsheets()
		.values()
		.update(
			spreadsheetId = sheet_id,
			range = range_name,
			valueInputOption = 'RAW',
			body = update_values,
		)
		.execute()
	)