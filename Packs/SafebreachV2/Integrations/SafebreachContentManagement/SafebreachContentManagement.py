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

tests_output_fields = [
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
    docker_image="demisto/python3:3.10.13.73190",
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


class NotFoundError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


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
        return response if not ((type(response) == dict) and (response.get("error") and not response.get("errorCode")))\
            else self.handle_sbcodes(response)

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

    def get_users_list(self):
        """This function returns all users present based on modifiers

        Returns:
            list: this is list of users queried based on modifiers specified
        """
        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/users"
        params = {
            "details": demisto.args().get("Should Include Details", "true"),
            "deleted": demisto.args().get("Should Include Deleted", "true")
        }
        response = self.get_response(url=url, request_params=params)
        user_data = response['data']
        return user_data

    def delete_user(self):
        """This function deletes a given user based on arguments of commands

        Returns:
            dict: user data related to the user who has been deleted
        """
        user_id = demisto.args().get("User ID")
        user_email = demisto.args().get("Email")
        # we are prioritizing email or ID when both are given by user
        if user_email and not user_id:
            # retrieve all users and filter with given details
            user_list = self.get_users_list()
            demisto.info("retrieved user list which contains all available users in safebreach")
            user = list(filter(lambda user_data: user_data["email"] == user_email, user_list))
            if user:
                user_id = int(user[0]["id"])
                demisto.info("user has been found and details are being given for deleting user")
        # since we have user ID we can delete the user
        account_id = demisto.params().get("account_id", 0)
        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/users/{user_id}"

        deleted_user = self.get_response(url=url, method=method)
        return deleted_user

    def update_user_with_details(self, user_id: str, user_details: dict):
        """This function updates user with given details

        Args:
            user_id (str): this is ID of user to update
            user_details (dict): this is list of user details to update

        Returns:
            dict: user data post update
        """
        # we dont want to update details as empty if user is not giving data in inputs , hence remove false values
        for key in list(user_details.keys()):
            if not user_details[key]:
                user_details.pop(key)

        account_id = demisto.params().get("account_id", 0)
        method = "PUT"
        url = f"/config/v1/accounts/{account_id}/users/{int(user_id)}"

        updated_user = self.get_response(url=url, method=method, body=user_details)
        return updated_user

    def list_deployments(self):
        """This function lists all deployments we extracted from safebreach

        Returns:
            list: List of deployments data retrieved
        """
        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/deployments"

        response = self.get_response(url=url)
        deployments = response['data']
        return deployments

    def get_deployment_id_by_name(self, deployment_name: str) -> dict:
        """This function gets deployment with given name

        Args:
            deployment_name (str): name of the given deployment

        Raises:
            Exception: If no deployment with given name is found then this exception is raised

        Returns:
            dict: deployment related details found while we find deployment with given name
        """
        available_deployments = self.list_deployments()
        needed_deployments = list(filter(lambda deployment: deployment["name"] == deployment_name, available_deployments))
        if needed_deployments:
            return needed_deployments[0]
        raise Exception("related deployment with given name couldn't be found")

    def create_deployment_data(self):
        """This function creates a deployment based on data given by user, this will be called by an external function
        which is triggered with a command for creating deployment

        Returns:
            dict: the data of deployment created
        """
        account_id = demisto.params().get("account_id", 0)
        name = demisto.args().get("Name")
        description = demisto.args().get("Description")
        nodes = demisto.args().get("Nodes", "").replace('"', "").split(",")
        deployment_payload = {
            "nodes": nodes,
            "name": name,
            "description": description,
        }

        method = "POST"
        url = f"/config/v1/accounts/{account_id}/deployments"
        created_deployment = self.get_response(url=url, method=method, body=deployment_payload)
        return created_deployment

    def update_deployment(self):
        """This function is called when we want to update a deployment data

        Raises:
            Exception: This will raise an exception if a deployment with given name or id couldn't be found 

        Returns:
            dict: updated deployment data
        """

        account_id = demisto.params().get("account_id", 0)
        deployment_id = demisto.args().get("Deployment ID", None)
        deployment_name = demisto.args().get("Deployment Name")

        if deployment_name and not deployment_id:
            needed_deployment = self.get_deployment_id_by_name(deployment_name)
            if needed_deployment:
                deployment_id = needed_deployment['name']
        if not deployment_id:
            raise Exception(f"Could not find Deployment with details Name:\
                {deployment_name} and Deployment ID : {deployment_id}")

        name = demisto.args().get("Updated Deployment Name")
        nodes = demisto.args().get("Updated Nodes for Deployment", None)
        description = demisto.args().get("Updated deployment description")
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
        """This function deletes a deployment with given id or name

        Raises:
            Exception: raised when a deployment with given name or id could not be found

        Returns:
            dict: deleted deployment data
        """
        account_id = demisto.params().get("account_id", 0)
        deployment_id = demisto.args().get("Deployment ID", None)
        deployment_name = demisto.args().get("Deployment Name")

        if deployment_name and not deployment_id:
            needed_deployment = self.get_deployment_id_by_name(deployment_name)
            if needed_deployment:
                deployment_id = needed_deployment['name']
        if not deployment_id:
            raise Exception(f"Could not find Deployment with details Name:\
                {deployment_name} and Deployment ID : {deployment_id}")
        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/deployments/{deployment_id}"
        deleted_deployment = self.get_response(url=url, method=method)
        return deleted_deployment

    def get_tests_with_args(self):
        """This function calls GET of testsummaries endpoint and returns data related to test
        The parameters are all optional

        parameters include:
        1. including archived, this will retrieve archived test summaries too
        2. size, Number of tests to retrieve
        3. status, status of test - CANCELED,COMPLETED
        4. plan_id : Plan id of test -  this is not plan run id
        5. simulator_id : this is simulator ID 
        6. sort by: default its sorted by endDate but can be altered with respect to given enum

        Returns:
            List[Dict]: Returns test data as a list of dictionaries
        """
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
        """This function flattens the test summaries related data for table view

        Args:
            test_summaries (dict): This returns a lit of dictionaries of test summaries 
            which are flattened versions of data retrieved for tests
        """
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
        """This function deletes test results of a given test ID by calling related endpoint

        Returns:
            dict: Deleted test data results
        """
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
        """This function flattens error logs into a single leveled dictionary for table view

        Args:
            error_logs (dict): This is list of dictionaries which have multiple levels of data

        Returns:
            dict : flattened error logs which are easier to display on table
        """
        flattened_logs_list = []
        for connector in error_logs:
            logs = error_logs[connector]["logs"] if error_logs[connector].get("status") == "error" else []
            if logs:
                for log in logs:
                    log["connector"] = connector
                    flattened_logs_list.append(log)
        return flattened_logs_list

    def get_all_error_logs(self):
        """This function retrieves all error logs of a given account

        Returns:
            dict: This will be having dict containing results and status
        """
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/siem/v1/accounts/{account_id}/config/providers/status"

        error_logs = self.get_response(url=url, method=method)
        return error_logs

    def delete_integration_error_logs(self):
        """This function accepts connector ID related to a connector and then returns a status

        Returns:
            dict: status stating whether its success and how many errors are remaining incase of failure to delete some
        """
        account_id = demisto.params().get("account_id", 0)
        connector_id = demisto.args().get("Connector ID")

        method = "DELETE"
        url = f"/siem/v1/accounts/{account_id}/config/providers/status/delete/{connector_id}"

        error_logs = self.get_response(url=url, method=method)
        return error_logs

    def generate_api_key(self):
        """This function calls generate API key endpoint

        Returns:
            dict: response of generate API key API call which contains generated \
                API key and name along with additional details
        """
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
        """This function retrieves all available API keys

        Returns:
            dict: This function retrieves API keys which are active for the given account
        """
        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"config/v1/accounts/{account_id}/apikeys"
        request_params = {
            "details": "true"
        }
        keys_data = self.get_response(url=url, method=method, request_params=request_params)
        return keys_data

    def filter_api_key_with_key_name(self, key_name):
        """This function retrieves all active keys and then filters key based on given input name

        Args:
            key_name (str): The API key name for searching API key

        Raises:
            Exception: if it couldn't find API key with given name

        Returns:
            _type_: key ID for API key
        """
        active_keys = self.get_all_active_api_keys_with_details()
        required_key_object = list(filter(lambda key_obj: key_obj["name"] == key_name, active_keys.get("data")))
        if not required_key_object:
            raise Exception(f"couldn't find APi key with given name: {key_name}")
        return required_key_object[0]["id"]

    def delete_api_key(self):
        """This function calls API key delete endpoint

        Returns:
            dict: Deleted API key data
        """
        key_name = demisto.args().get("Key Name")
        key_id = self.filter_api_key_with_key_name(key_name=key_name)
        account_id = demisto.params().get("account_id", 0)
        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/apikeys/{key_id}"
        deleted_api_key = self.get_response(method=method, url=url)
        return deleted_api_key

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

    def rotate_verification_token(self):
        """This function rotates a verification token thus generating a new token

        Returns:
            dict: dict containing a new token
        """
        method = "POST"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/secret/rotate"

        new_token = self.get_response(url=request_url, method=method, body={})
        return new_token

    def create_user_data(self):
        """This function takes user inputs and then formats it and 
        then calls create user endpoint.

        Returns:
            dict: created user data
        """
        account_id = demisto.params().get("account_id", 0)
        name = demisto.args().get("Name")
        email = demisto.args().get("Email")
        is_active = demisto.args().get("Is Active", False)
        send_email_post_creation = demisto.args().get("Email Post Creation", False)
        password = demisto.args().get("Password")
        admin_name = demisto.args().get("Admin Name", "")
        change_password = demisto.args().get("Change Password on create", False)
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
        """This function takes user inputs and then formats it and 
        then makes a call to function that handles updating user.

        Returns:
            dict: updated user data
        """

        user_id = demisto.args().get("User ID")
        user_email = demisto.args().get("Email")

        name = demisto.args().get("Name")
        is_active = demisto.args().get("Is Active", False)
        description = demisto.args().get("User Description", "")
        role = demisto.args().get("User role")
        password = demisto.args().get("Password")
        deployment_list = demisto.args().get("Deployments", [])
        deployment_list = list(deployment_list) if deployment_list else []
        # formatting the update user payload, we remove false values after passing to function which calls endpoint
        details = {
            "name": name,
            "is_active": is_active,
            "deployments": deployment_list,
            "description": description,
            "role": role,
            "password": password
        }
        # retrieve user based on email and user_id whichever is present
        if user_email and not user_id:
            user_list = self.get_users_list()
            demisto.info("retrieved user list which contains all available users in safebreach")
            user = list(filter(lambda user_data: user_data.get("email") == user_email, user_list))
            if not user:
                raise NotFoundError(f"User with {user_id} or {user_email} not found")
            user_id = user[0]["id"]
            demisto.info("user has been found and details are being given for updating user")
        user = self.update_user_with_details(user_id, details)
        return user


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


def get_tests_summary(client: Client):
    """This function retrieves tests and then flattens them and shows them in  a table

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: This returns a table view of data and a dictionary as output
    """
    test_summaries = client.get_tests_with_args()
    client.flatten_test_summaries(test_summaries)
    human_readable = tableToMarkdown(
        name="Test Results",
        t=test_summaries,
        headers=['planId', "planName", 'securityActionPerControl', 'planRunId', "runId", "status",
                 "plannedSimulationsAmount", "simulatorExecutions", "ranBy", "simulatorCount", "endTime", "startTime",
                 "finalStatus", "stopped", "missed", "logged", "detected", "prevented",
                 "inconsistent", "drifted", "not_drifted", "baseline"])
    outputs = {
        'tests_data': test_summaries
    }

    result = CommandResults(
        outputs_prefix="tests_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-all-users",
    inputs_list=[
        InputArgument(name="Should Include Details", description="If Details of user are to be included while querying all \
            users.", default="true", options=["true", "false"], required=False, is_array=False),
        InputArgument(name="Should Include Deleted", description="If deleted users are to be included while querying all users.",
                      default="true", options=["true", "false"], required=True, is_array=False),
    ],
    outputs_prefix="user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User retrieved.",
                       prefix="user_data", output_type=int),
        OutputArgument(name="name", description="The name of User retrieved.",
                       prefix="user_data", output_type=str),
        OutputArgument(name="email", description="The email of User retrieved.",
                       prefix="user_data", output_type=str),
    ],
    description="This command gives all users depending on inputs given.")
def get_all_users(client: Client):
    """This function is executed when 'safebreach-get-all-users' command is executed

    Args:
        client (Client): This is client class

    Returns:
        CommandResults,dict: This returns all user data retrieved based on given parameters,
        as a table and as a dictionary
    """
    user_data = client.get_users_list()
    demisto.info(f"users retrieved when executing {demisto.command()} command \n Data: \n{user_data}")

    human_readable = tableToMarkdown(name="user data", t=user_data, headers=['id', 'name', 'email'])
    outputs = user_data
    result = CommandResults(
        outputs_prefix="user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-get-user-with-matching-name-or-email",
    inputs_list=[
        InputArgument(name="name", description="Name of the user to lookup.", required=False, is_array=False),
        InputArgument(name="email", description="Email of the user to lookup.", required=True, is_array=False),
        InputArgument(name="Should Include Details", description="If Details of user are to be included while \
            querying all users.", default="true", options=["true"], required=True, is_array=False),
        InputArgument(name="Should Include Deleted", description="If deleted users are to be included while querying all users.",
                      default="true", options=["true", "false"], required=True, is_array=False),
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
    description="This command gives all users depending on inputs given.")
def get_user_id_by_name_or_email(client: Client):
    """This Command Returns a user or their email by a given name or email.

    Args:
        client (Client): Client class for calling API

    Raises:
        Exception: Raised when no user with given name or email or found

    Returns:
        CommandResults,dict,Exception: We create a table showing all details related to users found and 
        give JSON which has all data related to filtered users if any users match given criterion,
        else we raise an exception which is shown as error_result in XSOAR saying user is not found
    """

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

        return result
    raise NotFoundError(f"user with name {name} or email {email} was not found")


@metadata_collector.command(
    command_name="safebreach-create-user",
    inputs_list=[
        InputArgument(name="Name", description="Name of the user to create.", required=False, is_array=False),
        InputArgument(name="Email", description="Email of the user to Create.", required=True,
                      is_array=False),
        InputArgument(name="Is Active", description="Whether the user is active upon creation.",
                      required=False, is_array=False, options=["true", "false"], default="false"),
        InputArgument(name="Email Post Creation", description="Should Email be sent to user on creation.",
                      required=False, is_array=False, options=["true", "false"], default="false"),
        InputArgument(name="Password", description="Password of user being created.", required=True,
                      is_array=False),
        InputArgument(name="Admin Name", description="Name of the Admin creating user.", required=False,
                      is_array=False),
        InputArgument(name="Change Password on create", description="Should user change password on creation.",
                      required=False, is_array=False, options=["true", "false"], default="false"),
        InputArgument(name="User role", description="Role of the user being Created.", required=False,
                      is_array=False,
                      options=["viewer", "administrator", "contentDeveloper", "operator"], default="viewer"),
        InputArgument(name="Deployments", description="Comma separated ID of all deployments the user should be part of.",
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
    description="This command creates a user with given data.")
def create_user(client: Client):
    """this function is executed when 'safebreach-create-user' is called and this creates a user.
    This function calls another function which handles getting inputs and calling API, 
    This function just handles creating table and returning table and json

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: This will show a dictionary based on user data created
    """
    created_user = client.create_user_data()

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
    return result


@metadata_collector.command(
    command_name="safebreach-update-user-details",
    inputs_list=[
        InputArgument(name="User ID", description="user ID of user from safebreach to search.",
                      required=False, is_array=False),
        InputArgument(name="Email", description="Email of the user to Search for updating user details.", required=True,
                      is_array=False),
        InputArgument(name="Name", description="Update the user name to given string.",
                      required=False, is_array=False),
        InputArgument(name="User Description", description="Update the user Description to given string.",
                      required=False, is_array=False),
        InputArgument(name="Is Active", description="Update the user Status.",
                      required=False, is_array=False, options=["true", "false", ""], default=""),
        InputArgument(name="Password", description="Password of user to be updated with.", required=False,
                      is_array=False),
        InputArgument(name="User role", description="Role of the user to be changed to.", required=False,
                      is_array=False,
                      options=["viewer", "administrator", "contentDeveloper", "operator"], default="viewer"),
        InputArgument(name="Deployments", description="Comma separated ID of all deployments the user should be part of.",
                      required=False, is_array=True),
        InputArgument(name="Should Include Details", description="If Details of user are to be included while\
            querying all users.", default="true", options=["true", "false"], required=False, is_array=False),
        InputArgument(name="Should Include Deleted", description="If deleted users are to be included while querying all users.",
                      default="true", options=["true", "false"], required=True, is_array=False)
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
    description="This command updates a user with given data.")
def update_user_with_details(client: Client):
    """This function is executed when 'safebreach-update-user-details' command is being executed.
    This function will call another function which receives inputs from user and creates payload for upload user.

    Args:
        client (Client): Client class for API call

    Returns:
        CommandResults,dict: This function returns updated user in form of table and dictionary
    """
    updated_user = client.update_user_data()

    human_readable = tableToMarkdown(name="Updated User Data", t=updated_user.get("data", {}),
                                     headers=['id', 'name', 'email', "deletedAt", "roles", "description",
                                              "role", "deployments", "createdAt", "updatedAt"])
    outputs = updated_user.get("data", {})

    result = CommandResults(
        outputs_prefix="updated_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-delete-user",
    inputs_list=[
        InputArgument(name="User ID", description="user ID of user from safebreach to search.",
                      required=False, is_array=False),
        InputArgument(name="Email", description="Email of the user to Search for updating user details.", required=True,
                      is_array=False),
        InputArgument(name="Should Include Details", description="If Details of user are to be included while \
            querying all users.", default="true", options=["true", "false"], required=False, is_array=False),
        InputArgument(name="Should Include Deleted", description="If deleted users are to be included while querying all users.",
                      default="true", options=["true", "false"], required=True, is_array=False)
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
    description="This command deletes a user with given data.")
def delete_user_with_details(client: Client):
    """This function deletes user with given details, The inputs are being received in function which this function calls.
    It returns deleted user details

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: This is details of user that has been deleted
    """
    deleted_user = client.delete_user()

    human_readable = tableToMarkdown(name="Deleted User Data", t=deleted_user.get("data", {}),
                                     headers=['id', 'name', 'email', "deletedAt", "roles",
                                              "description", "role", "deployments", "createdAt"])
    outputs = deleted_user.get("data", {})
    result = CommandResults(
        outputs_prefix="deleted_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-create-deployment",
    inputs_list=[
        InputArgument(name="Name", description="Name of the deployment to create.", required=False, is_array=False),
        InputArgument(name="Description", description="Description of the deployment to create.", required=False, is_array=False),
        InputArgument(name="Nodes", description="Comma separated ID of all nodes the deployment should be part of.",
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
    description="This command creates a deployment with given data.")
def create_deployment(client: Client):
    """This function is executed on command "safebreach-create-deployment"

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: Created deployment data as a table and a dictionary
    """
    created_deployment = client.create_deployment_data()

    human_readable = tableToMarkdown(name="Created Deployment", t=created_deployment.get("data", {}),
                                     headers=['id', "accountId", 'name', 'createdAt', "description", "nodes"])
    outputs = created_deployment.get("data", {})

    result = CommandResults(
        outputs_prefix="created_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-update-deployment",
    inputs_list=[
        InputArgument(name="Deployment ID", description="Name of the deployment to update.", required=False, is_array=False),
        InputArgument(name="Deployment Name", description="Description of the deployment to update.",
                      required=False, is_array=False),
        InputArgument(name="Updated Nodes for Deployment", required=False, is_array=False,
                      description="Comma separated ID of all nodes the deployment should be part of."),
        InputArgument(name="Updated Deployment Name", description="Name of the deployment to update to.",
                      required=False, is_array=False),
        InputArgument(name="Updated deployment description.", required=False, is_array=False,
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
    description="This command updates a deployment with given data.")
def update_deployment(client: Client):
    """This function is executed on command "safebreach-update-deployment"

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: updated deployment data as a table and a dictionary
    """
    updated_deployment = client.update_deployment()

    human_readable = tableToMarkdown(name="Updated Deployment", t=updated_deployment.get("data", {}),
                                     headers=['id', "accountId", 'name', 'createdAt',
                                              "description", "nodes", "updatedAt"])
    outputs = updated_deployment.get("data", {})
    result = CommandResults(
        outputs_prefix="updated_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


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
    description="This command deletes a deployment with given data.")
def delete_deployment(client: Client):
    """This function is executed on command "safebreach-delete-deployment"

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: deleted deployment data as a table and a dictionary
    """
    deleted_deployment = client.delete_deployment()

    human_readable = tableToMarkdown(name="Deleted Deployment", t=deleted_deployment.get("data", {}),
                                     headers=['id', "accountId", 'name', 'createdAt',
                                              "description", "nodes", "updatedAt"])
    outputs = deleted_deployment.get("data", {})
    result = CommandResults(
        outputs_prefix="deleted_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


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
    description="This command creates a API Key with given data.")
def create_api_key(client: Client):
    """This function generates API key and returns API key, Executed for command 'safebreach-generate-api-key'

    Args:
        client (Client): Client class for API call

    Returns:
        CommandResults,dict: Command results for generated API key details table and dict containing data
    """
    generated_api_key = client.generate_api_key()

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
    return result


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
    description="This command deletes a API key with given name.")
def delete_api_key(client: Client):
    """This function deletes API key and returns API key, Executed for command 'safebreach-delete-api-key'

    Args:
        client (Client): Client class for API call

    Returns:
        CommandResults,dict: Command results for deleted API key details table and dict containing data
    """
    deleted_api_key = client.delete_api_key()

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
    return result


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
    description="This command gives all connector related errors.")
def get_all_error_logs(client: Client):
    """This function retrieves all error logs and shows them in form of table

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,Dict: This function returns all errors along with connector details in a table and we get data as json
    """
    formatted_error_logs = []
    error_logs = client.get_all_error_logs()

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
        return result
    return formatted_error_logs


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
    description="This command deleted connector related errors.")
def delete_integration_error_logs(client: Client):
    """This function deletes integration errors of a given connector

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,Dict: This returns a table of data showing deleted details and dict showing same in outputs
    """
    error_logs = client.delete_integration_error_logs()

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


@metadata_collector.command(
    command_name="safebreach-rotate-verification-token",
    inputs_list=None,
    outputs_list=[
        OutputArgument(name="new_token", description="new Token.", output_type=str),
    ],
    description="This command rotates generated verification token.")
def return_rotated_verification_token(client: Client):
    """This function is called when rotate-verification-token command is called and will
    help with calling API of rotate verification token
    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,Dict: This returns a table showing new token and a dict as output stating same 
    """
    new_token = client.rotate_verification_token()
    human_readable = tableToMarkdown(
        name=" new Token Details",
        t=new_token.get("data"),
        headers=["secret"])
    outputs = new_token.get("data", {}).get("secret", "")
    result = CommandResults(
        outputs_prefix="secret",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


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
        InputArgument(name="Sort By", description="sort by option.", required=False, is_array=False,
                      options=["endTime", "startTime", "planRunId", "stepRunId"], default="endTime"),
    ],
    outputs_prefix="test_results",
    outputs_list=tests_output_fields,
    description="This command gets tests with given modifiers.")
def get_all_tests_summary(client: Client):
    """This function gets all tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
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
        InputArgument(name="Sort By", description="sort by option.", required=False, is_array=False,
                      options=["endTime", "startTime", "planRunId", "stepRunId"], default="endTime"),
    ],
    outputs_prefix="test_results",
    outputs_list=tests_output_fields,
    description="This command gets tests with given plan ID.")
def get_all_tests_summary_with_plan_id(client: Client):
    """This function takes  a plan run ID and returns test summaries with that plan run ID

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,List(dict): This will return  a table with all details and
        a list of dictionaries with details related to tests with given plan ID
    """
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
    outputs_list=tests_output_fields,
    description="This command deletes tests with given plan ID.")
def delete_test_result_of_test(client: Client):
    """This function deletes test with given Test ID

    Args:
        client (Client): Client class for API call

    Returns:
        CommandResults,Dict: A table showing deletion results and a dict of outputs showing the same
    """
    test_summaries = client.delete_test_result_of_test()

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

        elif demisto.command() == "safebreach-get-all-users":
            users = get_all_users(client=client)
            return_results(users)

        elif demisto.command() == "safebreach-get-user-with-matching-name-or-email":
            result = get_user_id_by_name_or_email(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-create-user":
            user = create_user(client=client)
            return_results(user)

        elif demisto.command() == "safebreach-delete-user":
            user = delete_user_with_details(client=client)
            return_results(user)

        elif demisto.command() == 'safebreach-update-user-details':
            user = update_user_with_details(client=client)
            return_results(user)

        elif demisto.command() == 'safebreach-create-deployment':
            deployment = create_deployment(client=client)
            return_results(deployment)

        elif demisto.command() == 'safebreach-update-deployment':
            deployment = update_deployment(client=client)
            return_results(deployment)

        elif demisto.command() == "safebreach-delete-deployment":
            deployment = delete_deployment(client=client)
            return_results(deployment)

        elif demisto.command() == "safebreach-generate-api-key":
            result = create_api_key(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-api-key":
            result = delete_api_key(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-integration-errors":
            result = get_all_error_logs(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-integration-errors":
            result = delete_integration_error_logs(client=client)
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

        elif demisto.command() == "safebreach-rotate-verification-token":
            result = return_rotated_verification_token(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-test-summary":
            result = get_all_tests_summary(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-test-summary-with-plan-run-id":
            result = get_all_tests_summary_with_plan_id(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-test-summary-of-given-test":
            result = delete_test_result_of_test(client=client)
            return_results(result)

    except Exception as error:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(error)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
