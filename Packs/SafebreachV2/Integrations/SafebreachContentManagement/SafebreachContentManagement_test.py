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
                test_input[key]["args"]["name"]
            assert test_output["outputs"][key].get("data")["email"] == \
                test_input[key]["args"]["email"]

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
                assert f"User with {test_input[key]['args']['user_id']} or {test_input[key]['args']['email']} not found" == str(
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
            test_input[key]["args"]["name"]
        assert test_output["outputs"][key].get("data")["email"] == \
            test_input[key]["args"]["email"]
        assert test_output["outputs"][key].get("data")["description"] == \
            test_input[key]["args"]["user_description"]


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
                assert f"User with {test_input[key]['args']['user_id']} or {test_input[key]['args']['email']} not found" == str(
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
            test_input[key]["args"]["name"]
        assert test_output["outputs"][key].get("data")["email"] == \
            test_input[key]["args"]["email"]
        assert test_output["outputs"][key].get("data")["description"] == \
            test_input[key]["args"]["user_description"]


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
                test_input[key]["args"]["name"]
            assert test_output["outputs"][key].get("data")["description"] == \
                test_input[key]["args"]["description"]
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
                test_input[key]["args"]["updated_deployment_name"]
            assert test_output["outputs"][key].get("data")["description"] == \
                test_input[key]["args"]["updated_deployment_description"]
            assert test_output["outputs"][key].get("data")["deletedAt"] is None

        else:
            assert test_output["outputs"][key].get("data").get("updated_deployment_name") is None


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
                test_input[key]["args"]["name"]
            assert test_output["outputs"][key].get("data")["description"] == \
                test_input[key]["args"]["description"]
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
                assert f"couldn't find APi key with given name: {test_input[key]['args']['key_name']}" == str(err)
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
            test_input[key]["args"]["key_name"]
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
            assert test["status"] == test_input[key]["args"]["status"]
        assert len(test_output["outputs"][key]) <= test_input[key]["args"]["entries_per_page"]


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
            assert bool(test_input[key]["args"]["plan_id"]) is True
        else:
            assert bool(test_input[key]["args"]["plan_id"]) is False
        assert command_results.outputs_prefix == "tests_data"
        assert command_results.outputs == {"tests_data": test_output["outputs"][key]}
        for test in test_output["outputs"][key]:
            assert test["status"] == test_input[key]["args"]["status"]
        assert len(test_output["outputs"][key]) <= test_input[key]["args"]["entries_per_page"]


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
            assert bool(test_input[key]["args"]["test_id"]) is True
        else:
            assert bool(test_input[key]["args"]["test_id"]) is False
            continue
        assert command_results.outputs_prefix == "deleted_test_results"
        assert command_results.readable_output == tableToMarkdown(
            name="Deleted Test", t=command_results.outputs,
            headers=["id"])
        assert command_results.outputs == [test_output["outputs"][key].get("data", {}).get("id")]


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
            assert test_input[key]["args"]["connector_id"] in test_output["outputs"][key].get("errorMessage")
            continue
        else:
            assert test_output["outputs"][key].get("error") is not None
        assert command_results.outputs_prefix == "errors_cleared"
        assert command_results.readable_output == tableToMarkdown(
            name="Integration Connector errors status", t=command_results.outputs,
            headers=["error", "result"])


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
