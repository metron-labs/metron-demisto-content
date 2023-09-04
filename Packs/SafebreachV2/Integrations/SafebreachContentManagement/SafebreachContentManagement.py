import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
"""
New Integration starts from here

"""
import random
from enum import Enum
from ast import literal_eval
DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR


class InputTypes(Enum):
    TEXT_AREA = "textArea"


metadata_collector = YMLMetadataCollector(
    integration_name="Safebreach Content Management",
    description="This Integration aims to provide easy access to safebreach from XSOAR.\
        Following are the things that user can get access through XSOAR command integration: \
        1. User get, create, update and delete \
        2. Deployment create, update and delete \
        3. Tests get and delete \
        4. Nodes get, update, delete ",
    display="Safebreach Content Management",
    category="Data Enrichment & Threat Intelligence",
    docker_image="demisto/python3:3.10.4.29342",
    is_fetch=False,
    long_running=False,
    long_running_port=False,
    is_runonce=False,
    integration_subtype="python3",
    integration_type="python",
    fromversion="6.2.0",
    conf=[ConfKey(name="base_url",
                  display="Server URL",
                  required=True,
                  additional_info='This is base URL for your instance.',
                  key_type=ParameterTypes.STRING),
          ConfKey(name="api_key",
                  display="API Key",
                  required=True,
                  additional_info='This is API key for your instance, this can be created in safebreach user \
                      administration>APIkeys and then it must be saved as there is no way to view this again',
                  key_type=ParameterTypes.ENCRYPTED),
          ConfKey(name="account_id",
                  display="Account ID",
                  required=True,
                  additional_info="This is account ID of account with which we want to get data from safebreach",
                  key_type=ParameterTypes.NUMBER),
          ConfKey(name="verify",
                  display="Verify SSL Certificate",
                  required=True,
                  default_value=False,
                  additional_info="This Field is useful for checking if the certificate of SSL for HTTPS is valid or not",
                  key_type=ParameterTypes.BOOLEAN)
          ])


class Client(BaseClient):
    """Client class to interact with the service API

    This Client implements API calls, and does not contain any XSOAR logic.
    Should only do requests and return data.
    It inherits from BaseClient defined in CommonServer Python.
    Most calls use _http_request() that handles proxy, SSL verification, etc.
    For this  implementation, no special attributes defined
    """

    def __init__(self, api_key: str, account_id: int, base_url: str, verify: bool):
        super().__init__(base_url=base_url, verify=verify)

        self.api_key = api_key
        self.account_id = account_id

    def get_response(self, url: str = "", method: str = "GET", request_params: dict = {}, body: dict = None):

        base_url = demisto.params().get("base_url", "")
        base_url = base_url if base_url[-1] != "/" else base_url[0:-1]
        url = url if url[0] != "/" else url[1:]
        request_url = f"{base_url}/api/{url}"
        verify = demisto.params().get("verify", True)
        api_key = demisto.params().get("api_key")
        headers = {
            'Accept': 'application/json',
            'x-apitoken': api_key
        }

        try:
            response = requests.request(method=method, url=request_url, json=body, headers=headers,
                                        params=request_params, verify=verify)
            print(f"response, {response.__dict__}, request, {response.__dict__['request'].__dict__}")  # noqa: T201
            # if "bulk" in request_url:
            # raise Exception(f"{request_params}")
            # raise Exception(f"response, {response.__dict__}, request, {response.__dict__['request'].__dict__}")
            if response.status_code in [201, 200, 409]:
                return response
            self.handle_error(response, response.status_code, response.reason)
        except requests.exceptions.SSLError as e:
            demisto.error(f"response, {response.__dict__}, request, {response.__dict__['request'].__dict__}")
            raise Exception(json.dumps(e.__dict__))

    def handle_error(self, response, status_code, reason):
        error_dict = {
            401: f"{reason}, API-Key might be invalid, Please check and try again",
            404: f"{reason}, The given URL is not found, please check and try again",
            500: f"{reason}, There was an error on safebreach side",
            400: f"{reason} ,{response.text}"
        }
        raise Exception(error_dict.get(status_code) or reason)

    def get_all_users_for_test(self):

        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/users"
        response = self.get_response(url=url)
        if response:
            return "ok", True
        return "", False

    def get_users_list(self):
        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/users"
        params = {
            "details": "true",
            "deleted": "true"
        }
        response = self.get_response(url=url, request_params=params)
        user_data = response.json()['data']
        return user_data

    def delete_user(self, user_id: int):

        account_id = demisto.params().get("account_id", 0)
        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/users/{user_id}"

        deleted_user = self.get_response(url=url, method=method)
        if deleted_user.status_code == 400:
            return json.dumps(deleted_user.json()), False

        deleted_user = deleted_user.json()

        human_readable = tableToMarkdown(name="Deleted User Data", t=deleted_user.get("data", {}),
                                         headers=['id', 'name', 'email', "deletedAt", "roles", "description", "role",
                                                  "deployments", "createdAt"])
        outputs = deleted_user.get("data", {})

        result = CommandResults(
            outputs_prefix="user_data",
            outputs=outputs,
            readable_output=human_readable
        )

        return result, True

    def update_user_with_details(self, user_id: str, user_details: dict):
        for key in list(user_details.keys()):
            if not user_details[key]:
                user_details.pop(key)

        account_id = demisto.params().get("account_id", 0)
        method = "PUT"
        url = f"/config/v1/accounts/{account_id}/users/{int(user_id)}"

        updated_user = self.get_response(url=url, method=method, body=user_details)
        if updated_user.status_code == 400:
            return json.dumps(updated_user.json()), False

        updated_user = updated_user.json()

        human_readable = tableToMarkdown(name="Updated User Data", t=updated_user.get("data", {}),
                                         headers=['id', 'name', 'email', "deletedAt", "roles", "description", "role",
                                                  "deployments", "createdAt", "updatedAt"])
        outputs = updated_user.get("data", {})
        # [{
        #     'data':updated_user.get("data",{})
        # }]

        result = CommandResults(
            outputs_prefix="user_data",
            outputs=outputs,
            readable_output=human_readable
        )

        return result, True

    def list_deployments(self):
        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/deployments"

        response = self.get_response(url=url)
        deployments = response.json()['data']
        return deployments

    def get_deployment_id_by_name(self, deployment_name: str):
        available_deployments = self.list_deployments()
        needed_deployments = list(filter(lambda deployment: deployment["name"] == deployment_name, available_deployments))
        return needed_deployments[0] if needed_deployments else []

    def create_deployment(self, name: str, nodes: list[str]):
        try:
            account_id = demisto.params().get("account_id", 0)
            deployment_payload = {
                "nodes": nodes,
                "name": name,
                "id": random.getrandbits(20)
            }

            method = "POST"
            url = f"/config/v1/accounts/{account_id}/deployments"
            created_deployment = self.get_response(url=url, method=method, body=deployment_payload)

            if created_deployment.status_code == 409:
                return json.dumps(created_deployment.json()), False
            created_deployment = created_deployment.json()

            human_readable = tableToMarkdown(name="Created Deployment", t=created_deployment.get("data", {}),
                                             headers=['id', "accountId", 'name', 'createdAt', "description", "nodes"])
            outputs = created_deployment.get("data", {})

            result = CommandResults(
                outputs_prefix="deployment_data",
                outputs=outputs,
                readable_output=human_readable
            )

            return result, True

        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def update_deployment(self, deployment_id, name: str, nodes: list[str]):
        try:
            account_id = demisto.params().get("account_id", 0)
            deployment_payload = {
                "nodes": nodes,
                "name": name,
            }
            method = "PUT"
            url = f"/config/v1/accounts/{account_id}/deployments/{deployment_id}"
            updated_deployment = self.get_response(url=url, method=method, body=deployment_payload)

            if updated_deployment.status_code == 409:
                return json.dumps(updated_deployment.json()), False
            updated_deployment = updated_deployment.json()

            human_readable = tableToMarkdown(name="Updated Deployment", t=updated_deployment.get("data", {}),
                                             headers=['id', "accountId", 'name', 'createdAt',
                                                      "description", "nodes", "updatedAt"])
            outputs = updated_deployment.get("data", {})

            result = CommandResults(
                outputs_prefix="deployment_data",
                outputs=outputs,
                readable_output=human_readable
            )

            return result, True

        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def delete_deployment(self, deployment_id: str):
        try:
            account_id = demisto.params().get("account_id", 0)

            method = "DELETE"
            url = f"/config/v1/accounts/{account_id}/deployments/{deployment_id}"
            deleted_deployment = self.get_response(url=url, method=method)

            if deleted_deployment.status_code == 409:
                return json.dumps(deleted_deployment.json()), False
            deleted_deployment = deleted_deployment.json()

            human_readable = tableToMarkdown(name="deleted Deployment", t=deleted_deployment.get("data", {}),
                                             headers=['id', "accountId", 'name', 'createdAt',
                                                      "description", "nodes", "deletedAt"])
            outputs = deleted_deployment.get("data", {})

            result = CommandResults(
                outputs_prefix="deployment_data",
                outputs=outputs,
                readable_output=human_readable
            )

            return result, True

        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def get_tests_with_args(self, include_archived, size, status, plan_id, simulation_id, sort_by):
        account_id = demisto.params().get("account_id", 0)
        parameters = {}

        # preparing request data
        method = "GET"
        url = f"/data/v1/accounts/{account_id}/testsummaries"
        for param in [("includeArchived", include_archived), ("size", size), ("status", status), ("planId", plan_id),
                      ("simulationId", simulation_id), ("sortBy", sort_by)]:
            parameters.update({} if not param[1] else {param[0]: param[1]})

        test_summaries = self.get_response(url=url, method=method, request_params=parameters)
        if test_summaries.status_code == 409:
            return json.dumps(test_summaries.json()), False
        test_summaries = test_summaries.json()
        return test_summaries, True

    def flatten_test_summaries(self, test_summaries):
        for test_summary in test_summaries:
            for key in list(test_summary.keys()):
                if key == "finalStatus":
                    data_dict = {
                        "stopped": test_summary[key].get('stopped', 0),
                        "missed": test_summary[key].get('missed', 0),
                        "logged": test_summary[key].get('logged', 0),
                        "detected": test_summary[key].get('detected', 0),
                        "prevented": test_summary[key].get('prevented', 0),
                        "inconsistent": test_summary[key].get('inconsistent', 0),
                        "drifted": test_summary[key].get('drifted', 0),
                        "not_drifted": test_summary[key].get('not_drifted', 0),
                        "baseline": test_summary[key].get('baseline', 0)
                    }
                    test_summary.update(data_dict)
                if key in ["endTime", "startTime"]:
                    test_summary[key] = datetime.utcfromtimestamp(test_summary[key] / 1000).strftime(DATE_FORMAT)

    def get_tests_summary(self, include_archived, size, status, plan_id, simulation_id, sort_by):
        try:
            test_summaries, status = self.get_tests_with_args(include_archived, size, status, plan_id, simulation_id, sort_by)
            if status:
                self.flatten_test_summaries(test_summaries)
                human_readable = tableToMarkdown(
                    name="deleted Deployment",
                    t=test_summaries,
                    headers=['planId', "planName", 'securityActionPerControl', 'planRunId', "runId", "status",
                             "plannedSimulationsAmount", "simulatorExecutions", "ranBy", "simulatorCount", "endTime", "startTime",
                             "finalStatus", "stopped", "missed", "logged", "detected", "prevented",
                             "inconsistent", "drifted", "not_drifted", "baseline"])
                outputs = [{
                    'tests': test_summaries
                }]

                result = CommandResults(
                    outputs_prefix="Tests Data",
                    outputs=outputs,
                    readable_output=human_readable
                )

                return result, True
            return test_summaries, False
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def get_test_summary(self, include_archived, size, status, plan_id, simulation_id, sort_by):
        try:
            test_summaries, status = self.get_tests_with_args(include_archived, size, status, plan_id, simulation_id, sort_by)
            if status:
                self.flatten_test_summaries(test_summaries)
                human_readable = tableToMarkdown(
                    name="Test Summary",
                    t=test_summaries,
                    headers=['planId', "planName", 'securityActionPerControl', 'planRunId', "runId", "status",
                             "plannedSimulationsAmount", "simulatorExecutions", "ranBy", "simulatorCount", "endTime", "startTime",
                             "finalStatus", "stopped", "missed", "logged", "detected", "prevented",
                             "inconsistent", "drifted", "not_drifted", "baseline"])
                outputs = test_summaries[0] if test_summaries else {}
                result = CommandResults(
                    outputs_prefix="test_data",
                    outputs=outputs,
                    readable_output=human_readable
                )

                return result, True
            return test_summaries, False
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def delete_test_result_of_test(self, test_id: str, soft_delete: str):
        account_id = demisto.params().get("account_id", 0)

        method = "DELETE"
        url = f"/data/v1/accounts/{account_id}/tests/{test_id}"
        request_parameters = {
            "softDelete": soft_delete
        }
        test_summaries = self.get_response(url=url, method=method, request_params=request_parameters)
        if test_summaries.status_code == 409:
            return json.dumps(test_summaries.json()), False
        test_summaries = test_summaries.json()
        return test_summaries.get("data").get("id"), True

    def flatten_error_logs_for_table_view(self, error_logs):
        flattened_logs_list = []
        for connector in error_logs:
            logs = error_logs[connector]["logs"] if error_logs[connector].get("status") == "error" else []
            if logs:
                for log in logs:
                    log["connector"] = connector
                    flattened_logs_list.append(log)
        return flattened_logs_list

    def get_all_error_logs(self):
        account_id = demisto.params().get("account_id", 0)
        formatted_error_logs = []
        method = "GET"
        url = f"/siem/v1/accounts/{account_id}/config/providers/status"

        error_logs = self.get_response(url=url, method=method)
        if error_logs.status_code == 409:
            return json.dumps(error_logs.json()), False
        error_logs = error_logs.json()
        if error_logs.get("result"):
            formatted_error_logs = self.flatten_error_logs_for_table_view(error_logs.get("result"))
            human_readable = tableToMarkdown(
                name="Integration Connector errors",
                t=formatted_error_logs,
                headers=["action", "success", "error", "timestamp", "connector"])
            outputs = [{
                'Connector Errors': error_logs.get("result")
            }]
            result = CommandResults(
                outputs_prefix="Integration Error Data",
                outputs=outputs,
                readable_output=human_readable
            )
            return result, True
        return formatted_error_logs, True

    def generate_api_key(self, name, description):
        account_id = demisto.params().get("account_id", 0)
        method = "POST"
        url = f"/config/v1/accounts/{account_id}/apikeys"
        data = {
            "name": name,
            "description": description,
        }
        generated_api_key = self.get_response(method=method, url=url, body=data)
        if generated_api_key.status_code == 409:
            return json.dumps(generated_api_key.json()), False
        generated_api_key = generated_api_key.json()
        return generated_api_key, True

    def generate_api_key_and_table(self, name, description):
        generated_api_key, status = self.generate_api_key(name, description)
        if status:
            human_readable = tableToMarkdown(
                name="Generated API key Data",
                t=generated_api_key.get("data"),
                headers=["name", "description", "accountId", "createdBy", "createdAt", "key", "roles", "role"])
            outputs = generated_api_key.get("data")
            result = CommandResults(
                outputs_prefix="generated_api_key_data",
                outputs=outputs,
                readable_output=human_readable
            )
            return result, True
        return generated_api_key, False

    def get_all_active_api_keys_with_details(self):
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"config/v1/accounts/{account_id}/apikeys"
        request_params = {
            "details": "true"
        }
        keys_data = self.get_response(url=url, method=method, request_params=request_params)
        if keys_data.status_code == 409:
            return json.dumps(keys_data.json()), False
        keys_data = keys_data.json()
        return keys_data, True

    def filter_api_key_with_key_name(self, key_name):
        active_keys, status = self.get_all_active_api_keys_with_details()
        if status:
            required_key_object = list(filter(lambda key_obj: key_obj["name"] == key_name, active_keys.get("data")))
        if required_key_object:
            return required_key_object[0]["id"], True
        return "couldn't find APi key with given name", False

    def delete_api_key(self, key_name):
        key_id, status = self.filter_api_key_with_key_name(key_name=key_name)
        if status:
            account_id = demisto.params().get("account_id", 0)
            method = "DELETE"
            url = f"/config/v1/accounts/{account_id}/apikeys/{key_id}"
            deleted_api_key = self.get_response(method=method, url=url)
            if deleted_api_key.status_code == 409:
                return json.dumps(deleted_api_key.json()), False
            deleted_api_key = deleted_api_key.json()
            return deleted_api_key, True
        return key_id, False if key_id else deleted_api_key, False

    def delete_api_key_with_given_name(self, key_name):
        try:
            result, status = self.delete_api_key(key_name)
            if status:
                human_readable = tableToMarkdown(
                    name="Deleted API key Data",
                    t=result.get("data"),
                    headers=["name", "description", "accountId", "createdBy", "createdAt", "roles", "role"])
                outputs = result.get("data")
                result = CommandResults(
                    outputs_prefix="Deleted API key",
                    outputs=outputs,
                    readable_output=human_readable
                )
                return result, True
            return result, status
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def get_simulator_quota(self):
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}"
        simulator_details = self.get_response(method=method, url=url)
        if simulator_details.status_code == 409:
            return json.dumps(simulator_details.json()), False
        simulator_details = simulator_details.json()
        return simulator_details, True

    def get_simulator_quota_with_table(self):
        try:
            result, status = self.get_simulator_quota()
            if status:
                human_readable = tableToMarkdown(
                    name="Account Details",
                    t=result.get("data"),
                    headers=["id", "name", "contactName", "contactEmail", "userQuota", "nodesQuota", "registrationDate",
                             "activationDate", "expirationDate"])
                outputs = [{
                    'Account Details': result.get("data")
                }, {
                    "simulator_details": result.get("data").get("nodesQuota")
                }]
                result = CommandResults(
                    outputs_prefix="Account Details",
                    outputs=outputs,
                    readable_output=human_readable
                )
                return result, True
            return result, status
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def get_simulators_details(self, request_params):
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}/nodes/bulk"

        simulators_details = self.get_response(method=method, url=url, request_params=request_params)
        if simulators_details.status_code == 409:
            return json.dumps(simulators_details.json()), False
        simulators_details = simulators_details.json()
        if simulators_details.get("data", {}).get("count"):
            return simulators_details, True
        return f"No Matching simulators found with details name: {demisto.args().get('simulator_name')}", False

    def create_get_simulator_params_dict(self):
        possible_inputs = [
            "details", "deleted", "secret", "shouldIncludeProxies", "hostname", "connectionType", "externalIp", "internalIp",
            "os", "status", "sortDirection", "startRow", "pageSize", "isEnabled", "isConnected", "isCritical",
            "isExfiltrationEarget", "isInfiltrationTarget", "isMailTarget", "isMailAttacker", "isPreExecutor",
            "isAwsAttacker", "isAzureAttacker", "impersonatedUsers", "assets", "advancedActions", "deployments",
            "additionalDetails"]
        request_params = {}
        for parameter in possible_inputs:
            if demisto.args().get(parameter) and demisto.args().get(parameter) != 'false':
                request_params[parameter] = demisto.args().get(parameter)

        return request_params, True

    def flatten_node_details(self, nodes):
        keys = None
        flattened_nodes = []
        for node in nodes:
            node_details = {
                "is_enabled": node.get("isEnabled"),
                "simulator_id": node.get("id"),
                "simulator_name": node.get("name"),
                "account_id": node.get("accountId"),
                "is_critical": node.get("isCritical"),
                "is_exfiltration": node.get("isExfiltration"),
                "is_infiltration": node.get("isInfiltration"),
                "is_mail_target": node.get("isMailTarget"),
                "is_mail_attacker": node.get("isMailAttacker"),
                "is_pre_executor": node.get("isPreExecutor"),
                "is_aws_attacker": node.get("isAWSAttacker"),
                "is_azure_attacker": node.get("isAzureAttacker"),
                "is_web_application_attacker": node.get("isWebApplicationAttacker"),
                "external_ip": node.get("externalIp"),
                "internal_ip": node.get("internalIp"),
                "preferred_interface": node.get("preferredInterface"),
                "preferred_ip": node.get("preferredIp"),
                "hostname": node.get("hostname"),
                "connection_type": node.get("connectionType"),
                "simulator_status": node.get("status"),
                "connection_status": node.get("isConnected"),
                "simulator_framework_version": node.get("frameworkVersion"),
                "operating_system_type": node.get("nodeInfo", {}).get("MACHINE_INFO", {}).get("TYPE", ""),
                "operating_system": node.get("nodeInfo", {}).get("MACHINE_INFO", {}).get("PLATFORM", {}).get("PRETTY_NAME", ""),
                "execution_hostname": node.get("nodeInfo", {}).get("CURRENT_CONFIGURATION", {}).get("EXECUTION_HOSTNAME", ""),
                "deployments": node.get("group"),
                "created_at": node.get("createdAt"),
                "updated_at": node.get("updatedAt"),
                "deleted_at": node.get("deletedAt"),
                "assets": node.get("assets"),
                "simulation_users": node.get("simulationUsers"),
                "advanced_actions": node.get("advancedActions"),
                "proxies": node.get("proxies")
            }
            if not keys:
                keys = list(node_details.keys())
            # for keys in node_details:
            #     if not node_details[key]:
            #         node_details.pop(key)
            flattened_nodes.append(node_details)
        return flattened_nodes, keys

    def get_simulators_and_display_in_table(self, just_name=False):
        try:
            request_params, status = self.get_simulator_with_name_request_params() if just_name \
                else self.create_get_simulator_params_dict()
            result, status = self.get_simulators_details(request_params=request_params)
            if status:
                flattened_nodes, keys = self.flatten_node_details(result.get("data", {}).get("rows", {}))
                human_readable = tableToMarkdown(
                    name="Simulators Details",
                    t=flattened_nodes,
                    headers=keys)
                outputs = result.get("data", {}).get("rows")[0]
                print("outputs", outputs)  # noqa: T201
                result = CommandResults(
                    outputs_prefix="simulator_details",
                    outputs=outputs,
                    readable_output=human_readable
                )
                return result, True
            return result, status
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def get_simulator_with_name_request_params(self):
        name = demisto.args().get("simulator_name")
        request_params = {
            "name": name,
            "deleted": "true",
            "details": "true"
        }
        return request_params, True

    def get_simulator_with_a_name_return_id(self):
        request_params, status = self.get_simulator_with_name_request_params()
        result, status = self.get_simulators_details(request_params=request_params)
        if status:
            try:
                simulator_id = result.get("data", {}).get("rows", {})[0].get("id")
                return simulator_id, True
            except IndexError:
                return "Simulator with given details could not be found", False
        return "Simulator with given details could not be found", False

    def delete_node_with_given_id(self, node_id, force=False):
        request_params = {
            "force": "true" if force else "false"
        }
        method = "DELETE"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{node_id}"

        deleted_node = self.get_response(url=request_url, method=method, request_params=request_params)
        if deleted_node.status_code == 409:
            return json.dumps(deleted_node.json()), False
        deleted_node = deleted_node.json()
        return deleted_node, True

    def delete_simulator_with_given_name(self):
        try:
            simulator_id, status = self.get_simulator_with_a_name_return_id()
            if status:
                force_delete = demisto.args().get("force_delete")
                result, status = self.delete_node_with_given_id(node_id=simulator_id, force=force_delete)
                if status:
                    flattened_nodes, keys = self.flatten_node_details([result.get("data", {})])
                    human_readable = tableToMarkdown(
                        name="Deleted Simulators Details",
                        t=flattened_nodes,
                        headers=keys)
                    outputs = [{
                        'Deleted simulators Details': result.get("data", {}),
                    }]
                    result = CommandResults(
                        outputs_prefix="Deleted Simulators Details",
                        outputs=outputs,
                        readable_output=human_readable
                    )
                    return result, True
                return result, status
            return simulator_id, status
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def make_update_node_payload(self):
        # this is created under assumption that only these fields will be  chosen to be updated by user
        data_dict = {
            "isEnabled": demisto.args().get("isEnabled", "").lower(),
            "isProxySupported": demisto.args().get("isProxySupported", "").lower(),
            "isCritical": demisto.args().get("isCritical", "").lower(),
            "isExfiltration": demisto.args().get("isExfiltration", "").lower(),
            "isInfiltration": demisto.args().get("isInfiltration", "").lower(),
            "isMailTarget": demisto.args().get("isMailTarget", "").lower(),
            "isMailAttacker": demisto.args().get("isMailAttacker", "").lower(),
            "isPreExecutor": demisto.args().get("isPreExecutor", "").lower(),
            "isAWSAttacker": demisto.args().get("isAWSAttacker", "").lower(),
            "isAzureAttacker": demisto.args().get("isAzureAttacker", "").lower(),
            "isWebApplicationAttacker": demisto.args().get("isWebApplicationAttacker", "").lower(),
            "connectionUrl": demisto.args().get("connectionUrl", "").lower(),
            "cloudProxyUrl": demisto.args().get("cloudProxyUrl", ""),
            "useSystemUser": demisto.args().get("useSystemUser", ""),
            "name": demisto.args().get("name", ""),
            "tunnel": demisto.args().get("tunnel", ""),
            "preferredInterface": demisto.args().get("preferredInterface", ""),
            "preferredIp": demisto.args().get("preferredIp", ""),
        }

        for (key, value) in tuple(data_dict.items()):
            if not value:
                data_dict.pop(key)
        return data_dict

    def update_node(self, node_id, node_data):
        method = "PUT"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{node_id}"

        updated_node = self.get_response(url=request_url, method=method, body=node_data)
        if updated_node.status_code == 409:
            return json.dumps(updated_node.json()), False
        updated_node = updated_node.json()
        return updated_node, True

    def update_simulator_with_given_name(self):
        try:
            simulator_id, status = self.get_simulator_with_a_name_return_id()
            if status:
                payload = self.make_update_node_payload()
                result, status = self.update_node(node_id=simulator_id, node_data=payload)
                if status:
                    flattened_nodes, keys = self.flatten_node_details([result.get("data", {})])
                    human_readable = tableToMarkdown(
                        name="Updated Simulators Details",
                        t=flattened_nodes,
                        headers=keys)
                    outputs = result.get("data", {}), result.get("data", {})
                    result = CommandResults(
                        outputs_prefix="updated_simulator_details",
                        outputs=outputs,
                        readable_output=human_readable
                    )
                    return result, True
                return result, status
            return simulator_id, status
        except Exception as e:
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def rotate_verification_token(self):
        method = "POST"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/secret/rotate"

        new_token = self.get_response(url=request_url, method=method, body={})
        if new_token.status_code == 409:
            return json.dumps(new_token.json()), False
        new_token = new_token.json()
        return new_token, True

    def return_rotated_verification_token(self):
        try:
            result, status = self.rotate_verification_token()
            if status:
                human_readable = tableToMarkdown(
                    name=" new Token Details",
                    t=result.get("data"),
                    headers=["secret"])
                outputs = [{
                    'New Token Details': result.get("data", {}).get("secret", ""),
                }]
                result = CommandResults(
                    outputs_prefix="New Token Details",
                    outputs=outputs,
                    readable_output=human_readable
                )
                return result, True
            return "Verification Token Could not be created", False
        except Exception as e:  # noqa: E722
            demisto.error(traceback.format_exc())  # log exception for debugging purposes
            return f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}", False

    def create_user_data(self):
        account_id = literal_eval(demisto.params().get("account_id", 0))
        name = demisto.args().get("Name")
        email = demisto.args().get("Email")
        is_active = literal_eval(demisto.args().get("Is Active", False))
        send_email_post_creation = literal_eval(demisto.args().get("Email Post Creation", False))
        password = demisto.args().get("Password")
        admin_name = demisto.args().get("Admin Name", "")
        change_password = literal_eval(demisto.args().get("Change Password on create", False))
        role = demisto.args().get("User role", "")
        deployment_list = demisto.args().get("Deployments", [])
        deployment_list = list(deployment_list) if deployment_list else []

        user_payload = {
            "accountId": account_id,
            "name": name,
            "password": password,
            "email": email,
            "mustChangePassword": change_password,
            "sendMail": send_email_post_creation,
            "adminName": admin_name,
            "role": role,
            "isActive": is_active,
            "deployments": deployment_list,
        }

        # for key in list(user_payload.keys()):
        #     if not user_payload[key]:
        #         user_payload.pop(key)

        method = "POST"
        url = f"/config/v1/accounts/{account_id}/users"
        created_user = self.get_response(url=url, method=method, body=user_payload)
        return created_user


@metadata_collector.command(
    command_name="safebreach-get-all-users",
    inputs_list=None,
    outputs_prefix="user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User retrieved.",
                       prefix="user_data", output_type=int),
        OutputArgument(name="name", description="The name of User retrieved.",
                       prefix="user_data", output_type=str),
        OutputArgument(name="email", description="The email of User retrieved.",
                       prefix="user_data", output_type=str),
    ],
    description="This command gives all users depending on inputs given")
def get_all_users(client: Client):
    try:
        user_data = client.get_users_list()
        demisto.info(f"users retrieved when executing {demisto.command()} command \n Data: \n{user_data}")

        human_readable = tableToMarkdown(name="user data", t=user_data, headers=['id', 'name', 'email'])
        outputs = user_data
        result = CommandResults(
            outputs_prefix="user_data",
            outputs=outputs,
            readable_output=human_readable
        )

        return result, True
    except Exception as e:
        demisto.error(f"{traceback.format_exc()}, {e.__dict__}")  # log exception for debugging purposes
        return CommandResults(outputs=f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}"), False


@metadata_collector.command(
    command_name="safebreach-get-user-with-matching-name-or-email",
    inputs_list=[
        InputArgument(name="name", description="Name of the user to lookup.", required=False, is_array=False),
        InputArgument(name="email", description="Email of the user to lookup.", required=True, is_array=False)
    ],
    outputs_prefix="filtered_users",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User retrieved.",
                       prefix="user_data", output_type=int),
        OutputArgument(name="name", description="The name of User retrieved.",
                       prefix="user_data", output_type=str),
        OutputArgument(name="email", description="The email of User retrieved.",
                       prefix="user_data", output_type=str),
    ],
    description="This command gives all users depending on inputs given")
def get_user_id_by_name_or_email(client: Client, name: str, email: str):
    user_list = client.get_users_list()
    filtered_user_list = list(
        filter(lambda user_data: ((name in user_data['name']) or (email in user_data['email'])), user_list))
    if filtered_user_list:

        human_readable = tableToMarkdown(name="user data", t=filtered_user_list, headers=['id', 'name', 'email'])
        outputs = filtered_user_list

        result = CommandResults(
            outputs_prefix="filtered_users",
            outputs=outputs,
            readable_output=human_readable
        )

        return (result, True)
    return (CommandResults(outputs=[])), False


@metadata_collector.command(
    command_name="safebreach-create-user",
    inputs_list=[
        InputArgument(name="Name", description="Name of the user to create.", required=False, is_array=False),
        InputArgument(name="Email", description="Email of the user to Create.", required=True,
                      is_array=False),
        InputArgument(name="Is Active", description="Whether the user is active upon creation.",
                      required=False, is_array=False, options=["True", "False"], default="False"),
        InputArgument(name="Email Post Creation", description="Should Email be sent to user on creation",
                      required=False, is_array=False, options=["True", "False"], default="False"),
        InputArgument(name="Password", description="Password of user being created.", required=True,
                      is_array=False),
        InputArgument(name="Admin Name", description="Name of the Admin creating user.", required=False,
                      is_array=False),
        InputArgument(name="Change Password on create", description="Should user change password on creation",
                      required=False, is_array=False, options=["True", "False"], default="False"),
        InputArgument(name="User role", description="Role of the user being Created", required=False,
                      is_array=False,
                      options=["viewer", "administrator", "contentDeveloper", "operator"], default="viewer"),
        InputArgument(name="Deployments", description="Comma separated ID of all deployments the \
                                user should be part of", required=False, is_array=True)
    ],
    outputs_prefix="user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User created.", prefix="user_data", output_type=int),
        OutputArgument(name="name", description="The name of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="email", description="The email of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="deletedAt", description="The Deletion time of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="roles", description="The roles of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="role", description="The role of User created.", prefix="user_data",
                       output_type=str),
        OutputArgument(name="deployments", description="The deployments user is part of.", prefix="user_data",
                       output_type=str),
    ],
    description="This command creates a user with given data")
def create_user(client: Client):
    try:
        created_user = client.create_user_data()
        if created_user.status_code == 409:
            return json.dumps(created_user.json()), False
        created_user = created_user.json()

        human_readable = tableToMarkdown(name="Created User Data", t=created_user.get("data", {}),
                                         headers=['id', 'name', 'email', "mustChangePassword", "roles", "description", "role",
                                                  "isActive", "deployments", "createdAt"])
        outputs = created_user.get("data", {})

        result = CommandResults(
            outputs_prefix="user_data",
            outputs=outputs,
            outputs_key_field="user_data",
            readable_output=human_readable
        )
        return result, True

    except Exception as e:
        demisto.error(traceback.format_exc())  # log exception for debugging purposes
        return CommandResults(outputs=f"Failed to execute {demisto.command()} command.\nError:\n{str(e)}"), False


def main() -> None:
    """main function, parses params and runs command functions

    :return:
    :rtype:
    """
    client = Client(
        api_key=demisto.params().get("api_key"),
        account_id=demisto.params().get("account_id"),
        base_url=demisto.params().get("base_url"),
        verify=demisto.params().get("verify"))
    demisto.debug(f'Command being called is {demisto.command()}')
    try:

        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result, _ = client.get_all_users_for_test()
            return_results(result)

        elif demisto.command() == "safebreach-get-all-users":
            users, status = get_all_users(client=client)
            return_results(users) if status else return_error(users)

        elif demisto.command() == "safebreach-get-user-with-matching-name-or-email":
            name = demisto.args().get("name")
            email = demisto.args().get("email")
            result, status = get_user_id_by_name_or_email(client=client, name=name, email=email)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-create-user":

            user, status = create_user(client=client)
            return_results(user) if status else return_error(user)

        elif demisto.command() == "safebreach-delete-user":
            user_id = demisto.args().get("user_id")
            user_email = demisto.args().get("email")
            if user_email and not user_id:
                user_list = client.get_users_list()
                demisto.info("retrieved user list which contains all available users in safebreach")
                user = filter(lambda user_data: user_data["email"] == user_email, user_list)
                if user:
                    user_id = int(user["id"])
                    demisto.info("user has been found and details are being given for deleting user")
            user, status = client.delete_user(user_id=user_id)
            return_results(user) if status else return_error(user)
            # demisto.info(f"user has not been found with given details user_id {user_id} and email {user_email}")
            # return_results(f"no user with given email {user_email} or id {user_id} was found")

        elif demisto.command() == 'update-user-details':
            user_id = demisto.args().get("user_id")
            user_email = demisto.args().get("email")

            name = demisto.args().get("name")
            is_active = literal_eval(demisto.args().get("is_active", False))
            description = demisto.args().get("user_description", "")
            role = demisto.args().get("role", "viewer")
            deployment_list = demisto.args().get("deployment_list", [])
            deployment_list = list(literal_eval(deployment_list)) if deployment_list else []
            details = {
                "name": name,
                "is_active": is_active,
                "role": role,
                "deployments": deployment_list,
                "description": description
            }
            if user_email and not user_id:
                user_list = client.get_users_list()
                demisto.info("retrieved user list which contains all available users in safebreach")
                user = list(filter(lambda user_data: user_data["email"] == user_email, user_list))
                if user:
                    user_id = user[0]["id"]
                    demisto.info("user has been found and details are being given for updating user")
            user, status = client.update_user_with_details(user_id, details)
            return_results(user) if status else return_error(user)

        elif demisto.command() == 'create-deployment':
            name = demisto.args().get("name")
            nodes = demisto.args().get("nodes", []).replace('"', "").split(",")
            deployment, status = client.create_deployment(name, nodes)

            demisto.info(f"deployment created is {deployment}")
            return_results(deployment) if status else return_error(deployment)

        elif demisto.command() == 'update-deployment':
            deployment_id = demisto.args().get("deployment_id")
            deployment_name = demisto.args().get("deployment_name")

            if deployment_name and not deployment_id:
                needed_deployment = client.get_deployment_id_by_name(deployment_name)
                if needed_deployment:
                    deployment_id = needed_deployment['name']
            if deployment_id:
                name = demisto.args().get("updated_deployment_name")
                nodes = demisto.args().get("updated_nodes", []).replace('"', "").split(",")
                deployment, status = client.update_deployment(deployment_id, name, nodes)

                demisto.info(f"deployment updated is {deployment}")
                return_results(deployment) if status else return_error(deployment)
            else:
                return_error(f"no deployment with deployment name {deployment_name} na deployment id \
                    {deployment_id} has been found to update")

        elif demisto.command() == "delete-deployment":
            deployment_id = demisto.args().get("deployment_id")
            deployment_name = demisto.args().get("deployment_name")

            if deployment_name and not deployment_id:
                needed_deployment = client.get_deployment_id_by_name(deployment_name)
                if needed_deployment:
                    deployment_id = needed_deployment['name']

            if deployment_id:
                deployment, status = client.delete_deployment(deployment_id)
                demisto.info(f"deployment updated is {deployment}")
                return_results(deployment) if status else return_error(deployment)
            else:
                return_error(f"no deployment with deployment name {deployment_name} na deployment id \
                    {deployment_id} has been found to delete")

        elif demisto.command() == "safebreach-get-test-summary":
            includeArchived = demisto.args().get("include_archived")
            size = demisto.args().get("entries_per_page")
            status = demisto.args().get("status_of_test")
            planId = demisto.args().get("plan_id")
            simulation_id = demisto.args().get("simulation_id")
            sort_by = demisto.args().get("sort_by")

            result, status = client.get_tests_summary(includeArchived, size, status, planId, simulation_id, sort_by)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-test-summary-of-given-test":
            test_id = demisto.args().get("test_id")
            soft_delete = demisto.args().get("soft_delete")

            result, status = client.delete_test_result_of_test(test_id, soft_delete)
            return_results(f'test with plan run id {result}, has been deleted') if status else return_error(result)

        elif demisto.command() == "safebreach-get-test-summary-with-plan-run-id":
            includeArchived = demisto.args().get("include_archived")
            size = demisto.args().get("entries_per_page")
            status = demisto.args().get("status_of_test")
            planId = demisto.args().get("plan_id")
            simulation_id = demisto.args().get("simulation_id")
            sort_by = demisto.args().get("sort_by")

            result, status = client.get_test_summary(includeArchived, size, status, planId, simulation_id, sort_by)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-integration-errors":
            result, status = client.get_all_error_logs()
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-generate-api-key":
            name = demisto.args().get("name")
            description = demisto.args().get("description")

            result, status = client.generate_api_key_and_table(name, description)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-api-key":
            name = demisto.args().get("name")

            result, status = client.delete_api_key_with_given_name(name)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-available-simulator-count":

            result, status = client.get_simulator_quota_with_table()
            return_results(result) if status else return_error

        elif demisto.command() == "safebreach-get-available-simulator-details":

            result, status = client.get_simulators_and_display_in_table()
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-simulator-with-name":

            result, status = client.get_simulators_and_display_in_table(just_name=True)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-simulator-with-name":

            result, status = client.delete_simulator_with_given_name()
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-update-simulator-with-given-name":

            result, status = client.update_simulator_with_given_name()
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-rotate-verification-token":

            result, status = client.return_rotated_verification_token()
            return_results(result) if status else return_error(result)

    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())  # print the traceback
        return_error(f'Failed to execute {demisto.command()} command {traceback.format_exc()}.\nError:\n{str(e)}')


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
