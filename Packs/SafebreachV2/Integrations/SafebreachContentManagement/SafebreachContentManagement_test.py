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


def test_get_all_users(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_all_users_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_all_users_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "user_data"
        assert command_results.readable_output == tableToMarkdown(
            name="user data", t=command_results.outputs, headers=['id', 'name', 'email'])
        assert command_results.outputs == test_output["outputs"][key].get(
            "data")
        assert len(command_results.outputs) == 2
        if key == "details_and_deleted":
            assert test_output["outputs"][key].get(
                "data")[0]["deletedAt"] is None
            assert test_output["outputs"][key].get(
                "data")[1]["deletedAt"] is not None
        elif key == "just_details":
            assert test_output["outputs"][key].get(
                "data")[0]["deletedAt"] is None
            assert test_output["outputs"][key].get(
                "data")[1]["deletedAt"] is None
        else:
            with pytest.raises(KeyError) as key_err:
                test_output["outputs"][key].get("data")[0]["deletedAt"]
            assert key_err.type is KeyError


def test_get_user_id_by_name_or_email(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_get_named_user_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_get_named_user_outputs.json")

    for key in test_input:

        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "filtered_users"
        assert command_results.readable_output == tableToMarkdown(
            name="user data", t=command_results.outputs, headers=['id', 'name', 'email'])
        assert command_results.outputs == test_output["outputs"][key].get("data")
        assert len(command_results.outputs) in [0, 1]
        if key in ["not_deleted_with_name", "not_deleted_without_name"]:
            assert test_output["outputs"][key].get("data")[0]["deletedAt"] is None
        elif key in ["deleted_with_name", "deleted_without_name"]:
            assert test_output["outputs"][key].get("data")[0]["deletedAt"] is not None
            assert type(test_output["outputs"][key].get("data")[0]["deletedAt"]) == str
        else:
            assert isinstance(test_output["outputs"][key].get("data"), types.FunctionType)


def test_create_user(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_create_user_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_create_user_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "created_user_data"
        assert command_results.readable_output == tableToMarkdown(
            name="Created User Data", t=command_results.outputs, headers=['id', 'name', 'email', "mustChangePassword", "roles",
                                                                          "description", "role", "isActive", "deployments",
                                                                          "createdAt"])
        assert command_results.outputs == test_output["outputs"][key].get("data")

        if key == "successful_creation":
            assert test_output["outputs"][key].get("data") is not None
            assert test_output["outputs"][key].get("data")["name"] == \
                test_input[key]["args"]["Name"]
            assert test_output["outputs"][key].get("data")["email"] == \
                test_input[key]["args"]["Email"]

        elif key == "weak_password":
            assert callable(test_output["outputs"][key]["data"]) is False

        else:
            assert callable(test_output["outputs"][key]["data"]) is False


def test_update_user_with_details(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_update_user_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_update_user_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])

        mocker.patch.object(safebreach_client, 'get_users_list',
                            return_value=[test_output["outputs"][key]["data"]])
        if key in ["failed_update", "weak_password"]:
            try:
                safebreach_content_management.update_user_with_details(mock_sb_client)
            except NotFoundError as error:
                assert f"User with {test_input[key]['args']['User ID']} or {test_input[key]['args']['Email']} not found" == str(
                    error)
            continue
        else:
            main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "updated_user_data"
        assert command_results.readable_output == tableToMarkdown(
            name="Updated User Data", t=command_results.outputs, headers=['id', 'name', 'email', "deletedAt", "roles",
                                                                          "description", "role", "deployments", "createdAt",
                                                                          "updatedAt"])
        assert command_results.outputs == test_output["outputs"][key].get("data")

        assert test_output["outputs"][key].get("data") is not None
        assert test_output["outputs"][key].get("data")["name"] == \
            test_input[key]["args"]["Name"]
        assert test_output["outputs"][key].get("data")["email"] == \
            test_input[key]["args"]["Email"]
        assert test_output["outputs"][key].get("data")["description"] == \
            test_input[key]["args"]["User Description"]


def test_delete_user_with_details(mocker: Callable[..., Generator[MockerFixture, None, None]]):
    test_input = util_load_json(
        path="test_data/inputs/safebreach_delete_user_inputs.json")
    test_output = util_load_json(
        path="test_data/outputs/safebreach_delete_user_outputs.json")

    for key in test_input:
        mocker = modify_mocker_with_common_data(mocker=mocker,
                                                test_input_data=test_input[key], test_output_data=test_output["outputs"][key])
        mocker.patch.object(safebreach_client, 'get_users_list',
                            return_value=[test_output["outputs"][key]["data"]])
        if key == "failed_delete":
            try:
                safebreach_content_management.delete_user_with_details(mock_sb_client)
            except NotFoundError as error:
                assert f"User with {test_input[key]['args']['User ID']} or {test_input[key]['args']['Email']} not found" == str(
                    error)
            continue
        else:
            main()
        call = safebreach_content_management.return_results.call_args_list
        command_results = call[0].args[0]

        assert command_results.outputs_prefix == "deleted_user_data"
        assert command_results.readable_output == tableToMarkdown(
            name="Deleted User Data", t=command_results.outputs, headers=['id', 'name', 'email', "deletedAt", "roles",
                                                                          "description", "role", "deployments", "createdAt"])
        assert command_results.outputs == test_output["outputs"][key].get("data")

        assert test_output["outputs"][key].get("data") is not None
        assert test_output["outputs"][key].get("data")["name"] == \
            test_input[key]["args"]["Name"]
        assert test_output["outputs"][key].get("data")["email"] == \
            test_input[key]["args"]["Email"]
        assert test_output["outputs"][key].get("data")["description"] == \
            test_input[key]["args"]["User Description"]


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


def test_get_tests_summary(mocker: Callable[..., Generator[MockerFixture, None, None]]):
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
