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


def test_get_all_integration_error_logs(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_integration_logs_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_integration_logs_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert test_output["outputs"][key].get("error") is not None
        assert command_results.outputs_prefix == "Integration Error Data"
        assert len(test_output["outputs"][key].keys()) == 2


def test_delete_integration_error_logs(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_integration_connector_logs_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_integration_connector_logs_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        if key == "fail":
            assert test_output["outputs"][key].get("errorCode") is not None
            assert test_input[key]["args"]["Connector ID"] in test_output["outputs"][key].get("errorMessage")
            continue
        else:
            assert test_output["outputs"][key].get("error") is not None
        assert command_results.outputs_prefix == "errors_cleared"
        assert command_results.readable_output == tableToMarkdown(
            name="Integration Connector errors Status", t=command_results.outputs,
            headers=["error", "result"])


def test_return_rotated_verification_token(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_rotate_token_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_rotate_token_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "secret"
        assert command_results.readable_output == tableToMarkdown(
            name="new Token Details", t=command_results.outputs,
            headers=["secret"])

        assert command_results.outputs == test_output["outputs"][key].get("data").get("secret")
        assert test_output["outputs"][key].get("data") is not None


def test_get_all_tests_summary(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_all_tests_summary_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_all_tests_summary_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "tests_data"
        assert command_results.outputs == {"tests_data": test_output["outputs"][key]}
        for test in test_output["outputs"][key]:
            assert test["status"] == test_input[key]["args"]["Status"]
        assert len(test_output["outputs"][key]) <= test_input[key]["args"]["Entries per Page"]


def test_get_all_tests_summary_with_plan_id(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_all_tests_summary_with_plan_id_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_all_tests_summary_with_plan_id_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        if key == "success":
            assert bool(test_input[key]["args"]["Plan ID"]) is True
        else:
            assert bool(test_input[key]["args"]["Plan ID"]) is False
        assert command_results.outputs_prefix == "tests_data"
        assert command_results.outputs == {"tests_data": test_output["outputs"][key]}
        for test in test_output["outputs"][key]:
            assert test["status"] == test_input[key]["args"]["Status"]
        assert len(test_output["outputs"][key]) <= test_input[key]["args"]["Entries per Page"]


def test_delete_test_result_of_test(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_test_results_of_test_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_test_results_of_test_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        if key == "success":
            assert bool(test_input[key]["args"]["Test ID"]) is True
        else:
            assert bool(test_input[key]["args"]["Test ID"]) is False
            continue
        assert command_results.outputs_prefix == "deleted_test_results"
        assert command_results.readable_output == tableToMarkdown(
            name="Deleted Test", t=command_results.outputs,
            headers=["id"])
        assert command_results.outputs == [test_output["outputs"][key].get("data", {}).get("id")]
