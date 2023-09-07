import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

simulator_details_inputs = [
    InputArgument(name="details", description="if details are to be included for search.", options=["true", "false"],
                  default="true", required=True, is_array=False),
    InputArgument(name="deleted", description="if deleted are to be included for search.", options=["true", "false"],
                  default="true", required=True, is_array=False),
    InputArgument(name="secret", description="if secrets are to be included for search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="shouldIncludeProxies", description="if proxies are to be included for search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="hostname", description="if hostname to be included for search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="connectionType", description="if connectionType to be included for search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="externalIp", description="if external IP details to be included for search.",
                  required=False, is_array=False),
    InputArgument(name="internalIp", description="if Internal IP are to be included for search.",
                  required=False, is_array=False),
    InputArgument(name="os", description="if Operating system details to be included for search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="sortDirection", description="direction in which secrets are to be sorted.", options=["asc", "desc"],
                  default="asc", required=False, is_array=False),
    InputArgument(name="startRow", description="if there are too many entries then where should we start looking from.",
                  required=False, is_array=False),
    InputArgument(name="pageSize", description="number of entries to search.", required=False, is_array=False),
    InputArgument(name="isEnabled", description="if to search only enabled ones.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="isConnected", description="status of connection of nodes to search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="isCritical", description="whether to search only for critical nodes or not.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="assets", description="Whether search only for assets and which assets.", required=False, is_array=False),
    InputArgument(name="additionalDetails", description="Whether to show additional details or not.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="impersonatedUsers", description="should search only for impersonated user targets or not.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="isAzureAttacker", description="Whether to search only for azure attackers.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="isAwsAttacker", description="Whether to search only for aws attacker.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="isPreExecutor", description="should search only for pre-executors or not.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="isInfiltrationTarget", description="Whether to search only for infiltration targets.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="isMailTarget", description="Whether to search only for Mail targets.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="isExfiltrationTarget", description="should search only for exfiltration targets or not.",
                  options=["true", "false"], required=False, is_array=False),

    # These fields need to be '|' separated  arrays
    InputArgument(name="deployments", description="deployments list which the search should look.",
                  required=False, is_array=True),
    InputArgument(name="advancedActions", description="advanced actions to search.",
                  required=False, is_array=True),
    InputArgument(name="roles", description="roles to search.",
                  required=False, is_array=True),
    InputArgument(name="userids", description="userids to search.",
                  required=False, is_array=True),
    InputArgument(name="versions", description="versions to filter by.",
                  required=False, is_array=True),
    # '|' separated arrays end

    # normal arrays start
    InputArgument(name="proxyIds", description="proxy ids to search.",
                  required=False, is_array=True),
    InputArgument(name="assetIds", description="asset ids to search.",
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
    OutputArgument(name="name", description="name for given simulator.",
                   output_type=str),
    OutputArgument(name="account_id", description="Account Id of account Hosting given simulator.",
                   output_type=str),
    OutputArgument(name="is_critical", description="Whether the simulator is critical.",
                   output_type=str),
    OutputArgument(name="is_exfiltration", description="If Simulator is exfiltration target.",
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
    OutputArgument(name="is_azure_attacker", description="If the given simulator is azure attacker.",
                   output_type=str),
    OutputArgument(name="external_ip", description="external ip of given simulator.",
                   output_type=str),
    OutputArgument(name="internal_ip", description="internal ip of given simulator.",
                   output_type=str),
    OutputArgument(name="is_web_application_attacker", description="Whether the simulator is Web application attacker.",
                   output_type=str),
    OutputArgument(name="preferred_interface", description="Preferred simulator interface.",
                   output_type=int),
    OutputArgument(name="preferred_ip", description="Preferred Ip of simulator.",
                   output_type=int),
    OutputArgument(name="hostname", description="Hostname of given simulator.",
                   output_type=str),
    OutputArgument(name="connection_type", description="connection_type of given simulator.",
                   output_type=str),
    OutputArgument(name="simulator_status", description="status of the simulator.",
                   output_type=str),
    OutputArgument(name="connection_status", description="connection status of node/simulator.",
                   output_type=int),
    OutputArgument(name="simulator_framework_version", description="Framework version of simulator.",
                   output_type=int),
    OutputArgument(name="operating_system_type", description="operating system type of given simulator.",
                   output_type=str),
    OutputArgument(name="operating_system", description="Operating system of given simulator.",
                   output_type=str),
    OutputArgument(name="execution_hostname", description="Execution Hostname of the given node.",
                   output_type=str),
    OutputArgument(name="deployments", description="deployments simulator is part of.",
                   output_type=int),
    OutputArgument(name="created_at", description="Creation datetime of simulator.",
                   output_type=int),
    OutputArgument(name="updated_at", description="Update datetime of given simulator.",
                   output_type=str),
    OutputArgument(name="deleted_at", description="deletion datetime of given simulator.",
                   output_type=str),
    OutputArgument(name="assets", description="Assets of given simulator.",
                   output_type=str),
    OutputArgument(name="simulation_users", description="simulator users list.",
                   output_type=int),
    OutputArgument(name="proxies", description="Proxies of simulator.",
                   output_type=int),
    OutputArgument(name="advanced_actions", description="Advanced simulator details.",
                   output_type=int)
]

simulator_details_for_update_fields = [
    InputArgument(name="isEnabled", description="set true to enable the node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isProxySupported", description="set true to enable the proxy support.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isCritical", description="set true to make node as critical node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isExfiltration", description="set true to make the node as exfiltration node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isInfiltration", description="set true to make the node as infiltration node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isMailTarget", description="set true to make node as mail target.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isMailAttacker", description="set true to make node as MailAttacker node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isPreExecutor", description="set true to enable the node as PreExecutor node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isAWSAttacker", description="set true to make node as AWS attacker target.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isAzureAttacker", description="set true to make node as Azure attacker node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="isWebApplicationAttacker", description="set true to enable the node as web application attacker node.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="useSystemUser", description="set true to enable the node get system user access.",
                  options=["false", "true"], required=False, is_array=False),
    InputArgument(name="connectionUrl", description="the given value will be set as connection string.",
                  required=False, is_array=False),
    InputArgument(name="cloudProxyUrl", description="the given value will be set as cloud proxy url.",
                  required=False, is_array=False),
    InputArgument(name="name", description="the given value will be set as name of simulator.",
                  required=False, is_array=False),
    InputArgument(name="preferredInterface", description="the given value will be set as preferred interface string.",
                  required=False, is_array=False),
    InputArgument(name="preferredIp", description="the given value will be set as Preferred IP.",
                  required=False, is_array=False),
    InputArgument(name="tunnel", description="the given value will be set as tunnel.",
                  required=False, is_array=False),
]

simulation_output_fields = [
    OutputArgument(name="planId", description="Plan ID of the simulation.", output_type=str),
    OutputArgument(name="planName", description="Plan Name of the simulation.", output_type=str),
    OutputArgument(name="securityActionPerControl", description="Security Actions of the simulation.", output_type=str),
    OutputArgument(name="planRunId", description="Plan Run ID of the simulation.", output_type=str),
    OutputArgument(name="runId", description="Run ID of the simulation.", output_type=str),
    OutputArgument(name="status", description="status of the simulation.", output_type=str),
    OutputArgument(name="plannedSimulationsAmount", description="Planned simulations amount of the simulation.", output_type=str),
    OutputArgument(name="simulatorExecutions", description="simulator executions of the simulation.", output_type=str),
    OutputArgument(name="ranBy", description="user who started the simulation.", output_type=str),
    OutputArgument(name="simulatorCount", description="simulators count of simulation.", output_type=str),
    OutputArgument(name="endTime", description="End Time of the simulation.", output_type=str),
    OutputArgument(name="startTime", description="start time of the simulation.", output_type=str),
    OutputArgument(name="finalStatus.stopped", description="stopped count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.missed", description="missed count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.logged", description="logged count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.detected", description="detected count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.prevented", description="prevented count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.inconsistent", description="inconsistent count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.drifted", description="drifted count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.not_drifted", description="not drifted count of simulation.", output_type=str),
    OutputArgument(name="finalStatus.baseline", description="baseline count of simulation.", output_type=str),
]

metadata_collector = YMLMetadataCollector(
    integration_name="Safebreach Content Management",
    description="This Integration aims to provide easy access to safebreach from XSOAR.\
        Following are the things that user can get access through XSOAR command integration: \
        1. User get, create, update and delete. \
        2. Deployment create, update and delete. \
        3. Tests get and delete. \
        4. Nodes get, update, delete. ",
    display="Safebreach Content Management",
    category="Deception & Breach Simulation",
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


def format_sb_code_error(errors_data):
    """This function gets all errors for when we get a 400 status and
       formats the errors accordingly

    Args:
        errors_data (dict): This is all errors with sbcodes returned by safebreach API

    Returns:
        (str,optional): returns error codes which are formatted as string
    """

    error_data = ""
    sbcode_error_dict = {
        700: f"{error_data} value is below permitted minimum",
        701: f"{error_data} value is above permitted maximum",
        702: f"{error_data} length is more than permitted length",
        703: f"{error_data} field is expected to be integer but received something else",
        704: f"{error_data} field cant be empty",
        705: f"{error_data} field cant permit this value",
        706: f"{error_data} field value is supposed to be unique, value is already taken",
        707: f"{error_data} requested value not found",
        708: f"{error_data} expected UUID but found something else",
        709: f"{error_data} cannot be null",
        710: f"{error_data} is not a valid URL",
        711: f"{error_data} field should not be changed but has been changed",
        712: "license is invalid",
        713: f"{error_data} fields have opposite Attributes",
        714: f"{error_data} fields block association with each other",
        715: "weak password is set",
        716: "account name and account number dont match",
        718: "license expired",
        719: "Connection Refused",
        720: "passwords dont match",
        721: "gateway timeout"
    }
    errors = errors_data.get("errors")
    final_error_string = ""
    # here we are formatting errors and then we are making them as a string
    for error in errors:
        error_data = error.get("data")
        error_code = error.get("sbcode")
        final_error_string = final_error_string + " " + sbcode_error_dict[int(error_code)]
    return final_error_string


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
        """_summary_

        Args:
            url (str, optional): endpoint url which follows base URL will be this input . Defaults to "".
            method (str, optional): HTTP method to be used, Defaults to "GET".
            request_params (dict, optional): request parameters if any. Defaults to {}.
            body (dict, optional): request body for API call. Defaults to None.

        Returns:
            (dict,list,Exception): a dictionary or list with data based on API call OR Throws an error based on status code
        """
        base_url = demisto.params().get("base_url", "")
        base_url = base_url if base_url[-1] != "/" else base_url[0:-1]
        url = url if url[0] != "/" else url[1:]
        request_url = f"{base_url}/api/{url}"
        api_key = demisto.params().get("api_key")
        headers = {
            'Accept': 'application/json',
            'x-apitoken': api_key
        }

        response = self._http_request(method=method, full_url=request_url, json_data=body, headers=headers,
                                      params=request_params, ok_codes=[200, 201, 204, 400])
        return response if not response.get("error") else self.handle_sbcodes(response)

    def handle_sbcodes(self, response: dict):
        """This function handles errors related to SBcodes if the endpoint gives sbcode in errors

        Args:
            response (dict): all errors given by 400 response code will be accepted as dictionary and are formatted based on 
            the state of error

        Raises:
            Exception: all errors will be formatted and then thrown as exception string which will show as error_results in XSOAR
        """
        exception_string = format_sb_code_error(response.get("error"))
        raise Exception(exception_string)

    def get_all_users_for_test(self):
        """This function is being used for testing connection with safebreach 
        after API credentials re taken from user when creating instance

        Returns:
            str: This is just status string, if "ok" then it will show test as success else it throws error
        """
        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/users"
        response = self.get_response(url=url)
        if response:
            return "ok"
        return "Could not verify the connection"

    def get_simulator_quota(self):
        """This function calls Account details end point which will return account details
        which has nodesQuota

        Returns:
            dict: user details related to the queried account
        """
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}"
        simulator_details = self.get_response(method=method, url=url)
        return simulator_details

    def get_simulators_details(self, request_params):
        """This function queries for simulators along with modifiers which are request_params
        based on that we get simulator related details and this raises an exception if 
        no simulator with given details are found

        Args:
            request_params (dict): filters when querying the data related to nodes/simulators

        Raises:
            Exception: Raised when no entries are found related to given filters

        Returns:
            list(dict): returns simulator related data which fulfils the given input parameters
        """
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}/nodes/bulk"

        simulators_details = self.get_response(method=method, url=url, request_params=request_params)
        if not simulators_details.get("data", {}).get("count"):
            raise Exception(f"No Matching simulators found with details not found details are {request_params}")
        return simulators_details

    def create_simulator_params(self):
        """This function creates parameters related to simulator as a dictionary

        Returns:
            dict: parameters dictionary
        """
        possible_inputs = [
            "details", "deleted", "secret", "shouldIncludeProxies", "hostname", "connectionType", "externalIp", "internalIp",
            "os", "status", "sortDirection", "startRow", "pageSize", "isEnabled", "isConnected", "isCritical",
            "isExfiltrationTarget", "isInfiltrationTarget", "isMailTarget", "isMailAttacker", "isPreExecutor",
            "isAwsAttacker", "isAzureAttacker", "impersonatedUsers", "assets", "advancedActions", "deployments",
            "additionalDetails"]
        request_params = {}
        for parameter in possible_inputs:
            if demisto.args().get(parameter):
                request_params[parameter] = demisto.args().get(parameter)
        return request_params

    def flatten_node_details(self, nodes):
        """this function will flatten the nested simulator data 
        into a flatter structure for table display

        Args:
            nodes List(dict): This is list of nodes which are to be flattened

        Returns:
            List(dict): This is list of nodes related data for table which is flattened 
            List : This is list of keys which are present in the dict
        """
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
        """This will return parameters for getting simulators data

        Returns:
            dict: dict of request parameters
        """
        name = demisto.args().get("Simulator/Node Name")
        request_params = {
            "name": name,
            "deleted": demisto.args().get("deleted", "false"),
            "details": demisto.args().get("details", "false")
        }
        return request_params

    def get_simulator_with_a_name_return_id(self):
        """This function returns id of a given simulator when a name is given as input

        Raises:
            Exception: This is thrown when no simulator with given name is found

        Returns:
            int: Simulator ID with given name
        """
        request_params = self.get_simulator_with_name_request_params()
        result = self.get_simulators_details(request_params=request_params)
        try:
            simulator_id = result.get("data", {}).get("rows", {})[0].get("id")
            return simulator_id
        except IndexError:
            raise Exception("Simulator with given details could not be found")

    def delete_node_with_given_id(self, node_id, force: str):
        """This function calls delete simulator on simulator with given ID

        Args:
            node_id (str): This is node ID to delete
            force (str): If the node is to be force deleted even if its not connected 

        Returns:
            dict: Deleted node data
        """
        request_params = {
            "force": force
        }
        method = "DELETE"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{node_id}"

        deleted_node = self.get_response(url=request_url, method=method, request_params=request_params)
        return deleted_node

    def delete_simulator_with_given_name(self):
        """This function deletes a node with given name,
        This achieves this by retrieving ID by querying all nodes
        and then retrieving ID of name if it matches. 
        Then it calls a function which makes API call with this ID

        Returns:
            dict: deleted node related data
        """
        simulator_id = self.get_simulator_with_a_name_return_id()
        force_delete = demisto.args().get("Should Force Delete")
        result = self.delete_node_with_given_id(node_id=simulator_id, force=force_delete)
        return result

    def make_update_node_payload(self):
        # this is created under assumption that only these fields will be  chosen to be updated by user
        """This function returns a payload with update related data

        Returns:
            dict: Update Node payload
        """
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
        """This function calls update node details API and returns updated datas

        Args:
            node_id (str): ID of node to update
            node_data (dict): Payload for PUT call

        Returns:
            dict: Updated node details
        """
        method = "PUT"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{node_id}"

        updated_node = self.get_response(url=request_url, method=method, body=node_data)
        return updated_node

    def update_simulator_with_given_name(self):
        """This function updates simulator with given name

        Returns:
            dict: this is updated node details for given node ID
        """
        simulator_id = self.get_simulator_with_a_name_return_id()
        payload = self.make_update_node_payload()
        updated_node = self.update_node(node_id=simulator_id, node_data=payload)
        return updated_node


def get_simulators_and_display_in_table(client: Client, just_name=False):
    """This function gets all simulators and displays in table

    Args:
        client (Client): Client class for API calls
        just_name (bool, optional): This will be used to know whether to search and return all 
        simulators or only one. Defaults to False.

    Returns:
        CommandResults : table showing simulator details
        dict: simulator details
    """
    request_params = client.get_simulator_with_name_request_params() if just_name \
        else client.create_simulator_params()
    result = client.get_simulators_details(request_params=request_params)
    flattened_nodes, keys = client.flatten_node_details(result.get("data", {}).get("rows", {}))
    human_readable = tableToMarkdown(
        name="Simulators Details",
        t=flattened_nodes,
        headers=keys)
    outputs = result.get("data", {}).get("rows")
    outputs = outputs[0] if just_name else outputs
    result = CommandResults(
        outputs_prefix="simulator_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


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
    description="This command gives all details related to account, we are using this to find assigned simulator quota.")
def get_simulator_quota_with_table(client: Client):
    """This will be used to show account simulator quota and details in table

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: this shows a table with account details and a dict with account details
    """
    simulator_details = client.get_simulator_quota()

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
    return simulator_details


@metadata_collector.command(
    command_name="safebreach-get-available-simulator-details",
    inputs_list=simulator_details_inputs,
    outputs_prefix="simulator_details",
    outputs_list=simulators_output_fields,
    description="We are using this command to get all available simulators.")
def get_all_simulator_details(client: Client):
    """This function returns simulator details of all simulators

    Args:
        client (Client): Client class for API calls

    Returns:
        List(dict): This is list of all simulators data
    """
    return get_simulators_and_display_in_table(client=client, just_name=False)


@metadata_collector.command(
    command_name="safebreach-get-simulator-with-name",
    inputs_list=[
        InputArgument(name="Simulator/Node Name", description="Name of simulator/node to search with.",
                      required=False, is_array=False),
        InputArgument(name="details", description="if details are to be included for search.", options=["true", "false"],
                      default="true", required=True, is_array=False),
        InputArgument(name="deleted", description="if deleted are to be included for search.", options=["true", "false"],
                      default="true", required=True, is_array=False),
    ],
    outputs_prefix="simulator_details",
    outputs_list=simulators_output_fields,
    description="This command gives simulator with given name")
def get_simulator_with_name(client: Client):
    """this function returns simulator with given name as  table and dict

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,data: This is data of simulator with given name
    """
    return get_simulators_and_display_in_table(client=client, just_name=True)


@metadata_collector.command(
    command_name="safebreach-delete-simulator-with-name",
    inputs_list=[
        InputArgument(name="Simulator/Node Name", description="Name of simulator/node to search with.",
                      required=True, is_array=False),
        InputArgument(name="Should Force Delete", description="Should we force delete the simulator.",
                      default="false", options=["true", "false"], required=True, is_array=False),
        InputArgument(name="details", description="if details are to be included for search.", options=["true", "false"],
                      default="true", required=False, is_array=False),
        InputArgument(name="deleted", description="if deleted are to be included for search.", options=["true", "false"],
                      default="true", required=False, is_array=False),
    ],
    outputs_prefix="deleted_simulator_details",
    outputs_list=simulators_output_fields,
    description="This command deletes simulator with given name.")
def delete_simulator_with_given_name(client: Client):
    """This function deletes simulator with given name

    Args:
        client (Client): This is client class for API calls

    Returns:
        CommandResults,Dict: this is for table showing deleted simulator data and dict with data
    """
    deleted_node = client.delete_simulator_with_given_name()

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
    return result


@metadata_collector.command(
    command_name="safebreach-update-simulator-with-given-name",
    inputs_list=[
        InputArgument(name="Simulator/Node Name", description="Name of simulator/node to search with.",
                      required=True, is_array=False),
        InputArgument(name="details", description="if details are to be included for search.", options=["true", "false"],
                      default="true", required=False, is_array=False),
        InputArgument(name="deleted", description="if deleted are to be included for search.", options=["true", "false"],
                      default="true", required=False, is_array=False),
    ] + simulator_details_for_update_fields,
    outputs_prefix="updated_simulator_details",
    outputs_list=simulators_output_fields,
    description="This command updates simulator with given name with given details.")
def update_simulator_with_given_name(client: Client):
    """This function updates simulator with given data having name as given input

    Args:
        client (Client): This is client class for API calls

    Returns:
        CommandResults,Dict: This will return table and dict containing updated simulator data
    """
    updated_node = client.update_simulator_with_given_name()

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
    return result


def main() -> None:
    """
    Execution starts here
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
            result = client.get_all_users_for_test()
            return_results(result)

        elif demisto.command() == "safebreach-get-available-simulator-count":
            result = get_simulator_quota_with_table(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-available-simulator-details":
            result = get_all_simulator_details(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-simulator-with-name":
            result = get_simulator_with_name(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-simulator-with-name":
            result = delete_simulator_with_given_name(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-update-simulator-with-given-name":
            result = update_simulator_with_given_name(client=client)
            return_results(result)

    except Exception as e:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
