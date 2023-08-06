import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from django.conf import settings

from lino.api import dd

try:
    import argparse

    tools_argparser = tools.argparser
    tools_argparser.add_argument('runserver', action="store")
    # flags = argparse.ArgumentParser(parents=[tools_argparser]).parse_args()
    # flags.add_argument('runserver', action="store", dest="runserver")
    # flags = flags.parse_args()
except ImportError:
    flags = None


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials',settings.SITE.verbose_name)
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'people.googleapis.com-python-quickstart.json')
    # credential_path = CLIENT_SECRET_FILE

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(
            dd.plugins.googleapi.client_secret_file, dd.plugins.googleapi.scopes)
        flow.user_agent = dd.plugins.googleapi.application_name
        # flags = argparse.ArgumentParser(description='This is a PyMOTW sample program').parse_args()
        if flags:
            credentials = tools.run_flow(flow, store,flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('people', 'v1', http=http)
