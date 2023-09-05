import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
"""
New Integration starts from here

"""
import random
from ast import literal_eval

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

simulator_details_inputs = [
    InputArgument(name="details", description="if details are to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="deleted", description="if deleted are to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="secret", description="if secrets are to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="shouldIncludeProxies", description="if proxies are to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="hostname", description="if hostname to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="connectionType", description="if connectionType to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="externalIp", description="if external IP details to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="internalIp", description="if Internal IP are to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="os", description="if Operating system details to be included for search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="sortDirection", description="direction in which secrets are to be sorted.", options=["asc", "desc"],
                  default="asc", required=False, is_array=False),
    InputArgument(name="startRow", description="if there are too many entries then where should we start looking from.",
                  required=False, is_array=False),
    InputArgument(name="pageSize", description="number of entries to search.", required=False, is_array=False),
    InputArgument(name="isEnabled", description="if to search only enabled ones.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="isConnected", description="status of connection of nodes to search.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="isCritical", description="whether to search only for critical nodes or not", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="assets", description="Whether search only for assets and which assets.", required=False, is_array=False),
    InputArgument(name="additionalDetails", description="Whether to show additional details or not",
                  options=["true", "false"], default="false", required=False, is_array=False),
    InputArgument(name="impersonatedUsers", description="should search only for impersonated user targets or not",
                  options=["true", "false"], default="false", required=False, is_array=False),
    InputArgument(name="isAzureAttacker", description="Whether to search only for azure attackers",
                  options=["true", "false"], default="false", required=False, is_array=False),
    InputArgument(name="isAwsAttacker", description="Whether to search only for aws attacker.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="isPreExecutor", description="should search only for pre-executors or not",
                  options=["true", "false"], default="false", required=False, is_array=False),
    InputArgument(name="isInfiltrationTarget", description="Whether to search only for infiltration targets",
                  options=["true", "false"], default="false", required=False, is_array=False),
    InputArgument(name="isMailTarget", description="Whether to search only for Mail targets.", options=["true", "false"],
                  default="false", required=False, is_array=False),
    InputArgument(name="isExfiltrationTarget", description="should search only for exfiltration targets or not",
                  options=["true", "false"], default="false", required=False, is_array=False),

    # These fields need to be '|' separated  arrays
    InputArgument(name="deployments", description="deployments list which the search should look",
                  required=False, is_array=True),
    InputArgument(name="advancedActions", description="advanced actions to search",
                  required=False, is_array=True),
    InputArgument(name="roles", description="roles to search",
                  required=False, is_array=True),
    InputArgument(name="userids", description="userids to search",
                  required=False, is_array=True),
    InputArgument(name="versions", description="versions to filter by",
                  required=False, is_array=True),
    # '|' separated arrays end

    # normal arrays start
    InputArgument(name="proxyIds", description="proxy ids to search",
                  required=False, is_array=True),
    InputArgument(name="assetIds", description="asset ids to search",
                  required=False, is_array=True),
    # normal arrays end

    # enums start
    InputArgument(name="status", description="if simulator status are to be included for search.",
                  options=["APPROVED", "PENDING", "ALL"],
                  default="ALL", required=False, is_array=False),
    # enums end
]

simulators_output_fields = [
    OutputArgument(name="is_enabled", description="Whether the node is enabled or not.",
                   output_type=str),
    OutputArgument(name="simulator_id", description="The Id of given simulator.",
                   output_type=str),
    OutputArgument(name="simulator_name", description="name for given simulator.",
                   output_type=str),
    OutputArgument(name="account_id", description="Account Id of account Hosting given simulator",
                   output_type=str),
    OutputArgument(name="is_critical", description="Whether the simulator is critical",
                   output_type=str),
    OutputArgument(name="is_exfiltration", description="If Simulator is exfiltration target",
                   output_type=int),
    OutputArgument(name="is_infiltration", description="If simulator is infiltration target.",
                   output_type=int),
    OutputArgument(name="is_mail_target", description="If simulator is mail target.",
                   output_type=int),
    OutputArgument(name="is_mail_attacker", description="If simulator is mail attacker.",
                   output_type=int),
    OutputArgument(name="is_pre_executor", description="Whether the node is pre executor.",
                   output_type=int),
    OutputArgument(name="is_aws_attacker", description="if the given simulator is aws attacker.",
                   output_type=str),
    OutputArgument(name="is_azure_attacker", description="If the given simulator is azure attacker",
                   output_type=str),
    OutputArgument(name="external_ip", description="external ip of given simulator",
                   output_type=str),
    OutputArgument(name="internal_ip", description="internal ip of given simulator",
                   output_type=str),
    OutputArgument(name="is_web_application_attacker", description="Whether the simulator is Web application attacker",
                   output_type=str),
    OutputArgument(name="preferred_interface", description="Preferred simulator interface",
                   output_type=int),
    OutputArgument(name="preferred_ip", description="Preferred Ip of simulator.",
                   output_type=int),
    OutputArgument(name="hostname", description="Hostname of given simulator",
                   output_type=str),
    OutputArgument(name="connection_type", description="connection_type of given simulator",
                   output_type=str),
    OutputArgument(name="simulator_status", description="status of the simulator",
                   output_type=str),
    OutputArgument(name="connection_status", description="connection status of node/simulator",
                   output_type=int),
    OutputArgument(name="simulator_framework_version", description="Framework version of simulator.",
                   output_type=int),
    OutputArgument(name="operating_system_type", description="operating system type of given simulator",
                   output_type=str),
    OutputArgument(name="operating_system", description="Operating system of given simulator",
                   output_type=str),
    OutputArgument(name="execution_hostname", description="Execution Hostname of the given node",
                   output_type=str),
    OutputArgument(name="deployments", description="deployments simulator is part of",
                   output_type=int),
    OutputArgument(name="created_at", description="Creation datetime of simulator.",
                   output_type=int),
    OutputArgument(name="updated_at", description="Update datetime of given simulator",
                   output_type=str),
    OutputArgument(name="deleted_at", description="deletion datetime of given simulator",
                   output_type=str),
    OutputArgument(name="assets", description="Assets of given simulator",
                   output_type=str),
    OutputArgument(name="simulation_users", description="simulator users list",
                   output_type=int),
    OutputArgument(name="proxies", description="Proxies of simulator.",
                   output_type=int),
    OutputArgument(name="advanced_actions", description="Advanced simulator details.",
                   output_type=int)
]

simulator_details_for_update_fields = [
    InputArgument(name="isEnabled", description="set true to enable the node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isProxySupported", description="set true to enable the proxy support",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isCritical", description="set true to make node as critical node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isExfiltration", description="set true to make the node as exfiltration node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isInfiltration", description="set true to make the node as infiltration node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isMailTarget", description="set true to make node as mail target",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isMailAttacker", description="set true to make node as MailAttacker node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isPreExecutor", description="set true to enable the node as PreExecutor node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isAWSAttacker", description="set true to make node as AWS attacker target",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isAzureAttacker", description="set true to make node as Azure attacker node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isWebApplicationAttacker", description="set true to enable the node as web application attacker node",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="useSystemUser", description="set true to enable the node get system user access",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="connectionUrl", description="the given value will be set as connection string",
                  required=False, is_array=False),
    InputArgument(name="cloudProxyUrl", description="the given value will be set as cloud proxy url",
                  required=False, is_array=False),
    InputArgument(name="name", description="the given value will be set as name of simulator",
                  required=False, is_array=False),
    InputArgument(name="preferredInterface", description="the given value will be set as preferred interface string",
                  required=False, is_array=False),
    InputArgument(name="preferredIp", description="the given value will be set as Preferred IP",
                  required=False, is_array=False),
    InputArgument(name="tunnel", description="the given value will be set as tunnel",
                  required=False, is_array=False),
]

simulation_output_fields = [
    OutputArgument(name="planId", description="Plan ID of the simulation", output_type=str),
    OutputArgument(name="planName", description="Plan Name of the simulation", output_type=str),
    OutputArgument(name="securityActionPerControl", description="Security Actions of the simulation", output_type=str),
    OutputArgument(name="planRunId", description="Plan Run ID of the simulation", output_type=str),
    OutputArgument(name="runId", description="Run ID of the simulation", output_type=str),
    OutputArgument(name="status", description="status of the simulation", output_type=str),
    OutputArgument(name="plannedSimulationsAmount", description="Planned simulations amount of the simulation", output_type=str),
    OutputArgument(name="simulatorExecutions", description="simulator executions of the simulation", output_type=str),
    OutputArgument(name="ranBy", description="user who started the simulation", output_type=str),
    OutputArgument(name="simulatorCount", description="simulators count of simulation", output_type=str),
    OutputArgument(name="endTime", description="End Time of the simulation", output_type=str),
    OutputArgument(name="startTime", description="start time of the simulation", output_type=str),
    OutputArgument(name="finalStatus.stopped", description="stopped count of simulation", output_type=str),
    OutputArgument(name="finalStatus.missed", description="missed count of simulation", output_type=str),
    OutputArgument(name="finalStatus.logged", description="logged count of simulation", output_type=str),
    OutputArgument(name="finalStatus.detected", description="detected count of simulation", output_type=str),
    OutputArgument(name="finalStatus.prevented", description="prevented count of simulation", output_type=str),
    OutputArgument(name="finalStatus.inconsistent", description="inconsistent count of simulation", output_type=str),
    OutputArgument(name="finalStatus.drifted", description="drifted count of simulation", output_type=str),
    OutputArgument(name="finalStatus.not_drifted", description="not drifted count of simulation", output_type=str),
    OutputArgument(name="finalStatus.baseline", description="baseline count of simulation", output_type=str),
]

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
    docker_image="demisto/python3:3.10.13.72123",
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
                  required=False,
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
            # print(f"response, {response.__dict__}, request, {response.__dict__['request'].__dict__}")  # noqa: T201
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

    def delete_user(self):

        user_id = demisto.args().get("User ID")
        user_email = demisto.args().get("Email")
        if user_email and not user_id:
            user_list = self.get_users_list()
            demisto.info("retrieved user list which contains all available users in safebreach")
            user = list(filter(lambda user_data: user_data["email"] == user_email, user_list))
            if user:
                user_id = int(user[0]["id"])
                demisto.info("user has been found and details are being given for deleting user")

        account_id = demisto.params().get("account_id", 0)
        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/users/{user_id}"

        deleted_user = self.get_response(url=url, method=method)
        return deleted_user

    def update_user_with_details(self, user_id: str, user_details: dict):
        for key in list(user_details.keys()):
            if not user_details[key]:
                user_details.pop(key)

        account_id = demisto.params().get("account_id", 0)
        method = "PUT"
        url = f"/config/v1/accounts/{account_id}/users/{int(user_id)}"

        updated_user = self.get_response(url=url, method=method, body=user_details)
        return updated_user

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

    def create_deployment_data(self):

        account_id = demisto.params().get("account_id", 0)
        name = demisto.args().get("Name")
        description = demisto.args().get("Description")
        nodes = demisto.args().get("Nodes", "").replace('"', "").split(",")
        deployment_payload = {
            "nodes": nodes,
            "name": name,
            "description": description,
            "id": random.getrandbits(20)
        }

        method = "POST"
        url = f"/config/v1/accounts/{account_id}/deployments"
        created_deployment = self.get_response(url=url, method=method, body=deployment_payload)
        return created_deployment

    def update_deployment(self):
        account_id = demisto.params().get("account_id", 0)
        deployment_id = demisto.args().get("Deployment ID", None)
        deployment_name = demisto.args().get("Deployment Name")

        if deployment_name and not deployment_id:
            needed_deployment = self.get_deployment_id_by_name(deployment_name)
            if needed_deployment:
                deployment_id = needed_deployment['name']
        if deployment_id:
            name = demisto.args().get("Updated Deployment Name")
            nodes = demisto.args().get("Updated Nodes for Deployment", None)
            description = demisto.args().get("Updated deployment description")
        else:
            raise Exception(f"Could not find Deployment with details Name:\
                {deployment_name} and Deployment ID : {deployment_id}")
        deployment_payload = {}
        if name:
            deployment_payload["name"] = name
        if nodes:
            deployment_payload["nodes"] = nodes.replace('"', "").split(",")
        if description:
            deployment_payload["description"] = description

        method = "PUT"
        url = f"/config/v1/accounts/{account_id}/deployments/{deployment_id}"
        updated_deployment = self.get_response(url=url, method=method, body=deployment_payload)
        return updated_deployment

    def delete_deployment(self):

        account_id = demisto.params().get("account_id", 0)
        deployment_id = demisto.args().get("Deployment ID", None)
        deployment_name = demisto.args().get("Deployment Name")

        if deployment_name and not deployment_id:
            needed_deployment = self.get_deployment_id_by_name(deployment_name)
            if needed_deployment:
                deployment_id = needed_deployment['name']
        if deployment_id:
            method = "DELETE"
            url = f"/config/v1/accounts/{account_id}/deployments/{deployment_id}"
            deleted_deployment = self.get_response(url=url, method=method)
            return deleted_deployment
        else:
            raise Exception(f"Could not find Deployment with details Name:\
                {deployment_name} and Deployment ID : {deployment_id}")

    def get_tests_with_args(self):
        account_id = demisto.params().get("account_id", 0)

        include_archived = demisto.args().get("Include Archived")
        size = demisto.args().get("Entries per Page")
        status = demisto.args().get("Status")
        plan_id = demisto.args().get("Plan ID")
        simulation_id = demisto.args().get("Simulation ID")
        sort_by = demisto.args().get("Sort By")

        parameters = {}
        method = "GET"
        url = f"/data/v1/accounts/{account_id}/testsummaries"
        for param in [("includeArchived", include_archived), ("size", size), ("status", status), ("planId", plan_id),
                      ("simulationId", simulation_id), ("sortBy", sort_by)]:
            parameters.update({} if not param[1] else {param[0]: param[1]})

        test_summaries = self.get_response(url=url, method=method, request_params=parameters)
        return test_summaries

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

    def delete_test_result_of_test(self):
        account_id = demisto.params().get("account_id", 0)
        test_id = demisto.args().get("Test ID")
        soft_delete = demisto.args().get("Soft Delete")

        method = "DELETE"
        url = f"/data/v1/accounts/{account_id}/tests/{test_id}"
        request_parameters = {
            "softDelete": soft_delete
        }

        test_summaries = self.get_response(url=url, method=method, request_params=request_parameters)
        return test_summaries

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
        method = "GET"
        url = f"/siem/v1/accounts/{account_id}/config/providers/status"

        error_logs = self.get_response(url=url, method=method)
        return error_logs

    def delete_integration_error_logs(self):
        account_id = demisto.params().get("account_id", 0)
        connector_id = demisto.args().get("Connector ID")

        method = "DELETE"
        url = f"/siem/v1/accounts/{account_id}/config/providers/status/delete/{connector_id}"

        error_logs = self.get_response(url=url, method=method)
        return error_logs

    def generate_api_key(self):
        account_id = demisto.params().get("account_id", 0)
        name = demisto.args().get("Name")
        description = demisto.args().get("Description")
        method = "POST"
        url = f"/config/v1/accounts/{account_id}/apikeys"
        data = {}
        if name:
            data["name"] = name
        if description:
            data['description'] = description

        generated_api_key = self.get_response(method=method, url=url, body=data)
        return generated_api_key

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
        raise Exception(f"couldn't find APi key with given name: {key_name}")

    def delete_api_key(self):
        key_name = demisto.args().get("Key Name")
        key_id, status = self.filter_api_key_with_key_name(key_name=key_name)
        account_id = demisto.params().get("account_id", 0)
        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/apikeys/{key_id}"
        deleted_api_key = self.get_response(method=method, url=url)
        return deleted_api_key

    def get_simulator_quota(self):
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}"
        simulator_details = self.get_response(method=method, url=url)
        return simulator_details

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
        raise Exception(f"No Matching simulators found with details name: {demisto.args().get('simulator_name')}")

    def create_get_simulator_params_dict(self):
        possible_inputs = [
            "details", "deleted", "secret", "shouldIncludeProxies", "hostname", "connectionType", "externalIp", "internalIp",
            "os", "status", "sortDirection", "startRow", "pageSize", "isEnabled", "isConnected", "isCritical",
            "isExfiltrationTarget", "isInfiltrationTarget", "isMailTarget", "isMailAttacker", "isPreExecutor",
            "isAwsAttacker", "isAzureAttacker", "impersonatedUsers", "assets", "advancedActions", "deployments",
            "additionalDetails"]
        request_params = {}
        for parameter in possible_inputs:
            if demisto.args().get(parameter) and demisto.args().get(parameter) != 'false':
                request_params[parameter] = demisto.args().get(parameter)
        return request_params

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
            flattened_nodes.append(node_details)

        return flattened_nodes, keys

    def get_simulator_with_name_request_params(self):
        name = demisto.args().get("Simulator/Node Name")
        request_params = {
            "name": name,
            "deleted": "true",
            "details": "true"
        }
        return request_params

    def get_simulator_with_a_name_return_id(self):
        request_params = self.get_simulator_with_name_request_params()
        result, status = self.get_simulators_details(request_params=request_params)
        if status:
            try:
                simulator_id = result.get("data", {}).get("rows", {})[0].get("id")
                return simulator_id
            except IndexError:
                raise Exception("Simulator with given details could not be found")
        raise Exception("Simulator with given details could not be found")

    def delete_node_with_given_id(self, node_id, force: str):
        request_params = {
            "force": force
        }
        method = "DELETE"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{node_id}"

        deleted_node = self.get_response(url=request_url, method=method, request_params=request_params)
        return deleted_node

    def delete_simulator_with_given_name(self):
        simulator_id = self.get_simulator_with_a_name_return_id()
        force_delete = demisto.args().get("Should Force Delete")
        result = self.delete_node_with_given_id(node_id=simulator_id, force=force_delete)
        return result

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
        return updated_node

    def update_simulator_with_given_name(self):
        simulator_id = self.get_simulator_with_a_name_return_id()
        payload = self.make_update_node_payload()
        updated_node = self.update_node(node_id=simulator_id, node_data=payload)
        return updated_node

    def rotate_verification_token(self):
        method = "POST"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/secret/rotate"

        new_token = self.get_response(url=request_url, method=method, body={})
        return new_token

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
        method = "POST"
        url = f"/config/v1/accounts/{account_id}/users"
        created_user = self.get_response(url=url, method=method, body=user_payload)
        return created_user

    def update_user_data(self):
        user_id = demisto.args().get("User ID")
        user_email = demisto.args().get("Email")

        name = demisto.args().get("Name")
        is_active = literal_eval(demisto.args().get("Is Active", False))
        description = demisto.args().get("User Description", "")
        role = demisto.args().get("User role")
        password = demisto.args().get("Password")
        deployment_list = demisto.args().get("Deployments", [])
        deployment_list = list(literal_eval(deployment_list)) if deployment_list else []
        details = {
            "name": name,
            "is_active": is_active,
            "deployments": deployment_list,
            "description": description
        }
        if role:
            details["role"] = role
        if password:
            details["password"] = password
        if user_email and not user_id:
            user_list = self.get_users_list()
            demisto.info("retrieved user list which contains all available users in safebreach")
            user = list(filter(lambda user_data: user_data["email"] == user_email, user_list))
            if user:
                user_id = user[0]["id"]
                demisto.info("user has been found and details are being given for updating user")
        user = self.update_user_with_details(user_id, details)
        return user


def get_simulators_and_display_in_table(client: Client, just_name=False):

    request_params = client.get_simulator_with_name_request_params() if just_name \
        else client.create_get_simulator_params_dict()
    result, status = client.get_simulators_details(request_params=request_params)
    if status:
        flattened_nodes, keys = client.flatten_node_details(result.get("data", {}).get("rows", {}))
        human_readable = tableToMarkdown(
            name="Simulators Details",
            t=flattened_nodes,
            headers=keys)
        outputs = result.get("data", {}).get("rows")[0]

        result = CommandResults(
            outputs_prefix="simulator_details",
            outputs=outputs,
            readable_output=human_readable
        )
        return result, True
    return result, status


def get_tests_summary(client: Client):
    test_summaries = client.get_tests_with_args()
    if test_summaries.status_code == 409:
        return json.dumps(test_summaries.json()), False
    test_summaries = test_summaries.json()

    client.flatten_test_summaries(test_summaries)
    human_readable = tableToMarkdown(
        name="Test Results",
        t=test_summaries,
        headers=['planId', "planName", 'securityActionPerControl', 'planRunId', "runId", "status",
                 "plannedSimulationsAmount", "simulatorExecutions", "ranBy", "simulatorCount", "endTime", "startTime",
                 "finalStatus", "stopped", "missed", "logged", "detected", "prevented",
                 "inconsistent", "drifted", "not_drifted", "baseline"])
    outputs = [{
        'tests': test_summaries
    }]

    result = CommandResults(
        outputs_prefix="tests_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result, True


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
def get_user_id_by_name_or_email(client: Client):
    name = demisto.args().get("name")
    email = demisto.args().get("email")
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
    raise Exception(f"user with name {name} or email {email} was not found")


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
        InputArgument(name="Deployments", description="Comma separated ID of all deployments the user should be part of",
                      required=False, is_array=True)
    ],
    outputs_prefix="created_user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User created.", prefix="created_user_data", output_type=int),
        OutputArgument(name="name", description="The name of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="email", description="The email of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="deletedAt", description="The Deletion time of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="roles", description="The roles of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="role", description="The role of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="deployments", description="The deployments user is part of.", prefix="created_user_data",
                       output_type=str),
    ],
    description="This command creates a user with given data")
def create_user(client: Client):

    created_user = client.create_user_data()
    if created_user.status_code == 409:
        return json.dumps(created_user.json()), False
    created_user = created_user.json()

    human_readable = tableToMarkdown(name="Created User Data", t=created_user.get("data", {}),
                                     headers=['id', 'name', 'email', "mustChangePassword", "roles", "description",
                                              "role", "isActive", "deployments", "createdAt"])
    outputs = created_user.get("data", {})

    result = CommandResults(
        outputs_prefix="created_user_data",
        outputs=outputs,
        outputs_key_field="created_user_data",
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-update-user-details",
    inputs_list=[
        InputArgument(name="User ID", description="user ID of user from safebreach to search",
                      required=False, is_array=False),
        InputArgument(name="Email", description="Email of the user to Search for updating user details.", required=True,
                      is_array=False),
        InputArgument(name="Name", description="Update the user name to given string.",
                      required=False, is_array=False),
        InputArgument(name="User Description", description="Update the user Description to given string.",
                      required=False, is_array=False),
        InputArgument(name="Is Active", description="Update the user Status.",
                      required=False, is_array=False, options=["True", "False", ""], default=""),
        InputArgument(name="Password", description="Password of user to be updated with.", required=False,
                      is_array=False),
        InputArgument(name="User role", description="Role of the user to be changed to", required=False,
                      is_array=False,
                      options=["viewer", "administrator", "contentDeveloper", "operator"], default="viewer"),
        InputArgument(name="Deployments", description="Comma separated ID of all deployments the user should be part of",
                      required=False, is_array=True)
    ],
    outputs_prefix="updated_user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User created.", prefix="updated_user_data", output_type=int),
        OutputArgument(name="name", description="The name of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="email", description="The email of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="deletedAt", description="The Deletion time of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="roles", description="The roles of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="role", description="The role of User created.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="deployments", description="The deployments user is part of.", prefix="updated_user_data",
                       output_type=str),
    ],
    description="This command updates a user with given data")
def update_user_with_details(client: Client):

    updated_user = client.update_user_data()

    if updated_user.status_code == 400:
        return json.dumps(updated_user.json()), False

    updated_user = updated_user.json()
    human_readable = tableToMarkdown(name="Updated User Data", t=updated_user.get("data", {}),
                                     headers=['id', 'name', 'email', "deletedAt", "roles", "description",
                                              "role", "deployments", "createdAt", "updatedAt"])
    outputs = updated_user.get("data", {})

    result = CommandResults(
        outputs_prefix="updated_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-delete-user",
    inputs_list=[
        InputArgument(name="User ID", description="user ID of user from safebreach to search",
                      required=False, is_array=False),
        InputArgument(name="Email", description="Email of the user to Search for updating user details.", required=True,
                      is_array=False)
    ],
    outputs_prefix="deleted_user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User deleted.", prefix="deleted_user_data", output_type=int),
        OutputArgument(name="name", description="The name of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="email", description="The email of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="deletedAt", description="The Deletion time of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="roles", description="The roles of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="role", description="The role of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="deployments", description="The deployments user was part of.", prefix="deleted_user_data",
                       output_type=str),
    ],
    description="This command deletes a user with given data")
def delete_user_with_details(client: Client):

    deleted_user = client.delete_user()
    if deleted_user.status_code == 400:
        return json.dumps(deleted_user.json()), False

    deleted_user = deleted_user.json()

    human_readable = tableToMarkdown(name="Deleted User Data", t=deleted_user.get("data", {}),
                                     headers=['id', 'name', 'email', "deletedAt", "roles",
                                              "description", "role", "deployments", "createdAt"])
    outputs = deleted_user.get("data", {})
    result = CommandResults(
        outputs_prefix="deleted_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-create-deployment",
    inputs_list=[
        InputArgument(name="Name", description="Name of the deployment to create.", required=False, is_array=False),
        InputArgument(name="Description", description="Description of the deployment to create.", required=False, is_array=False),
        InputArgument(name="Nodes", description="Comma separated ID of all nodes the deployment should be part of",
                      required=False, is_array=True)
    ],
    outputs_prefix="created_deployment_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of deployment created.", prefix="created_deployment_data", output_type=int),
        OutputArgument(name="accountId", description="The account of deployment created.", prefix="created_deployment_data",
                       output_type=str),
        OutputArgument(name="name", description="The name of deployment created.", prefix="created_deployment_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of deployment created.", prefix="created_deployment_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of deployment created.", prefix="created_deployment_data",
                       output_type=str),
        OutputArgument(name="nodes", description="The nodes that are part of deployment.", prefix="created_deployment_data",
                       output_type=str),
    ],
    description="This command creates a deployment with given data")
def create_deployment(client: Client):

    created_deployment = client.create_deployment_data()
    if created_deployment.status_code == 409:
        return json.dumps(created_deployment.json()), False
    created_deployment = created_deployment.json()

    human_readable = tableToMarkdown(name="Created Deployment", t=created_deployment.get("data", {}),
                                     headers=['id', "accountId", 'name', 'createdAt', "description", "nodes"])
    outputs = created_deployment.get("data", {})

    result = CommandResults(
        outputs_prefix="created_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result, True


@metadata_collector.command(
    command_name="safebreach-update-deployment",
    inputs_list=[
        InputArgument(name="Deployment ID", description="Name of the deployment to update.", required=False, is_array=False),
        InputArgument(name="Deployment Name", description="Description of the deployment to update.",
                      required=False, is_array=False),
        InputArgument(name="Updated Nodes for Deployment", required=False, is_array=False,
                      description="Comma separated ID of all nodes the deployment should be part of"),
        InputArgument(name="Updated Deployment Name", description="Name of the deployment to update to.",
                      required=False, is_array=False),
        InputArgument(name="Updated deployment description", required=False, is_array=False,
                      description="name of the deployment to update to."),
    ],
    outputs_prefix="updated_deployment_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of deployment created.", prefix="updated_deployment_data", output_type=int),
        OutputArgument(name="accountId", description="The account of deployment created.", prefix="updated_deployment_data",
                       output_type=str),
        OutputArgument(name="name", description="The name of deployment created.", prefix="updated_deployment_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of deployment created.", prefix="updated_deployment_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of deployment created.", prefix="updated_deployment_data",
                       output_type=str),
        OutputArgument(name="nodes", description="The nodes that are part of deployment.", prefix="updated_deployment_data",
                       output_type=str),
    ],
    description="This command updates a deployment with given data")
def update_deployment(client: Client):

    updated_deployment = client.update_deployment()
    if updated_deployment.status_code == 409:
        return json.dumps(updated_deployment.json()), False
    updated_deployment = updated_deployment.json()

    human_readable = tableToMarkdown(name="Updated Deployment", t=updated_deployment.get("data", {}),
                                     headers=['id', "accountId", 'name', 'createdAt',
                                              "description", "nodes", "updatedAt"])
    outputs = updated_deployment.get("data", {})
    result = CommandResults(
        outputs_prefix="updated_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-delete-deployment",
    inputs_list=[
        InputArgument(name="Deployment ID", description="Name of the deployment to update.", required=False, is_array=False),
        InputArgument(name="Deployment Name", description="Description of the deployment to update.",
                      required=False, is_array=False),
    ],
    outputs_prefix="deleted_deployment_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of deployment created.", prefix="deleted_deployment_data", output_type=int),
        OutputArgument(name="accountId", description="The account of deployment created.", prefix="deleted_deployment_data",
                       output_type=str),
        OutputArgument(name="name", description="The name of deployment created.", prefix="deleted_deployment_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of deployment created.", prefix="deleted_deployment_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of deployment created.", prefix="deleted_deployment_data",
                       output_type=str),
        OutputArgument(name="nodes", description="The nodes that are part of deployment.", prefix="deleted_deployment_data",
                       output_type=str),
    ],
    description="This command deletes a deployment with given data")
def delete_deployment(client: Client):

    deleted_deployment = client.delete_deployment()
    if deleted_deployment.status_code == 409:
        return json.dumps(deleted_deployment.json()), False
    deleted_deployment = deleted_deployment.json()

    human_readable = tableToMarkdown(name="Deleted Deployment", t=deleted_deployment.get("data", {}),
                                     headers=['id', "accountId", 'name', 'createdAt',
                                              "description", "nodes", "updatedAt"])
    outputs = deleted_deployment.get("data", {})
    result = CommandResults(
        outputs_prefix="deleted_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-generate-api-key",
    inputs_list=[
        InputArgument(name="Name", description="Name of the API Key to create.", required=True, is_array=False),
        InputArgument(name="Description", description="Description of the API Key to create.", required=False, is_array=False),
    ],
    outputs_prefix="generated_api_key",
    outputs_list=[
        OutputArgument(name="name", description="The Name of API Key created.", prefix="generated_api_key", output_type=int),
        OutputArgument(name="description", description="The Description of API Key created.", prefix="generated_api_key",
                       output_type=str),
        OutputArgument(name="createdBy", description="The User ID of API key creator.", prefix="generated_api_key",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of API key.", prefix="generated_api_key",
                       output_type=str),
        OutputArgument(name="key", description="The API key Value.", prefix="generated_api_key",
                       output_type=str),
        OutputArgument(name="roles", description="The roles allowed for this api key.", prefix="generated_api_key",
                       output_type=str),
        OutputArgument(name="role", description="The role of API Key.", prefix="generated_api_key",
                       output_type=str),
    ],
    description="This command creates a API Key with given data")
def create_api_key(client: Client):

    generated_api_key = client.generate_api_key()
    if generated_api_key.status_code == 409:
        return json.dumps(generated_api_key.json()), False
    generated_api_key = generated_api_key.json()

    human_readable = tableToMarkdown(
        name="Generated API key Data",
        t=generated_api_key.get("data"),
        headers=["name", "description", "createdBy", "createdAt", "key", "roles", "role"])
    outputs = generated_api_key.get("data")
    result = CommandResults(
        outputs_prefix="generated_api_key",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-delete-api-key",
    inputs_list=[
        InputArgument(name="Key Name", description="Name of the API Key to Delete.", required=True, is_array=False),
    ],
    outputs_prefix="deleted_api_key",
    outputs_list=[
        OutputArgument(name="name", description="The Name of API Key deleted.", prefix="deleted_api_key", output_type=int),
        OutputArgument(name="description", description="The Description of API Key deleted.", prefix="deleted_api_key",
                       output_type=str),
        OutputArgument(name="createdBy", description="The User ID of API key creator.", prefix="deleted_api_key",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of API key.", prefix="deleted_api_key",
                       output_type=str),
        OutputArgument(name="deletedAt", description="The deletion time of API key.", prefix="deleted_api_key",
                       output_type=str),
    ],
    description="This command deletes a API key with given name")
def delete_api_key(client: Client):

    deleted_api_key = client.delete_api_key()
    if deleted_api_key.status_code == 409:
        return json.dumps(deleted_api_key.json()), False
    deleted_api_key = deleted_api_key.json()

    human_readable = tableToMarkdown(
        name="Deleted API key Data",
        t=deleted_api_key.get("data"),
        headers=["name", "description", "createdBy", "createdAt", "deletedAt"])
    outputs = deleted_api_key.get("data")
    result = CommandResults(
        outputs_prefix="deleted_api_key",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-get-integration-errors",
    inputs_list=None,
    outputs_prefix="integration_errors",
    outputs_list=[
        OutputArgument(name="connector", description="The connector ID of Integration connector retrieved.",
                       prefix="integration_errors", output_type=int),
        OutputArgument(name="action", description="The action of Integration connector error.",
                       prefix="integration_errors", output_type=str),
        OutputArgument(name="success", description="status of connector error.",
                       prefix="integration_errors", output_type=str),
        OutputArgument(name="error", description="Error description.",
                       prefix="integration_errors", output_type=str),
        OutputArgument(name="timestamp", description="Time of error.",
                       prefix="integration_errors", output_type=str),
    ],
    description="This command gives all connector related errors")
def get_all_error_logs(client: Client):

    formatted_error_logs = []
    error_logs = client.get_all_error_logs()
    if error_logs.status_code == 409:
        return json.dumps(error_logs.json()), False
    error_logs = error_logs.json()
    if error_logs.get("result"):
        formatted_error_logs = client.flatten_error_logs_for_table_view(error_logs.get("result"))
        human_readable = tableToMarkdown(
            name="Integration Connector errors",
            t=formatted_error_logs,
            headers=["action", "success", "error", "timestamp", "connector"])
        outputs = error_logs.get("result")
        result = CommandResults(
            outputs_prefix="Integration Error Data",
            outputs=outputs,
            readable_output=human_readable
        )
        return result, True
    return formatted_error_logs, True


@metadata_collector.command(
    command_name="safebreach-delete-integration-errors",
    inputs_list=[
        InputArgument(name="Connector ID", description="The connector ID of Integration connector to have its errors deleted.",
                      required=True, is_array=False),
    ],
    outputs_prefix="errors_cleared",
    outputs_list=[
        OutputArgument(name="error", description="Error count after deletion of errors for the given connector.",
                       prefix="integration_errors", output_type=int),
        OutputArgument(name="result", description="error deletion status whether true or false.",
                       prefix="integration_errors", output_type=str),
    ],
    description="This command deleted connector related errors")
def delete_integration_error_logs(client: Client):

    error_logs = client.delete_integration_error_logs()
    if error_logs.status_code == 409:
        return json.dumps(error_logs.json()), False
    error_logs = error_logs.json()
    human_readable = tableToMarkdown(
        name="Integration Connector errors Status",
        t=error_logs,
        headers=["error", "result"])
    outputs = error_logs
    result = CommandResults(
        outputs_prefix="errors_cleared",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-get-available-simulator-count",
    inputs_list=None,
    outputs_prefix="account_details",
    outputs_list=[
        OutputArgument(name="id", description="The account ID of account.",
                       prefix="account_details", output_type=int),
        OutputArgument(name="name", description="The Account Name of account being queried.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="contactName", description="Contact name for given account.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="contactEmail", description="Email of the contact person.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="userQuota", description="User Quota for the given account, max number of users for this account.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="nodesQuota", description="The simulator quota for the given account.",
                       prefix="account_details", output_type=int),
        OutputArgument(name="registrationDate", description="The registration date of given account.",
                       prefix="account_details", output_type=int),
        OutputArgument(name="activationDate", description="The Activation date of given account.",
                       prefix="account_details", output_type=int),
        OutputArgument(name="expirationDate", description="Account expiration date.",
                       prefix="account_details", output_type=int),
    ],
    description="This command gives all details related to account, we are using this to find assigned simulator quota")
def get_simulator_quota_with_table(client: Client):

    simulator_details = client.get_simulator_quota()
    if simulator_details.status_code == 409:
        return json.dumps(simulator_details.json()), False
    simulator_details = simulator_details.json()

    human_readable = tableToMarkdown(
        name="Account Details",
        t=simulator_details.get("data"),
        headers=["id", "name", "contactName", "contactEmail", "userQuota", "nodesQuota", "registrationDate",
                 "activationDate", "expirationDate"])
    outputs = {
        'account_details': simulator_details.get("data"),
        "simulator_quota": simulator_details.get("data").get("nodesQuota")
    }
    simulator_details = CommandResults(
        outputs_prefix="account_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return simulator_details, True


@metadata_collector.command(
    command_name="safebreach-get-available-simulator-details",
    inputs_list=simulator_details_inputs,
    outputs_prefix="simulator_details",
    outputs_list=simulators_output_fields,
    description="This command gives all details related to account, we are using this to find assigned simulator quota")
def get_all_simulator_details(client: Client):
    return get_simulators_and_display_in_table(client=client, just_name=False)


@metadata_collector.command(
    command_name="safebreach-get-simulator-with-name",
    inputs_list=[
        InputArgument(name="Simulator/Node Name", description="Name of simulator/node to search with.",
                      required=False, is_array=False),
    ],
    outputs_prefix="simulator_details",
    outputs_list=simulators_output_fields,
    description="This command gives simulator with given name")
def get_simulator_with_name(client: Client):
    return get_simulators_and_display_in_table(client=client, just_name=True)


@metadata_collector.command(
    command_name="safebreach-delete-simulator-with-name",
    inputs_list=[
        InputArgument(name="Simulator/Node Name", description="Name of simulator/node to search with.",
                      required=True, is_array=False),
        InputArgument(name="Should Force Delete", description="Name of simulator/node to search with.",
                      default="false", options=["true", "false"], required=True, is_array=False),
    ],
    outputs_prefix="deleted_simulator_details",
    outputs_list=simulators_output_fields,
    description="This command deletes simulator with given name")
def delete_simulator_with_given_name(client: Client):

    deleted_node = client.delete_simulator_with_given_name()
    if deleted_node.status_code == 409:
        return json.dumps(deleted_node.json()), False
    deleted_node = deleted_node.json()

    flattened_nodes, keys = client.flatten_node_details([deleted_node.get("data", {})])
    human_readable = tableToMarkdown(
        name="Deleted Simulators Details",
        t=flattened_nodes,
        headers=keys)
    outputs = [{
        'Deleted simulators Details': deleted_node.get("data", {}),
    }]
    result = CommandResults(
        outputs_prefix="deleted_simulator_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-update-simulator-with-given-name",
    inputs_list=[
        InputArgument(name="Simulator/Node Name", description="Name of simulator/node to search with.",
                      required=True, is_array=False),
    ] + simulator_details_for_update_fields,
    outputs_prefix="updated_simulator_details",
    outputs_list=simulators_output_fields,
    description="This command updates simulator with given name")
def update_simulator_with_given_name(client: Client):

    updated_node = client.update_simulator_with_given_name()
    if updated_node.status_code == 409:
        return json.dumps(updated_node.json()), False
    updated_node = updated_node.json()

    flattened_nodes, keys = client.flatten_node_details([updated_node.get("data", {})])
    human_readable = tableToMarkdown(
        name="Updated Simulators Details",
        t=flattened_nodes,
        headers=keys)
    outputs = updated_node.get("data", {})
    result = CommandResults(
        outputs_prefix="updated_simulator_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-rotate-verification-token",
    inputs_list=None,
    outputs_prefix="new_token",
    outputs_list=simulators_output_fields,
    description="This command gives simulator with given name")
def return_rotated_verification_token(client: Client):
    new_token = client.rotate_verification_token()
    if new_token.status_code == 409:
        return json.dumps(new_token.json()), False
    new_token = new_token.json()
    human_readable = tableToMarkdown(
        name=" new Token Details",
        t=new_token.get("data"),
        headers=["secret"])
    outputs = new_token.get("data", {}).get("secret", "")
    result = CommandResults(
        outputs_prefix="new_token",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


@metadata_collector.command(
    command_name="safebreach-get-test-summary",
    inputs_list=[
        InputArgument(name="Include Archived", description="Should archived tests be included in search.",
                      options=["true", "false"], default="true", required=False, is_array=False),
        InputArgument(name="Entries per Page", description="number of entries per page to be retrieved.",
                      required=False, is_array=False),
        InputArgument(name="Plan ID", description="plan Id of test.", required=False, is_array=False),
        InputArgument(name="Status", description="Status of simulation.", required=False, is_array=False,
                      default="CANCELED", options=["CANCELED", "COMPLETED"]),
        InputArgument(name="Simulation ID", description="Unique ID of the simulation.", required=False, is_array=False),
        InputArgument(name="Sort By", description="sort by option", required=False, is_array=False,
                      options=["endTime", "startTime", "planRunId", "stepRunId"], default="endTime"),
    ],
    outputs_prefix="test_results",
    outputs_list=simulation_output_fields,
    description="This command gets tests with given modifiers")
def get_all_tests_summary(client: Client):
    return get_tests_summary(client=client)


@metadata_collector.command(
    command_name="safebreach-get-test-summary-with-plan-run-id",
    inputs_list=[
        InputArgument(name="Include Archived", description="Should archived tests be included in search.",
                      options=["true", "false"], default="true", required=False, is_array=False),
        InputArgument(name="Entries per Page", description="number of entries per page to be retrieved.",
                      required=False, is_array=False),
        InputArgument(name="Plan ID", description="plan Id of test.", required=True, is_array=False),
        InputArgument(name="Status", description="Status of simulation.", required=False, is_array=False,
                      options=["CANCELED", "COMPLETED"]),
        InputArgument(name="Simulation ID", description="Unique ID of the simulation.", required=False, is_array=False),
        InputArgument(name="Sort By", description="sort by option", required=False, is_array=False,
                      options=["endTime", "startTime", "planRunId", "stepRunId"], default="endTime"),
    ],
    outputs_prefix="test_results",
    outputs_list=simulation_output_fields,
    description="This command gets tests with given plan ID")
def get_all_tests_summary_with_plan_id(client: Client):
    return get_tests_summary(client=client)


@metadata_collector.command(
    command_name="safebreach-delete-test-summary-of-given-test",
    inputs_list=[
        InputArgument(name="Test ID", description="number of entries per page to be retrieved.",
                      required=False, is_array=False),
        InputArgument(name="Soft Delete", description="Should archived tests be included in search.",
                      options=["true", "false"], default="true", required=False, is_array=False),
    ],
    outputs_prefix="deleted_test_results",
    outputs_list=simulation_output_fields,
    description="This command deletes tests with given plan ID")
def delete_test_result_of_test(client: Client):
    test_summaries = client.delete_test_result_of_test()
    if test_summaries.status_code == 409:
        return json.dumps(test_summaries.json()), False
    test_summaries = test_summaries.json()
    human_readable = tableToMarkdown(
        name="Deleted Test",
        t=test_summaries.get("data", {}),
        headers=["id"])
    outputs = [test_summaries.get("data", {}).get("id")]

    result = CommandResults(
        outputs_prefix="deleted_test_results",
        outputs=outputs,
        readable_output=human_readable
    )
    return result, True


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
            result, status = get_user_id_by_name_or_email(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-create-user":
            user, status = create_user(client=client)
            return_results(user) if status else return_error(user)

        elif demisto.command() == "safebreach-delete-user":
            user, status = delete_user_with_details(client=client)
            return_results(user) if status else return_error(user)

        elif demisto.command() == 'safebreach-update-user-details':
            user, status = update_user_with_details(client=client)
            return_results(user) if status else return_error(user)

        elif demisto.command() == 'safebreach-create-deployment':
            deployment, status = create_deployment(client=client)
            return_results(deployment) if status else return_error(deployment)

        elif demisto.command() == 'safebreach-update-deployment':
            deployment, status = update_deployment(client=client)
            return_results(deployment) if status else return_error(deployment)

        elif demisto.command() == "safebreach-delete-deployment":
            deployment, status = delete_deployment(client=client)
            return_results(deployment) if status else return_error(deployment)

        elif demisto.command() == "safebreach-generate-api-key":
            result, status = create_api_key(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-api-key":
            result, status = delete_api_key(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-integration-errors":
            result, status = get_all_error_logs(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-integration-errors":
            result, status = delete_integration_error_logs(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-available-simulator-count":
            result, status = get_simulator_quota_with_table(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-available-simulator-details":
            result, status = get_all_simulator_details(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-simulator-with-name":
            result, status = get_simulator_with_name(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-simulator-with-name":
            result, status = delete_simulator_with_given_name(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-update-simulator-with-given-name":
            result, status = update_simulator_with_given_name(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-rotate-verification-token":
            result, status = return_rotated_verification_token(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-test-summary":
            result, status = get_all_tests_summary(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-get-test-summary-with-plan-run-id":
            result, status = get_all_tests_summary_with_plan_id(client=client)
            return_results(result) if status else return_error(result)

        elif demisto.command() == "safebreach-delete-test-summary-of-given-test":
            result, status = delete_test_result_of_test(client=client)
            return_results(result) if status else return_error(result)

    # Log exceptions and return errors
    except Exception as e:
        demisto.error(traceback.format_exc())
        return_error(f'Failed to execute {demisto.command()} command {traceback.format_exc()}.\nError:\n{str(e)}')


''' ENTRY POINT '''

if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
