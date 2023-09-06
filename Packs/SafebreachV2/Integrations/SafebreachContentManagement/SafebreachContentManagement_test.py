import pytest
from CommonServerPython import *
from SafebreachContentManagement import Client
SERVER_URL = 'https://test_url.com'


def util_load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.loads(f.read())


@pytest.fixture()
def client():
    return Client(api_key='test', account_id=None, base_url=SERVER_URL,
                  verify=True)
