from collections.abc import Callable, Generator
import pytest
from pytest_mock import MockerFixture
from CommonServerPython import *
from SafebreachContentManagement import Client, NotFoundError
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


def test_create_deployment(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_create_deployment_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_create_deployment_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "created_deployment_data"
        assert command_results.readable_output == tableToMarkdown(
            name="Created Deployment", t=command_results.outputs, headers=['id', "accountId", 'name',
                                                                           'createdAt', "description", "nodes"])

        if key == "successful_creation":
            assert command_results.outputs == test_output["outputs"][key].get("data")
            assert test_output["outputs"][key].get("data") is not None
            assert test_output["outputs"][key].get("data")["name"] == \
                test_input[key]["args"]["Name"]
            assert test_output["outputs"][key].get("data")["description"] == \
                test_input[key]["args"]["Description"]
            assert test_output["outputs"][key].get("data")["deletedAt"] is None

        else:
            assert isinstance(test_output["outputs"][key]["error"], dict)


def test_update_deployment(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_update_deployment_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_update_deployment_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, 'get_deployment_id_by_name',
                            return_value=[test_output["outputs"][key]["data"]])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "updated_deployment_data"
        assert command_results.readable_output == tableToMarkdown(
            name="Updated Deployment", t=command_results.outputs, headers=['id', "accountId", 'name', 'createdAt',
                                                                           "description", "nodes", "updatedAt"])

        if key != "failed_update":
            assert command_results.outputs == test_output["outputs"][key].get("data")
            assert test_output["outputs"][key].get("data") is not None
            assert test_output["outputs"][key].get("data")["name"] == \
                test_input[key]["args"]["Updated Deployment Name"]
            assert test_output["outputs"][key].get("data")["description"] == \
                test_input[key]["args"]["Updated deployment description."]
            assert test_output["outputs"][key].get("data")["deletedAt"] is None

        else:
            assert test_output["outputs"][key].get("data").get("Updated Deployment Name") is None


def test_delete_deployment(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_deployment_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_deployment_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, 'get_deployment_id_by_name',
                            return_value=[test_output["outputs"][key]["data"]])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "deleted_deployment_data"
        assert command_results.readable_output == tableToMarkdown(
            name="Deleted Deployment", t=command_results.outputs, headers=['id', "accountId", 'name', 'createdAt',
                                                                           "description", "nodes", "updatedAt"])

        if key != "failed_delete":
            assert key == key
            assert command_results.outputs == test_output["outputs"][key].get("data")
            assert test_output["outputs"][key].get("data") is not None
            assert test_output["outputs"][key].get("data")["deletedAt"] is not None

        else:
            assert test_output["outputs"][key].get("data").get("deletedAt") is None


def test_create_api_key(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_create_api_key_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_create_api_key_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "generated_api_key"
        assert command_results.readable_output == tableToMarkdown(
            name="Generated API key Data", t=command_results.outputs,
            headers=["name", "description", "createdBy", "createdAt", "key", "roles", "role"])

        if key == "successful_creation":
            assert command_results.outputs == test_output["outputs"][key].get("data")
            assert test_output["outputs"][key].get("data") is not None
            assert test_output["outputs"][key].get("data")["name"] == \
                test_input[key]["args"]["Name"]
            assert test_output["outputs"][key].get("data")["description"] == \
                test_input[key]["args"]["Description"]
            assert test_output["outputs"][key].get("data")["deletedAt"] is None

        else:
            assert isinstance(test_output["outputs"][key]["error"], dict)
            assert test_output["outputs"][key]["error"].get("errors") is not None


def test_delete_api_key(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_api_key_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_api_key_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, 'get_all_active_api_keys_with_details',
                            return_value=test_input[key]["all_active_api_keys_data"])
        if key == "successful_delete_just_name":
            main()
        else:
            try:
                safebreach_content_management.delete_api_key(mock_sb_client)
            except NotFoundError as err:
                assert f"couldn't find APi key with given name: {test_input[key]['args']['Key Name']}" == str(err)
            continue
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "deleted_api_key"
        assert command_results.readable_output == tableToMarkdown(
            name="Deleted API key Data", t=command_results.outputs,
            headers=["name", "description", "createdBy", "createdAt", "deletedAt"])

        assert command_results.outputs == test_output["outputs"][key].get("data")
        assert test_output["outputs"][key].get("data") is not None
        assert test_output["outputs"][key].get("data")["name"] == \
            test_input[key]["args"]["Key Name"]
        assert test_output["outputs"][key].get("data")["deletedAt"] is not None
