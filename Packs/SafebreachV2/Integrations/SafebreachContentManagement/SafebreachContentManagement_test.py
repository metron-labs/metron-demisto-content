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


def test_get_all_running_tests_summary(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_all_running_tests_summary_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_all_running_tests_summary_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        if key == "success":
            assert command_results.outputs_prefix == "tests_data"
            assert command_results.outputs == test_output["outputs"][key]
        else:
            assert bool(test_output["outputs"][key]) is False


def test_get_all_running_simulations_summary(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_all_running_simulations_summary_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_all_running_simulations_summary_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "active_simulations"
        assert command_results.outputs == test_output["outputs"][key]
        if key == "success_with_data":
            assert test_output["outputs"][key].get("data").get("RUNNING") is not None
        elif key == "success_without_data":
            assert bool(test_output["outputs"][key].get("data").get("RUNNING")) is False
        else:
            assert bool(test_output["outputs"][key]) is False


def test_pause_resume_tests_and_simulations(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_pause_resume_tests_and_simulations_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_pause_resume_tests_and_simulations_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "simulations_tests_status"
        assert command_results.outputs == test_output["outputs"][key].get("data")
        if key != "fail":
            assert test_output["outputs"][key].get("data").get("status") == "OK"
        else:
            assert bool(test_output["outputs"][key]) is False


def test_get_schedules(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_schedules_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_schedules_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "schedules"
        assert command_results.outputs == test_output["outputs"][key].get("data")
        if key != "fail":
            assert test_output["outputs"][key].get("data") is not None
            if key in ("success_no_deleted_no_details", "success_deleted_no_details"):
                assert isinstance(test_output["outputs"][key].get("data")[0], dict) is True
                assert len(test_output["outputs"][key].get("data")[0]) == 2
            elif key in ("success_deleted_details", "success_no_deleted_details"):
                assert isinstance(test_output["outputs"][key].get("data")[0], dict) is True
                assert len(test_output["outputs"][key].get("data")[0]) > 2
        else:
            assert bool(test_output["outputs"][key]) is False


def test_delete_schedules(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_schedules_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_schedules_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        if key != "fail":
            assert test_output["outputs"][key].get("data") is not None
            main()
            call = safebreach_content_management.return_results.call_args_list
            command_results = call[0].args[0]
            assert command_results.outputs_prefix == "deleted_Schedule"
            assert command_results.outputs == test_output["outputs"][key]
        else:
            main()


def test_get_prebuilt_scenarios(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_prebuilt_scenarios_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_prebuilt_scenarios_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "prebuilt_scenarios"
        assert command_results.outputs == test_output["outputs"][key]
        if key != "fail":
            assert bool(test_output["outputs"][key]) is True
            assert all(item["createdBy"] == "SafeBreach" for item in test_output["outputs"][key])
        else:
            assert bool(test_output["outputs"][key]) is False


def test_get_custom_scenarios(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_custom_scenarios_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_custom_scenarios_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "custom_scenarios"
        assert command_results.outputs == test_output["outputs"][key]
        if key != "fail":
            assert bool(test_output["outputs"][key].get("data")) is True
            assert all(item.get("createdBy") is None for item in test_output["outputs"][key].get("data"))
            if key == "success_with_details":
                assert all(item.get("createdAt") is not None for item in test_output["outputs"][key].get("data"))
        else:
            assert bool(test_output["outputs"][key]) is False


def test_get_services_status(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_services_status_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_services_status_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "services_status"
        assert command_results.outputs == test_output["outputs"][key]
        assert bool(test_output["outputs"][key]) is True
        if key == "success":
            assert all(item.get("isUp") is True for item in test_output["outputs"][key])
        else:
            assert any(item.get("isUp") is False for item in test_output["outputs"][key])


def test_get_verification_token(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_verification_token_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_verification_token_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "verification_token"
        assert command_results.outputs == test_output["outputs"][key]
        if key != "fail":
            assert test_output["outputs"][key].get("data", {}).get("secret") is not None


def test_rerun_scenario(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_rerun_scenario_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_rerun_scenario_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "changed_data"
        assert command_results.outputs == test_output["outputs"][key]
        if key != "fail":
            assert test_output["outputs"][key]["data"]["priority"] == test_input[key]["args"]["priority"]


def test_rerun_test(mocker):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_rerun_test_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_rerun_test_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]
        assert command_results.outputs_prefix == "changed_data"
        assert command_results.outputs == test_output["outputs"][key]
        if key != "fail":
            assert isinstance(test_output["outputs"][key]["data"]["planRunId"], str)
            assert test_output["outputs"][key]["data"]["priority"] == test_input[key]["args"]["priority"]
