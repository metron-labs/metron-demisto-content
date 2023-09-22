from collections.abc import Callable, Generator
import pytest
from pytest_mock import MockerFixture
from CommonServerPython import *
from SafebreachContentManagement import Client
import json
import demistomock as demisto
from importlib import import_module

safebreach_content_management = import_module("SafebreachContentManagement")
main = safebreach_content_management.main
safebreach_client = safebreach_content_management.Client
SERVER_URL = 'https://metron01.safebreach.com'
mock_sb_client = safebreach_client(api_key='api_key', account_id=1234567,
                                   base_url=SERVER_URL, verify=True)


def util_load_json(path):
    with open(path, encoding='utf-8') as f:
        return json.loads(f.read())


@pytest.fixture()
def client():
    return Client(api_key='api_key', account_id=1234567, base_url=SERVER_URL,
                  verify=True)


@pytest.fixture()
def demisto_mocker_sb(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    mocker.patch.object(demisto, 'params', return_value={
        'base_url': SERVER_URL,
        'api_key': 'api_key',
        'account_id': 1234567,
        'verify': True})


def modify_mocker_with_common_data(mocker, test_input_data, test_output_data):

    mocker.patch.object(demisto, 'command',
                        return_value=test_input_data.get("command"))
    mocker.patch.object(
        demisto, 'args', return_value=test_input_data.get("args"))

    mocker.patch.object(safebreach_content_management, "return_results")
    mocker.patch.object(safebreach_client, 'get_response',
                        return_value=test_output_data)

    return mocker


def test_get_simulator_quota_with_table(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_simulator_quota_with_table_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_simulator_quota_with_table_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        if key == "success":
            main()
            call = safebreach_content_management.return_results.call_args_list
            command_results = call[0].args[0]
            assert command_results.outputs_prefix == "account_details"
            assert command_results.outputs.get("account_details") == test_output["outputs"][key].get("data")
            assert command_results.outputs.get("simulator_quota") == test_output["outputs"][key].get("data").get("nodesQuota")


def test_get_all_simulator_details(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_all_simulator_details_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_all_simulator_details_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "simulator_details"
        assert command_results.outputs == test_output["outputs"][key].get("data").get("rows")
        assert len(test_output["outputs"][key].get("data").get("rows")) == test_output["outputs"][key].get("data").get("count")


def test_get_simulator_with_name(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_simulator_with_name_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_simulator_with_name_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, "get_simulators_details", returns=test_output["outputs"][key])
        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "simulator_details_with_name"
        # assert command_results.outputs == test_output["outputs"][key]


def test_delete_simulator_with_given_name(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_simulator_with_given_name_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_simulator_with_given_name_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, "get_simulators_details", returns=test_output["outputs"][key])
        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "deleted_simulator_details"
        assert command_results.outputs == test_output["outputs"][key].get("data")


def test_update_simulator_with_given_name(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_update_simulator_with_given_name_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_update_simulator_with_given_name_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, "get_simulators_details", returns=test_output["outputs"][key])
        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "deleted_simulator_details"
        assert command_results.outputs == test_output["outputs"][key].get("data")
