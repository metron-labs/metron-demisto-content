import pytest
from CommonServerPython import *
from SafebreachContentManagement import Client
import json
import demistomock as demisto
from importlib import import_module

safebreach_content_management = import_module("SafebreachContentManagement")
main = safebreach_content_management.main
safebreach_client = safebreach_content_management.Client
SERVER_URL = 'https://metron01.safebreach.com'


def util_load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.loads(f.read())


@pytest.fixture()
def client():
    return Client(api_key='api_key', account_id=1234567, base_url=SERVER_URL,
                  verify=True)


@pytest.fixture()
def demisto_mocker_sb(mocker):
    mocker.patch.object(demisto, 'params', return_value={
        'base_url': SERVER_URL,
        'api_key': 'api_key',
        'account_id': 1234567,
        'verify': True})
    # mocker.patch.object(demisto, 'getLastRun', return_value={'time': 1558541949000})
    # mocker.patch.object(demisto, 'incidents')
    # mocker.patch.object(demisto, 'results')


def test_get_all_users(mocker):
    test_data = util_load_json(path="test_data/safebreach_get_all_users_inputs.json")
    test_output = util_load_json(path="test_data/outputs/safebreach_get_all_users_outputs.json")
    mocker.patch.object(demisto, 'params', return_value={
        'base_url': SERVER_URL,
        'api_key': 'api_key',
        'account_id': 1234567,
        'verify': True})

    mocker.patch.object(demisto, 'command', return_value=test_data.get("command"))
    mocker.patch.object(demisto, 'args', return_value=test_data.get("args"))

    mocker.patch.object(safebreach_content_management, "return_results")
    mocker.patch.object(safebreach_client, 'get_response', return_value=test_data.get("get_response"))
    main()
    call = safebreach_content_management.return_results.call_args_list
    Command_results = call[0].args[0]

    assert Command_results.outputs_prefix == "user_data"
    assert Command_results.readable_output == tableToMarkdown(
        name="user data", t=Command_results.outputs, headers=['id', 'name', 'email'])
    assert Command_results.outputs == test_output.get("outputs")
    assert len(Command_results.outputs) == 2
