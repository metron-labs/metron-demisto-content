import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
from copy import deepcopy

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

bool_map = {
    "true": True,
    "false": False,
    "True": True,
    "False": False,
    True: True,
    False: False
}

simulator_details_inputs = [
    InputArgument(name="secret", description="if secrets are to be included for search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="should_include_proxies", description="if proxies are to be included for search.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="hostname", description="if hostname to be included for search.",
                  required=False, is_array=False),
    InputArgument(name="connection_type", description="if connectionType to be included for search.",
                  required=False, is_array=False),
    InputArgument(name="external_ip", description="if external IP details to be included for search.",
                  required=False, is_array=False),
    InputArgument(name="internal_ip", description="if Internal IP are to be included for search.",
                  required=False, is_array=False),
    InputArgument(name="os", description="operating system name to filter with, Eg: LINUX,WINDOWS etc",
                  required=False, is_array=False),
    InputArgument(name="sort_direction", description="direction in which secrets are to be sorted.", options=["asc", "desc"],
                  default="asc", required=False, is_array=False),
    InputArgument(name="page_size", description="number of entries to search.", required=False, is_array=False),
    InputArgument(name="is_enabled", description="if to search only enabled ones.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="is_connected", description="status of connection of simulators to search.", options=["true", "false"],
                  required=False, is_array=False),
    InputArgument(name="is_critical", description="whether to search only for critical simulators or not.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="additional_details", description="Whether to show additional details or not.",
                  options=["true", "false"], required=False, is_array=False),
    InputArgument(name="status", description="if simulator status are to be included for search.",
                  options=["APPROVED", "PENDING", "ALL"],
                  default="ALL", required=False, is_array=False),
]

simulators_output_fields = [
    OutputArgument(name="is_enabled", description="Whether the simulator is enabled or not.",
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
                   output_type=str),
    OutputArgument(name="is_infiltration", description="If simulator is infiltration target.",
                   output_type=str),
    OutputArgument(name="is_mail_target", description="If simulator is mail target.",
                   output_type=str),
    OutputArgument(name="is_mail_attacker", description="If simulator is mail attacker.",
                   output_type=str),
    OutputArgument(name="is_pre_executor", description="Whether the simulator is pre executor.",
                   output_type=str),
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
                   output_type=str),
    OutputArgument(name="preferred_ip", description="Preferred Ip of simulator.",
                   output_type=str),
    OutputArgument(name="hostname", description="Hostname of given simulator.",
                   output_type=str),
    OutputArgument(name="connection_type", description="connection_type of given simulator.",
                   output_type=str),
    OutputArgument(name="simulator_status", description="status of the simulator.",
                   output_type=str),
    OutputArgument(name="connection_status", description="connection status of simulator.",
                   output_type=str),
    OutputArgument(name="simulator_framework_version", description="Framework version of simulator.",
                   output_type=str),
    OutputArgument(name="operating_system_type", description="operating system type of given simulator.",
                   output_type=str),
    OutputArgument(name="operating_system", description="Operating system of given simulator.",
                   output_type=str),
    OutputArgument(name="execution_hostname", description="Execution Hostname of the given simulator.",
                   output_type=str),
    OutputArgument(name="deployments", description="deployments simulator is part of.",
                   output_type=str),
    OutputArgument(name="created_at", description="Creation datetime of simulator.",
                   output_type=str),
    OutputArgument(name="updated_at", description="Update datetime of given simulator.",
                   output_type=str),
    OutputArgument(name="deleted_at", description="deletion datetime of given simulator.",
                   output_type=str),
    OutputArgument(name="assets", description="Assets of given simulator.",
                   output_type=str),
    OutputArgument(name="simulation_users", description="simulator users list.",
                   output_type=str),
    OutputArgument(name="proxies", description="Proxies of simulator.",
                   output_type=str),
    OutputArgument(name="advanced_actions", description="Advanced simulator details.",
                   output_type=str)
]

simulator_details_for_update_fields = [
    InputArgument(name="connection_url", required=False, is_array=False, description="""
                  the given value will be set as connection string, meaning this can be used to connect to
                  this URL.
                  """,),
    InputArgument(name="cloud_proxy_url", description="the given value will be set as cloud proxy url.",
                  required=False, is_array=False),
    InputArgument(name="name", required=False, is_array=False, description="""
                  the given value will be set as name of simulator. this will be the name of simulator once the command runs.
                  """),
    InputArgument(name="preferred_interface", required=False, is_array=False, description="""
                  the given value will be set as preferred interface.
                  """),
    InputArgument(name="preferred_ip", required=False, is_array=False, description="""
                  the given value will be set as Preferred IP to connect to the simulator.
                  """),
    InputArgument(name="tunnel", required=False, is_array=False, description="""
                  the given value will be set as tunnel.
                  """),
]

test_summaries_output_fields = [
    OutputArgument(name="planId", description="Plan ID of the simulation.", output_type=str),
    OutputArgument(name="planName", description="Test Name of the simulation.", output_type=str),
    OutputArgument(name="securityActionPerControl", description="Security Actions of the simulation.", output_type=str),
    OutputArgument(name="planRunId", description="Test id of the simulation.", output_type=str),
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

tests_outputs = [
    OutputArgument(name="id", description="Id of Actively running test.", output_type=int),
    OutputArgument(name="name", description="Name of the test being run.", output_type=str),
    OutputArgument(name="description", description="Details related to the test being run.", output_type=str),
    OutputArgument(name="successCriteria", description="Plan Run ID of the simulation.", output_type=str),
    OutputArgument(name="originalScenarioId", description="Original scenario ID of the running test", output_type=str),
    OutputArgument(name="actions count", description="number of actions", output_type=str),
    OutputArgument(name="edges count", description="number of edges.", output_type=str),
    OutputArgument(name="createdAt", description="details related to when test is created.", output_type=str),
    OutputArgument(name="updatedAt", description="details related to when test is last updated/changed", output_type=str),
    OutputArgument(name="steps count", description="number of steps in simulator.", output_type=str),
    OutputArgument(name="planId", description="planId of the test.", output_type=str),
    OutputArgument(name="originalPlan ID", description="original plan ID for reference.", output_type=str),
    OutputArgument(name="ranBy", description="User who ran the plan.", output_type=str),
    OutputArgument(name="ranFrom", description="Where the test ran from.", output_type=str),
    OutputArgument(name="enableFeedbackLoop", description="Should feedback loop be enabled.", output_type=str),
    OutputArgument(name="testID", description="plan run id.", output_type=str),
    OutputArgument(name="priority", description="priority of tests.", output_type=str),
    OutputArgument(name="retrySimulations", description="Should simulations be retried", output_type=str),
    OutputArgument(name="flowControl", description="Flow control of tests", output_type=str),
    OutputArgument(name="slot position", description="position in queue.", output_type=str),
    OutputArgument(name="slot status", description="is the test paused.", output_type=bool),
    OutputArgument(name="pauseDuration", description="is the test paused and if so till when", output_type=str),
    OutputArgument(name="totalJobs", description="Total number of jobs for this test", output_type=str),
    OutputArgument(name="pausedDate", description="when the test is paused", output_type=str),
    OutputArgument(name="expectedSimulationsAmount", description="number of simulations expected", output_type=str),
    OutputArgument(name="dispatchedSimulationsAmount", description="the number of simulations dispatched", output_type=str),
    OutputArgument(name="blockedSimulationsAmount", description="The number of simulations blocked", output_type=str),
    OutputArgument(name="unblockedSimulationsAmount", description="The number of simulations unblocked", output_type=str),
    OutputArgument(name="skippedSimulationsAmount", description="The number of simulations skipped", output_type=str),
    OutputArgument(name="failedSimulationsAmount", description="The number of simulations failed", output_type=str),
    OutputArgument(name="isPrepared", description="Total number of simulations that have been prepared", output_type=str),
]

test_outputs_headers_list = [
    "id", "name", "description", "successCriteria", "originalScenarioId", "actions count", "edges count",
    "createdAt", "updatedAt", "steps count", "planId", "originalPlan ID", "ranBy", "ranFrom", "enableFeedbackLoop",
    "planRunId", "priority", "retrySimulations", "flowControl", "slot position", "slot status", "pauseDuration",
    "totalJobs", "pausedDate", "expectedSimulationsAmount", "dispatchedSimulationsAmount", "blockedSimulationsAmount",
    "unblockedSimulationsAmount", "skippedSimulationsAmount", "failedSimulationsAmount", "isPrepared"
]


def test_outputs_headers_transform(header):
    return_map = {
        "id": "id",
        "name": "name",
        "description": "description",
        "successCriteria": "successCriteria",
        "originalScenarioId": "originalScenarioId",
        "actions count": "actions count",
        "edges count": "edges count",
        "createdAt": "createdAt",
        "updatedAt": "updatedAt",
        "steps count": "steps count",
        "planId": "planId",
        "originalPlan ID": "original Plan ID",
        "ranBy": "ranBy",
        "ranFrom": "ranFrom",
        "enableFeedbackLoop": "enableFeedbackLoop",
        "planRunId": "test id",
        "priority": "priority",
        "retrySimulations": "retrySimulations",
        "flowControl": "flowControl",
        "slot position": "slot position",
        "slot status": "slot status",
        "pauseDuration": "pauseDuration",
        "totalJobs": "totalJobs",
        "pausedDate": "pausedDate",
        "expectedSimulationsAmount": "expectedSimulationsAmount",
        "dispatchedSimulationsAmount": "dispatchedSimulationsAmount",
        "blockedSimulationsAmount": "blockedSimulationsAmount",
        "unblockedSimulationsAmount": "unblockedSimulationsAmount",
        "skippedSimulationsAmount": "skippedSimulationsAmount",
        "failedSimulationsAmount": "failedSimulationsAmount",
        "isPrepared": "isPrepared"
    }

    return return_map.get(header, header)


metadata_collector = YMLMetadataCollector(
    integration_name="Safebreach Content Management",
    description="""
    This Integration aims to provide easy access to safebreach from XSOAR.
    Following are the things that user can get access through XSOAR command integration:
    1. User get, create, update and delete. 
    2. Deployment create, update and delete.
    3. Tests get and delete.
    4. Simulators get, update, delete.
    5. Get current tests/simulation status and/or queue them.
    """,
    display="Safebreach Content Management",
    category="Deception & Breach Simulation",
    docker_image="demisto/python3:3.10.13.75921",
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
                  key_type=ParameterTypes.BOOLEAN),
          ConfKey(name="proxy",
                  display="Use system proxy settings",
                  required=False,
                  default_value=False,
                  additional_info="This Field is useful for asking integration to use default system proxy settings.",
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
    try:
        errors = errors_data.get("errors")
        if errors_data.get("statusCode") == 400:
            return json.dumps({"issue": errors_data.get("message"), "details": errors_data.get("additionalData")})
    except AttributeError:
        return errors_data

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


class SBError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class InputError(Exception):
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

    def __init__(self, api_key: str, account_id: int, base_url: str, verify: bool, proxy: bool):
        super().__init__(base_url=base_url, verify=verify)

        self.api_key = api_key
        self.account_id = account_id
        if proxy:
            self.proxies = handle_proxy()

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
        base_url = demisto.params().get("base_url", "").strip()
        base_url = base_url if base_url[-1] != "/" else base_url[0:-1]
        url = url if url[0] != "/" else url[1:]
        request_url = f"{base_url}/api/{url}"
        api_key = demisto.params().get("api_key", "").strip()
        headers = {
            'Accept': 'application/json',
            'x-apitoken': api_key
        }

        response = self._http_request(method=method, full_url=request_url, json_data=body, headers=headers,
                                      params=request_params, ok_codes=[200, 201, 204, 400])

        return response if not ((type(response) == dict) and (response.get("error") and not response.get("errorCode")))\
            else self.handle_sbcodes(response)

    def handle_sbcodes(self, response: dict):
        """
            This function handles errors related to SBcodes if the endpoint gives sbcode in errors

        Args:
            response (dict): all errors given by 400 response code will be accepted as dictionary and are formatted based on 
            the state of error

        Raises:
            Exception: all errors will be formatted and then thrown as exception string which will show as error_results in XSOAR
        """
        demisto.debug(f"error being sent to format_sb_code_error function is {response.get('error')}")
        exception_string = format_sb_code_error(response.get("error"))
        raise SBError(exception_string)

    def get_all_users_for_test(self):
        """
        This function is being used for testing connection with safebreach 
        after API credentials re taken from user when creating instance

        Returns:
            str: This is just status string, if "ok" then it will show test as success else it throws error
        """
        try:
            account_id = demisto.params().get("account_id", 0)
            url = f"/config/v1/accounts/{account_id}/users"
            response = self.get_response(url=url)
            demisto.info(f"the response of function get_all_users_for_test is {response}")
            if response and response.get("data"):
                return "ok"
            elif response.get("data") == []:
                return "please check the user details and try again"
            return "Could not verify the connection"
        except Exception as exc:
            if "Error in API call [404] - Not Found" in str(exc):
                return "Please check the URL configured and try again"
            elif "Error in API call [401] - Unauthorized" in str(exc):
                return "Please check the API used and try again"
            elif "SSL Certificate Verification Failed" in str(exc):
                return "Error with SSL certificate verification. Please check the URL used and try again"
            else:
                raise Exception(exc)

    def get_users_list(self):
        """This function returns all users present based on modifiers

        Returns:
            list: this is list of users queried based on modifiers specified
        """
        account_id = demisto.params().get("account_id", 0)
        url = f"/config/v1/accounts/{account_id}/users"
        params = {
            "details": "true",
            "deleted": "false"
        }
        response = self.get_response(url=url, request_params=params)
        user_data = response['data']
        return user_data

    def delete_user(self):
        """This function deletes a given user based on arguments of commands

        Returns:
            dict: user data related to the user who has been deleted
        """
        user_id = demisto.args().get("user_id")
        user_email = demisto.args().get("email", "").strip()
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
        demisto.info(f"available deployments are {available_deployments}")
        if not available_deployments:
            raise NotFoundError(f"deployments with name: {deployment_name} not found as you dont have any deployments")
        needed_deployments = list(filter(
            lambda deployment: deployment["name"].lower() == deployment_name.lower(), available_deployments))
        if not needed_deployments:
            raise NotFoundError("related deployment with given name couldn't be found")
        return needed_deployments[0]

    def create_deployment_data(self):
        """This function creates a deployment based on data given by user, this will be called by an external function
        which is triggered with a command for creating deployment

        Returns:
            dict: the data of deployment created
        """
        account_id = demisto.params().get("account_id", 0)
        name = demisto.args().get("name", "").strip()
        description = demisto.args().get("description", "").strip()
        simulators = demisto.args().get("simulators", "").replace('"', "").split(",")
        deployment_payload = {
            "nodes": simulators,
            "name": name,
            "description": description,
        }
        demisto.info(f"deployment creation payload is {deployment_payload}")
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
        deployment_id = demisto.args().get("deployment_id", "")
        if not deployment_id:
            raise InputError("Inputs Error: Deployment ID is a required field which has to have a value as input")

        name = demisto.args().get("updated_deployment_name", "").strip()
        simulators = demisto.args().get("updated_simulators_for_deployment", None)
        description = demisto.args().get("updated_deployment_description.", "").strip()
        deployment_payload = {}
        if name:
            deployment_payload["name"] = name
        if simulators:
            deployment_payload["nodes"] = simulators.replace('"', "").split(",")
        if description:
            deployment_payload["description"] = description

        demisto.info(f"deployment payload is {deployment_payload}")
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
        deployment_id = demisto.args().get("deployment_id", None)

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

        sort_map = {
            "endTime": "endTime",
            "startTime": "startTime",
            "testID": "planRunId",
            "stepRunId": "stepRunId"
        }

        account_id = demisto.params().get("account_id", 0)

        include_archived = demisto.args().get("include_archived")
        size = demisto.args().get("entries_per_page", 100)
        status = demisto.args().get("status")
        plan_id = demisto.args().get("plan_id")
        simulation_id = demisto.args().get("simulation_id")
        sort_by = sort_map.get(demisto.args().get("sort_by"), "endTime")

        parameters = {}
        method = "GET"
        url = f"/data/v1/accounts/{account_id}/testsummaries"
        for param in [("includeArchived", include_archived), ("size", size), ("status", status), ("planId", plan_id),
                      ("simulationId", simulation_id), ("sortBy", sort_by)]:
            parameters.update({} if not param[1] else {param[0]: param[1]})

        demisto.info(f"get_test_summary parameters is {parameters}")
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
                if key in ["endTime", "startTime"] and isinstance(test_summary[key], int):
                    test_summary[key] = datetime.utcfromtimestamp((test_summary[key]) / 1000).strftime(DATE_FORMAT)
        return test_summaries

    def flatten_tests_data(self, tests):
        """this function flattens tests data which is used for formatting running and queued tests

        Args:
            tests (list[dict]): This is list of dictionary containing data for tests which are queued

        Returns:
            list[dict]: the same data will have other keys which will be of more use to show in table
        """
        return_list = []
        return_obj = {}
        for test in tests:
            for key in list(test.keys()):
                if key == "actions":
                    return_obj['actions count'] = len(test[key])
                elif key == "edges":
                    return_obj['edges count'] = len(test[key])
                elif key == "steps":
                    return_obj["steps count"] = len(test[key])
                elif key == "slot":
                    return_obj["slot position"] = test[key]["id"]
                    return_obj["slot status"] = test[key]["isPaused"]
                elif key == "originalPlan":
                    return_obj["originalPlan ID"] = test[key].get("id")
                return_obj[key] = test[key]
            return_list.append(return_obj)
        return return_list

    def flatten_simulations_data(self, simulations):
        """this function flattens simulations data which is used for formatting running and queued simulations

        Args:
            simulations (dict[lists]): This is list of dictionary containing data for simulations which are queued

        Returns:
            list[dict]: the same data will have other keys which will be of more use to show in table
        """
        simulations_copy = deepcopy(simulations)
        return_list = []
        for simulation in simulations_copy:
            return_obj = {}
            return_obj["status"] = simulation
            simulation_type = simulations[simulation]
            items = list(simulation_type.values())
            for data in items:
                for key in data:
                    if key == "metadata":
                        return_obj['moveId'] = data["metadata"]["moveId"]
                        return_obj['moveRevision'] = data["metadata"]["moveRevision"]
                        # skipping params keys because it is full of ID's and useless for user
                    elif key == "actions":
                        return_obj['simulator_ids_involved'] = ""
                        return_obj["simulator_names_involved"] = ""
                        for object in data["actions"]:
                            return_obj['simulator_ids_involved'] = f"{return_obj['simulator_ids_involved']} ; {object['nodeId']}"
                            return_obj['simulator_names_involved'] = f"{return_obj['simulator_names_involved']} \
                                ; {object.get('nodeNameInMove','') or object.get('nodeNameInMoveDescription','')}"
                    else:
                        return_obj[key] = data[key]
                return_list.append(return_obj)

        return return_list

    def delete_test_result_of_test(self):
        """This function deletes test results of a given test ID by calling related endpoint

        Returns:
            dict: Deleted test data results
        """
        account_id = demisto.params().get("account_id", 0)
        test_id = demisto.args().get("test_id")

        method = "DELETE"
        url = f"/data/v1/accounts/{account_id}/tests/{test_id}"
        request_parameters = {
            "softDelete": "false"
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
            logs = error_logs[connector]["logs"] if error_logs[connector].get("status") != "ok" else []
            if logs:
                for log in logs:
                    log["connector"] = connector
                    flattened_logs_list.append(log)
        return flattened_logs_list

    def get_all_integration_error_logs(self):
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
        connector_id = demisto.args().get("integration_id", "").strip()
        demisto.info(f"connector id for deleting integration errors is {connector_id}")

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
        name = demisto.args().get("name", "").strip()
        description = demisto.args().get("description", "").strip()
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
        demisto.info(f"active api keys count is {len(active_keys.get('data'))}")
        required_key_object = list(filter(
            lambda key_obj: key_obj["name"].lower() == key_name.lower(), active_keys.get("data")))
        if not required_key_object:
            raise NotFoundError(f"couldn't find APi key with given name: {key_name}")
        return required_key_object[0]["id"]

    def delete_api_key(self):
        """This function calls API key delete endpoint

        Returns:
            dict: Deleted API key data
        """
        key_name = demisto.args().get("key_name", "").strip()
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
            request_params (dict): filters when querying the data related to simulators

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
            raise NotFoundError(f"No Matching simulators found with details not found details are {request_params}")
        return simulators_details

    def get_simulators_details_with_id(self):
        """This function queries for simulators along with modifiers which are request_params
        based on that we get simulator related details and this raises an exception if 
        no simulator with given details are found

        Args:
            request_params (dict): filters when querying the data related to simulators

        Raises:
            Exception: Raised when no entries are found related to given filters

        Returns:
            list(dict): returns simulator related data which fulfils the given input parameters
        """
        account_id = demisto.params().get("account_id", 0)
        simulator_id = demisto.args().get("simulator_id")
        method = "GET"
        url = f"/config/v1/accounts/{account_id}/nodes/{simulator_id}"

        simulators_details = self.get_response(method=method, url=url)
        return simulators_details

    def create_search_simulator_params(self):
        """This function creates parameters related to simulator as a dictionary

        Returns:
            dict: parameters dictionary
        """
        possible_inputs = {
            "secret": "secret",
            "should_include_proxies": "shouldIncludeProxies",
            "hostname": "hostname",
            "connection_type": "connectionType",
            "external_ip": "externalIp",
            "internal_ip": "internalIp",
            "os": "os",
            "status": "status",
            "sort_direction": "sortDirection",
            "page_size": "pageSize",
            "is_enabled": "isEnabled",
            "is_connected": "isConnected",
            "is_critical": "isCritical",
            "additional_details": "additionalDetails"
        }
        request_params = {
            "details": "true",
            "deleted": "false",
        }
        for parameter in possible_inputs:
            if demisto.args().get(parameter):
                request_params[possible_inputs[parameter]] = bool_map[demisto.args().get(parameter)] \
                    if (demisto.args().get(parameter) not in ["true", "false"] and parameter in ["details", "deleted",
                        "is_enabled", "is_connected", "is_critical", "additional_details"]) else demisto.args().get(parameter)
        return request_params

    def flatten_simulator_details(self, simulators):
        """this function will flatten the nested simulator data 
        into a flatter structure for table display

        Args:
            simulators List(dict): This is list of simulators which are to be flattened

        Returns:
            List(dict): This is list of simulators related data for table which is flattened 
            List : This is list of keys which are present in the dict
        """
        keys = None
        flattened_simulators = []
        for simulator in simulators:
            simulator_details = {
                "is_enabled": simulator.get("isEnabled"),
                "simulator_id": simulator.get("id"),
                "simulator_name": simulator.get("name"),
                "account_id": simulator.get("accountId"),
                "is_critical": simulator.get("isCritical"),
                "is_exfiltration": simulator.get("isExfiltration"),
                "is_infiltration": simulator.get("isInfiltration"),
                "is_mail_target": simulator.get("isMailTarget"),
                "is_mail_attacker": simulator.get("isMailAttacker"),
                "is_pre_executor": simulator.get("isPreExecutor"),
                "is_aws_attacker": simulator.get("isAWSAttacker"),
                "is_azure_attacker": simulator.get("isAzureAttacker"),
                "is_web_application_attacker": simulator.get("isWebApplicationAttacker"),
                "external_ip": simulator.get("externalIp"),
                "internal_ip": simulator.get("internalIp"),
                "preferred_interface": simulator.get("preferredInterface"),
                "preferred_ip": simulator.get("preferredIp"),
                "hostname": simulator.get("hostname"),
                "connection_type": simulator.get("connectionType"),
                "simulator_status": simulator.get("status"),
                "connection_status": simulator.get("isConnected"),
                "simulator_framework_version": simulator.get("frameworkVersion"),
                "operating_system_type": simulator.get("nodeInfo", {}).get("MACHINE_INFO", {}).get("TYPE", ""),
                "operating_system": simulator.get("nodeInfo", {}).get("MACHINE_INFO", {}).get("PLATFORM",
                                                                                              {}).get("PRETTY_NAME", ""),
                "execution_hostname": simulator.get("nodeInfo", {}).get("CURRENT_CONFIGURATION",
                                                                        {}).get("EXECUTION_HOSTNAME", ""),
                "deployments": simulator.get("group"),
                "created_at": simulator.get("createdAt"),
                "updated_at": simulator.get("updatedAt"),
                "deleted_at": simulator.get("deletedAt"),
                "assets": simulator.get("assets"),
                "simulation_users": simulator.get("simulationUsers"),
                "advanced_actions": simulator.get("advancedActions"),
                "proxies": simulator.get("proxies")
            }

            if not keys:
                keys = list(simulator_details.keys())
            flattened_simulators.append(simulator_details)

        return flattened_simulators, keys

    def delete_simulator_with_given_id(self, simulator_id, force: str):
        """This function calls delete simulator on simulator with given ID

        Args:
            simulator_id (str): This is simulator ID to delete
            force (str): If the simulator is to be force deleted even if its not connected 

        Returns:
            dict: Deleted simulator data
        """
        request_params = {
            "force": force
        }
        method = "DELETE"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{simulator_id}"

        deleted_simulator = self.get_response(url=request_url, method=method, request_params=request_params)
        return deleted_simulator

    def delete_simulator_with_given_name(self):
        """This function deletes a simulator with given name,
        This achieves this by retrieving ID by querying all simulators
        and then retrieving ID of name if it matches. 
        Then it calls a function which makes API call with this ID

        Returns:
            dict: deleted simulator related data
        """
        simulator_id = demisto.args().get("simulator_id")
        demisto.info(f"simulator id of given simulator is {simulator_id}")

        force_delete = "false"
        result = self.delete_simulator_with_given_id(simulator_id=simulator_id, force=force_delete)
        return result

    def make_update_simulator_payload(self):
        # this is created under assumption that only these fields will be  chosen to be updated by user
        """This function returns a payload with update related data

        Returns:
            dict: Update simulators payload
        """
        data_dict = {
            "connectionUrl": demisto.args().get("connection_url", "").lower().strip(),
            "cloudProxyUrl": demisto.args().get("cloud_proxy_url", "").strip(),
            "name": demisto.args().get("name", "").strip(),
            "tunnel": demisto.args().get("tunnel", "").strip(),
            "preferredInterface": demisto.args().get("preferred_interface", "").strip(),
            "preferredIp": demisto.args().get("preferred_ip", "").strip(),
        }
        demisto.info(f"update simulator payload before deletion of useless keys is {data_dict}")
        for (key, value) in tuple(data_dict.items()):
            if not value:
                data_dict.pop(key)
        return data_dict

    def update_simulator_api_call(self, simulator_id, simulator_data):
        """This function calls update simulators details API and returns updated data

        Args:
            simulator_id (str): ID of simulators to update
            simulator_data (dict): Payload for PUT call

        Returns:
            dict: Updated simulators details
        """
        method = "PUT"
        account_id = demisto.params().get("account_id")
        request_url = f"/config/v1/accounts/{account_id}/nodes/{simulator_id}"

        updated_simulator = self.get_response(url=request_url, method=method, body=simulator_data)
        return updated_simulator

    def update_simulator(self):
        """This function updates simulator with given name

        Returns:
            dict: this is updated simulators details for given simulators ID
        """
        simulator_id = demisto.args().get("simulator_id")
        demisto.info(f"simulator id is {simulator_id}")

        payload = self.make_update_simulator_payload()
        demisto.info(f"update simulator payload is {payload}")

        updated_simulator = self.update_simulator_api_call(simulator_id=simulator_id, simulator_data=payload)
        return updated_simulator

    def approve_simulator_with_given_name(self):
        """This function updates simulator with given name

        Returns:
            dict: this is updated simulators details for given simulators ID
        """
        simulator_id = demisto.args().get("simulator_id")
        demisto.info(f"simulator id is {simulator_id}")
        payload = {
            "status": "APPROVED"
        }

        approved_simulator = self.update_simulator_api_call(simulator_id=simulator_id, simulator_data=payload)
        return approved_simulator

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
        name = demisto.args().get("name", "").strip()
        email = demisto.args().get("email", "").strip()
        is_active = bool_map.get(demisto.args().get("is_active"), "false")
        send_email_post_creation = bool_map.get(demisto.args().get("email_post_creation"), "false")
        password = demisto.args().get("password")
        admin_name = demisto.args().get("admin_name", "").strip()
        change_password = bool_map.get(demisto.args().get("change_password_on_create"), "false")
        role = demisto.args().get("user_role", "").strip()
        deployment_list = demisto.args().get("deployments", None)
        try:
            deployment_list = list(map(int, deployment_list.split(","))) if deployment_list else []
        except ValueError:
            raise InputError("Input Error: deployments ids are numbers, please give deployments ids as comma separated values")

        if not email:
            raise InputError("Inputs Error: email is necessary when creating user, please give a valid email which hasn't \
                been used before for user creation")

        user_payload = {
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

        demisto.info(f"user payload for create user is {user_payload}")
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

        user_id = demisto.args().get("user_id")
        user_email = demisto.args().get("email", "").strip()

        name = demisto.args().get("name", "").strip()
        is_active = bool_map[demisto.args().get("is_active", "False")]
        description = demisto.args().get("user_description", "").strip()
        role = demisto.args().get("user_role", "").strip()
        password = demisto.args().get("password")
        deployment_list = demisto.args().get("deployments", [])
        try:
            deployment_list = list(map(int, deployment_list.split(","))) if deployment_list else []
        except ValueError:
            raise InputError("Input Error: deployments ids are numbers, please give deployments ids as comma separated values")

        # formatting the update user payload, we remove false values after passing to function which calls endpoint
        details = {
            "name": name,
            "isActive": is_active,
            "deployments": deployment_list,
            "description": description,
            "role": role,
            "password": password
        }
        demisto.info(f"upload user payload is {details}")
        # retrieve user based on email and user_id whichever is present
        if user_email and not user_id:
            user_list = self.get_users_list()
            demisto.info("retrieved user list which contains all available users in safebreach")
            user = list(filter(lambda user_data: user_data.get("email") == user_email, user_list))
            if not user:
                demisto.info(f"filtered users are {user} while all users are {user_list}")
                raise NotFoundError(f"User with {user_id} or {user_email} not found")
            user_id = user[0]["id"]
        user = self.update_user_with_details(user_id, details)
        return user

    def get_active_tests(self):
        """This function calls GET of active tests being run endpoint

        Returns:
            Dict: Returns test data as a dictionary per test which is array as value for "data" key
        """
        account_id = demisto.params().get("account_id", 0)

        method = "GET"
        url = f"/orch/v2/accounts/{account_id}/queue"
        tests = self.get_response(url=url, method=method)
        return tests

    def get_active_simulations(self):
        """This function calls GET of active tests being run endpoint

        Returns:
            Dict: Returns test data as a dictionary per test which is array as value for "data" key
        """
        method = "GET"
        url = "/execution/v2/tasks"
        simulations_details = self.get_response(url=url, method=method)
        return simulations_details

    def set_simulations_status(self):
        account_id = demisto.params().get("account_id", 0)

        method = "PUT"
        url = f"orch/v3/accounts/{account_id}/queue/state"
        data = {
            "status": demisto.args().get("simulation_or_test_state", "").strip()
        }
        simulations_details = self.get_response(url=url, method=method, body=data)
        return simulations_details

    def get_schedules(self):
        account_id = demisto.params().get("account_id", 0)

        method = "GET"
        url = f"/config/v1/accounts/{account_id}/schedules"
        request_params = {
            "details": "true",
            "deleted": "false"
        }
        schedule_data = self.get_response(url=url, method=method, request_params=request_params)
        return schedule_data

    def append_cron_to_schedule(self, schedules):

        for schedule in schedules:
            if schedule["cronString"]:
                schedule["user_schedule"] = CronString(schedule["cronString"], schedule["cronTimezone"]).to_string()
        return schedules

    def delete_schedule(self):
        account_id = demisto.params().get("account_id", 0)
        schedule_id = demisto.args().get("schedule_id")

        method = "DELETE"
        url = f"/config/v1/accounts/{account_id}/schedules/{schedule_id}"

        schedule_data = self.get_response(url=url, method=method)
        return schedule_data

    def extract_default_scenario_fields(self, scenarios):
        return_list = []
        for scenario in deepcopy(scenarios):
            return_obj = {
                "tags_list": "",
                "steps_order": ""
            }
            for key in scenario:
                if key == "tags" and scenario[key]:
                    return_obj["tags_list"] = ", ".join(scenario.get(key, []))
                elif key == "steps" and scenario[key]:
                    steps_involved = [step.get('name') for step in scenario[key]]
                    return_obj['steps_order'] = "; ".join(steps_involved)
                return_obj[key] = scenario[key]
            return_list.append(return_obj)
        return return_list

    def extract_custom_scenario_fields(self, scenarios):
        return_list = []
        for scenario in deepcopy(scenarios):
            return_obj = {
                "actions_list": "",
                "steps_order": "",
                "edges_count": 0
            }
            for key in scenario:
                if key == "actions" and scenario[key]:
                    actions_list = [f"{action.get('type')} with identity: "
                                    + f"{action.get('data',{}).get('uuid','') or action.get('data',{}).get('id','')}"
                                    for action in scenario[key]]
                    return_obj["actions_list"] = "; ".join(actions_list)
                elif key == "steps" and scenario[key]:
                    steps_involved = [step.get('name') for step in scenario[key] if step.get("name") is not None]
                    return_obj["steps_order"] = "; ".join(steps_involved)
                elif key == "edges":
                    return_obj["edges_count"] = len(scenario[key])
                return_obj[key] = scenario[key]
            return_obj["custom_data_object_for_rerun_simulation"] = json.dumps({
                "name": return_obj.get("name"),
                "steps": return_obj.get("steps")
            })
            return_list.append(return_obj)

        return return_list

    def extract_test_fields(self, test):
        return_obj = {
            "actions_list": "",
            "steps_order": "",
            "edges_count": 0
        }
        for key in test:
            if key == "actions" and test[key]:
                new_list = [f"{action.get('type')} with id:{action.get('id','')}" for action in test[key]]
                return_obj["actions_list"] = "; ".join(new_list)
            elif key == "steps" and test[key]:
                steps_involved = [f"{step.get('name')}- with test ID {step.get('planRunId')}" for step in test[key]
                                  if step.get("name") is not None]
                return_obj["steps_order"] = "; ".join(steps_involved)
            elif key == "edges":
                return_obj["edges_count"] = len(test[key])
            return_obj[key] = test[key]
        return return_obj

    def format_services_response(self, services):
        return_list = []
        for service in deepcopy(services):
            service["connection_status"] = f"Service {service['name']} is \
                {'running' if service['isUp'] else 'not running'} as on {service['lastCheck']}"
            return_list.append(service)
        return return_list

    def get_prebuilt_scenarios(self):

        method = "GET"
        url = "/content-manager/v18/scenarios"

        scenarios = self.get_response(url=url, method=method)
        return scenarios

    def get_custom_scenarios(self):

        account_id = demisto.params().get("account_id", 0)

        method = "GET"
        url = f"/config/v2/accounts/{account_id}/plans"
        request_params = {
            "details": demisto.args().get("schedule_details", "").strip()
        }
        scenarios = self.get_response(url=url, method=method, request_params=request_params)
        return scenarios

    def get_services_status(self):

        method = "GET"
        url = "/lighthouse/v1/services"
        services_data = self.get_response(url=url, method=method)
        return services_data

    def get_simulations(self):

        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/data/v1/accounts/{account_id}/executionsHistoryResults"

        request_params = {
            "runId": demisto.args().get("test_id")
        }

        simulations_data = self.get_response(url=url, method=method, request_params=request_params)
        return simulations_data

    def get_verification_token(self):

        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}/nodes/secret"
        verification_data = self.get_response(url=url, method=method)
        return verification_data

    def rerun_test_or_simulation(self):

        account_id = demisto.params().get("account_id", 0)

        if demisto.command() == "safebreach-rerun-test":
            test_data = {
                "testId": demisto.args().get("test_id"),
                "name": demisto.args().get("test_name", ""),
            }
        elif demisto.command() == "safebreach-rerun-simulation":
            simulation_ids = demisto.args().get("simulation_ids").strip()
            simulation_ids = simulation_ids.replace('"', "").split(",")
            simulations_list = []
            for simulation in simulation_ids:
                try:
                    simulations_list.append(int(simulation))
                except ValueError:
                    raise InputError("Input Error: simulation_ids are numbers and not strings, please \
                        enter valid simulation ids")
            test_data = {
                "name": demisto.args().get("simulation_name", "").strip(),
                "steps": [
                        {
                            "attacksFilter": {},
                            "attackerFilter": {},
                            "targetFilter": {},
                            "systemFilter": {
                                "simulations": {
                                    "operator": "is",
                                    "values": simulations_list
                                }
                            }
                        }
                ]
            }

        position = demisto.args().get("position")
        feedback_loop = demisto.args().get("enable_feedback_loop")
        retry_simulations = demisto.args().get("retry_simulation")
        wait_for_retry = demisto.args().get("wait_for_retry")
        priority = demisto.args().get("priority")
        request_params = {
            "position": position,
            "enableFeedbackLoop": feedback_loop,
            "retrySimulations": retry_simulations,
            "priority": priority,
            "waitForRetry": wait_for_retry
        }
        for parameter in list(request_params.keys()):
            if not request_params[parameter]:
                request_params.pop(parameter)

        demisto.info(f"processed request parameters payload is {request_params}")

        method = "POST"
        url = f"/orch/v3/accounts/{account_id}/queue"
        tests_data = self.get_response(url=url, method=method, body={"plan": test_data}, request_params=request_params)
        return tests_data


def get_simulators_and_display_in_table(client: Client):
    """This function gets all simulators and displays in table

    Args:
        client (Client): Client class for API calls
        just_name (bool, optional): This will be used to know whether to search and return all 
        simulators or only one. Defaults to False.

    Returns:
        CommandResults : table showing simulator details
        dict: simulator details
    """
    request_params = client.create_search_simulator_params()
    demisto.info(f"request parameters for {demisto.command()} is {request_params}")

    result = client.get_simulators_details(request_params=request_params)
    demisto.info(f"related simulations are {result}")

    flattened_simulators, keys = client.flatten_simulator_details(result.get("data", {}).get("rows", {}))

    human_readable = tableToMarkdown(
        name="Simulators Details",
        t=flattened_simulators,
        headers=keys)
    outputs = result.get("data", {}).get("rows")
    outputs_prefix = "simulator_details"
    demisto.info(f"json output is {outputs} with prefix {outputs_prefix}")

    result = CommandResults(
        outputs_prefix=outputs_prefix,
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def format_simulations_data(simulations):
    return_list = []
    for simulation in simulations:
        return_object = {}
        for key in simulation:
            if key in ["id", "planName", "attackerNodeName", "id", "finalStatus", "resultDetails",
                       "securityAction", "targetNodeName", "securityAction", "moveDesc"]:
                return_object[key] = simulation.get(key)
            elif key == "Attack_Type":
                return_object["attacks_involved"] = ", ".join([attack["displayName"] for attack in simulation[key]])
        return_list.append(return_object)
    return return_list


def get_specific_simulator_details(client: Client):
    """This function simulator details and displays in table

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults : table showing simulator details
        dict: simulator details
    """

    result = client.get_simulators_details_with_id()
    demisto.info(f"related simulations are {result}")

    flattened_simulators, keys = client.flatten_simulator_details([result.get("data", {})])

    human_readable = tableToMarkdown(
        name="Simulators Details",
        t=flattened_simulators,
        headers=keys)
    outputs = result.get("data", {})
    outputs_prefix = "simulator_details_with_id"
    demisto.info(f"json output is {outputs} with prefix {outputs_prefix}")

    result = CommandResults(
        outputs_prefix=outputs_prefix,
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def tests_header_transformer(header):
    return_map = {
        'planId': 'planId',
        "planName": "planName",
        'securityActionPerControl': 'securityActionPerControl',
        'planRunId': 'testID',
        "status": "status",
        "plannedSimulationsAmount": "plannedSimulationsAmount",
        "simulatorExecutions": "simulatorExecutions",
        "ranBy": "ranBy",
        "simulatorCount": "simulatorCount",
        "endTime": "endTime",
        "startTime": "startTime",
        "stopped": "stopped",
        "missed": "missed",
        "logged": "logged",
        "detected": "detected",
        "prevented": "prevented",
        "inconsistent": "inconsistent",
        "drifted": "drifted",
        "not_drifted": "not_drifted",
        "baseline": "baseline"
    }
    return return_map.get(header, header)


def get_tests_summary(client: Client):
    """This function retrieves tests and then flattens them and shows them in  a table

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: This returns a table view of data and a dictionary as output
    """
    test_summaries = client.get_tests_with_args()
    demisto.info(f"output of get_tests_summary is {test_summaries}")
    client.flatten_test_summaries(test_summaries)
    human_readable = tableToMarkdown(
        name="Test Results",
        t=test_summaries,
        headerTransform=tests_header_transformer,
        headers=['planId', "planName", 'securityActionPerControl', 'planRunId', "status", "plannedSimulationsAmount",
                 "simulatorExecutions", "ranBy", "simulatorCount", "endTime", "startTime", "stopped", "missed",
                 "logged", "detected", "prevented", "inconsistent", "drifted", "not_drifted", "baseline"])
    outputs = {
        'tests_data': test_summaries
    }
    demisto.info(f"json output of get_tests_summary is {outputs}")
    result = CommandResults(
        outputs_prefix="tests_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-all-users",
    inputs_list=None,
    outputs_prefix="user_data",
    outputs_list=[
        OutputArgument(name="id", prefix="user_data", output_type=int,
                       description="The ID of User retrieved. this can be used to further link this user with\
                       user_id field of safebreach-update-user or safebreach-delete-user commands"),
        OutputArgument(name="name", prefix="user_data", output_type=str,
                       description="The name of User retrieved."
                       ),
        OutputArgument(name="email", prefix="user_data", output_type=str,
                       description="The email of User retrieved. this can be used for updating user or\
                       deleting user for input email of commands safebreach-update-user or safebreach-delete-user "),
    ],
    description="This command gives all users who are not deleted.")
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
        InputArgument(name="name", required=False, is_array=False, description="""
                      Name of the user to lookup. This will first retrieve all users and show details related to 
                      name entered here. this name will be search of if name is part of name given to user and not 
                      a perfect match. For example if actual name is 'demisto' but if input is 'dem', even then this
                      will be shown as a valid match to name. This is so that command user need not know exact name of
                      user and just searching first name or last name will work.
                      """),
        InputArgument(name="email", required=False, is_array=False, description="""
                      Email of the user to lookup. This will be used to retrieve user with matching email that user entered
                      partial email search doesn't work here.
                      """)
    ],
    outputs_prefix="filtered_users",
    outputs_list=[
        OutputArgument(name="id", prefix="user_data", output_type=int,
                       description="The ID of User retrieved. this can be used to further link this user with user_id field of \
                       safebreach-update-user or safebreach-delete-user commands"),
        OutputArgument(name="name", prefix="user_data", output_type=str,
                       description="The name of User retrieved."),
        OutputArgument(name="email", prefix="user_data", output_type=str,
                       description="The email of User retrieved. this can be used for updating user or deleting user \
                       for input email of commands safebreach-update-user or safebreach-delete-user"),
    ],
    description="This command gives all users which match the inputs given, Since email is a unique field we only get one user if\
            email matches but if name is given as input then care should be taken to see name matches exactly.\
            else there is a chance that multiple users are retrieved, please not that either name or email are to\
            be populated and if neither of them are given as input then it results in error")
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

    name = demisto.args().get("name", "").strip()
    email = demisto.args().get("email", "").strip()
    if not (name or email):
        raise InputError("Incorrect inputs: either name or email are to be given.")
    user_list = client.get_users_list()
    demisto.info(f"retrieved user list which has {len(user_list)} users")

    filtered_user_list = list(
        filter(lambda user_data: ((name.lower() == user_data['name'].lower() if name else False) or
                                  (email.lower() == user_data['email'].lower())), user_list))
    demisto.info(f"filtered user list which contains {len(filtered_user_list)}")

    if filtered_user_list:
        human_readable = tableToMarkdown(name="user data", t=filtered_user_list, headers=['id', 'name', 'email'])
        outputs = filtered_user_list

        result = CommandResults(
            outputs_prefix="filtered_users",
            outputs=outputs,
            readable_output=human_readable
        )

        return result
    demisto.info(f"list of retrieved users are {user_list}")
    raise NotFoundError(f"user with name {name} or email {email} was not found")


@metadata_collector.command(
    command_name="safebreach-create-user",
    inputs_list=[
        InputArgument(name="name", required=True, is_array=False, description="Name of the user to create."),
        InputArgument(name="email", required=True, is_array=False, description="Email of the user to Create."),
        InputArgument(name="is_active", description="""
                      Whether the user is active upon creation. if this is set to true then user will be active as soon
                      as this command succeeds but if set to false then the user has to activated and if user will have to
                      do reset password process to become active. by default the user will be active.
                      """,
                      required=False, is_array=False, options=["true", "false"], default="true"),
        InputArgument(name="email_post_creation", required=False, is_array=False, options=["true", "false"], default="true",
                      description="""
                      This field sends email to user post creation if this field is set to true, by default this field is set 
                      to false. set this to true if user has to be sent email post creation else set this to false.
                      """),
        InputArgument(name="password", required=True, is_array=False, description="""
                      This will be set as password for the created user. incase needed the flag change password can be set to
                      true if its needed for user to change password on first login.
                      """,),
        InputArgument(name="admin_name", required=False, is_array=False, description="""
                      Name of the Admin creating user. This will be populated in created by field of user page in safebreach.
                      """),
        InputArgument(name="change_password_on_create", required=False, is_array=False, options=["true", "false"],
                      default="false", description="""
                      Should user change password on creation. when this is set to true then user will have to reset password on
                      the next login, this can be used if we want user to reset password as soon as they login.
                      """,),
        InputArgument(name="user_role", required=False, is_array=False, description="""
                      Role of the user being Created. The user will have the permissions of role they are being assigned here.
                      choices are viewer, administrator, content developer, operator.
                      """,
                      options=["viewer", "administrator", "contentDeveloper", "operator"], default="viewer"),
        InputArgument(name="deployments", required=False, is_array=True,
                      description="""
                      Comma separated ID of all deployments the user should be part of. The deployment IDs can be retrieved from
                      get-deployments-list command or from UI directly but care should be noted that only deployment ids of 
                      deployments which haven't been deleted will be shown here and after creation of user. for example
                      if 1,2,3 are deployment ids given while creation but if 2 is deleted then when user is created , he will
                      only have 1,3.
                      """)
    ],
    outputs_prefix="created_user_data",
    outputs_list=[
        OutputArgument(name="id", description="The ID of User created.", prefix="created_user_data", output_type=int),
        OutputArgument(name="name", description="The name of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="email", description="The email of User created.", prefix="created_user_data",
                       output_type=str),
        OutputArgument(name="createdAt", prefix="created_user_data", output_type=str,
                       description="The creation time of User."),
        OutputArgument(name="deletedAt", prefix="created_user_data", output_type=str,
                       description="The Deletion time of User . This will be empty unless the user is deleted"),
        OutputArgument(name="roles", prefix="created_user_data", output_type=str,
                       description="The roles and permissions of User created.",),
        OutputArgument(name="description", prefix="created_user_data", output_type=str,
                       description="The description of User if any is given at creation time, it will be populated here.",),
        OutputArgument(name="role", prefix="created_user_data",
                       output_type=str, description="The role assigned to user during creation."),
        OutputArgument(name="deployments", prefix="created_user_data", output_type=str,
                       description="The deployments user is part of.",),
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
    demisto.info(f"json output for create user is {outputs}")

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
        InputArgument(name="user_id", required=False, is_array=False,
                      description="""
                      user ID of user from safebreach to search. this can be retrieved in 2 ways,
                      1. run get-all-users command and then look for user id of user with matching criteria
                      but to see details its required that details parameter to be set to true,
                      2. if you know user name or email then those can be used in safebreach-get-user-with-given-name-or-email
                      command and then search for user with required details in displayed results for ID.
                      This field is not  required, meaning even if just email is given , we will internally search user
                      id with the matching email and use the user for further process
                      """),
        InputArgument(name="email", required=False, is_array=False,
                      description="""
                      Email of the user to Search for updating user details. This is a required field.
                      The user with matching email will be considered as user whose data will be updated
                      """),
        InputArgument(name="name", required=False, is_array=False, description="""
                      Update the user name to given value of this field, 
                      unless this field is left empty, whatever is present here will be updated to user details.
                      user will be selected based on user_id or email fields mentioned above.
                      """,),
        InputArgument(name="user_description", required=False, is_array=False, description="""
                      Update the user Description to given value in this field. This will be updated description of user
                      unless this field is left empty, whatever is present here will be updated to user details.
                      user will be selected based on user_id or email fields mentioned above.
                      """),
        InputArgument(name="is_active", required=False, is_array=False, options=["true", "false", ""], default="",
                      description="""
                      Update the user Status based on the input, if this is set to false then user will be deactivated.
                      unless this field is left empty, whatever is present here will be updated to user details.
                      user will be selected based on user_id or email fields mentioned above.
                      """,),
        InputArgument(name="password", required=False, is_array=False, description="""
                      Password of user to be updated with. this will be used for changing password for user.
                      unless this field is left empty, whatever is present here will be updated to user details.
                      user will be selected based on user_id or email fields mentioned above.
                      """),
        InputArgument(name="user_role", required=False, is_array=False,
                      options=["viewer", "administrator", "contentDeveloper", "operator"], default="", description="""
                      Role of the user to be changed to. unless you want to change the user role and permissions, 
                      dont select anything in this field, user will be selected based on user_id or email fields mentioned above.
                      """),
        InputArgument(name="deployments", required=False, is_array=True, description="""
                        Comma separated ID of all deployments the user should be part of.
                        unless this field is left empty, whatever is present here will be updated to user details.
                        user will be selected based on user_id or email fields mentioned above.
                      """,
                      )
    ],
    outputs_prefix="updated_user_data",
    outputs_list=[
        OutputArgument(name="id", prefix="updated_user_data", output_type=int,
                       description="The ID of User whose data has been updated."),
        OutputArgument(name="name", prefix="updated_user_data", output_type=str,
                       description="The name of User after running the update command according to safebreach records."),
        OutputArgument(name="email", prefix="updated_user_data", output_type=str,
                       description="the email of the user whose data has been updated by the command."),
        OutputArgument(name="createdAt", prefix="updated_user_data", output_type=str,
                       description="the time at which the user who has been selected has been created"),
        OutputArgument(name="updatedAt", prefix="updated_user_data", output_type=str,
                       description="The last updated time of User selected for update. \
                       this will be the execution time for the command or close to it."),
        OutputArgument(name="deletedAt", prefix="updated_user_data", output_type=str,
                       description="The Deletion time of User selected to update. Generally this is empty unless\
                       user chosen to update is a deleted user"),
        OutputArgument(name="roles", prefix="updated_user_data", output_type=str,
                       description="The roles of User updated. these will change if role has been updated during\
                       updating user details else they will be same as pre update."),
        OutputArgument(name="description", prefix="updated_user_data", output_type=str,
                       description="The description of User after updating user, if description field has been given any\
                       new value during update then its updated else this will be left unchanged from previous value."),
        OutputArgument(name="role", prefix="updated_user_data", output_type=str,
                       description="The roles and permissions related to user who has been selected for update.unless this field\
                       has been given a value , this will not be updated and will stay the same as previous value."),
        OutputArgument(name="deployments", prefix="updated_user_data", output_type=str,
                       description="The deployments related to user, this will be comma separated values of deployment IDs"),
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

    demisto.info(f"json output for update user is {outputs}")
    result = CommandResults(
        outputs_prefix="updated_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-delete-user",
    inputs_list=[
        InputArgument(name="user_id", required=False, is_array=False,
                      description="""
                      user ID of user from safebreach to search. this can be retrieved in 2 ways,
                      1. run get-all-users command and then look for user id of user with matching criteria
                      but to see details its required that details parameter to be set to true,
                      2. if you know user name or email then those can be used in safebreach-get-user-with-given-name-or-email
                      command and then search for user with required details in displayed results for ID.
                      This field is not  required, meaning even if just email is given , we will internally search user
                      id with the matching email and use the user for further process
                      """),
        InputArgument(name="email", required=True, is_array=False,
                      description="""
                      Email of the user to Search for updating user details. This is a required field.
                      The user with matching email will be considered as user whose data will be updated
                      """)
    ],
    outputs_prefix="deleted_user_data",
    outputs_list=[
        OutputArgument(name="id", prefix="deleted_user_data", output_type=int,
                       description="The ID of User whose data has been deleted."),
        OutputArgument(name="name", prefix="deleted_user_data", output_type=str,
                       description="The name of User deleted.",),
        OutputArgument(name="email", description="The email of User deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="createdAt", prefix="deleted_user_data", output_type=str,
                       description="the time at which the user who has been selected has been created"),
        OutputArgument(name="updatedAt", prefix="deleted_user_data", output_type=str,
                       description="The last updated time of User selected for delete.\
                       this will be less than time choses to delete"),
        OutputArgument(name="deletedAt", prefix="deleted_user_data", output_type=str,
                       description="The Deletion time of User selected to delete.\
                       this will be the execution time for the command or close to it."),
        OutputArgument(name="roles", description="The roles of User before they were deleted.", prefix="deleted_user_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of User who has been deleted.",
                       prefix="deleted_user_data", output_type=str),
        OutputArgument(name="role", description="The roles and permissions of User who has been deleted.",
                       prefix="deleted_user_data", output_type=str),
        OutputArgument(name="deployments", description="The deployments related to user before he was deleted.",
                       prefix="deleted_user_data", output_type=str),
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

    demisto.info(f"json output for delete uer is {outputs}")
    result = CommandResults(
        outputs_prefix="deleted_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def deployment_transformer(header):
    return_map = {
        'id': 'id',
        "accountId": "accountId",
        'name': 'name',
        'createdAt': 'createdAt',
        "description": "description",
        "nodes": "simulators",
        "updatedAt": "updatedAt"
    }

    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-create-deployment",
    inputs_list=[
        InputArgument(name="name", required=True, is_array=False, description="""
                      Name of the deployment to create. this will be shown as name in deployments page of safebreach
                      """),
        InputArgument(name="description", required=False, is_array=False,
                      description="""
                      Description of the deployment to create. 
                      This will show as description of the deployment in your safebreach instance.
                      It is generally preferable to give description while creating a deployment for easier identification
                      """),
        InputArgument(name="simulators", required=False, is_array=True, description="""
                      A deployment is a group of simulators which work as a single group. this field needs
                      Comma separated IDs of all simulators that should be part of this deployment.
                      the ID can be retrieved from safebreach-get-all-simulator-details command with
                      details input set to true so that the details can be seen. Care should be taken when giving 
                      simulator IDs as comma separated values as if any simulator has been deleted then this deployment 
                      wont contain that simulator on creation
                      """)
    ],
    outputs_prefix="created_deployment_data",
    outputs_list=[
        OutputArgument(name="id", prefix="created_deployment_data", output_type=int,
                       description="The ID of deployment created. this Id can be used to update ,delete deployment as\
                       deployment_id field of the deployment."),
        OutputArgument(name="accountId", prefix="created_deployment_data", output_type=str,
                       description="This field shows account ID of user who has created the account."),
        OutputArgument(name="name", prefix="created_deployment_data", output_type=str,
                       description="The name of deployment created. this will be name which will be shown on deployments page\
                       of safebreach and name that is given as input to the command."),
        OutputArgument(name="createdAt", prefix="created_deployment_data", output_type=str,
                       description="The creation date and time of deployment , this will be closer to\
                       command execution time if the deployment creation is successful."),
        OutputArgument(name="description", prefix="created_deployment_data", output_type=str,
                       description="The description of the deployment created will be shown in description \
                           part of the table in safebreach."),
        OutputArgument(name="simulators", prefix="created_deployment_data", output_type=str,
                       description="The simulators that are part of deployment. In case any simulators are given during\
                       creation that are deleted before the creation time then the deployment wont contain those simulators."),
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
                                     headerTransform=deployment_transformer,
                                     headers=['id', "accountId", 'name', 'createdAt', "description", "nodes"])
    outputs = created_deployment.get("data", {})
    demisto.info(f"json output for create deployment is {outputs}")

    result = CommandResults(
        outputs_prefix="created_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-update-deployment",
    inputs_list=[
        InputArgument(name="deployment_id", required=True, is_array=False, description="""
                      ID of the deployment to update. this can be searched with list-deployments command or
                      from UI. this will be taken as id of deployment whose properties we want to update.
                      """),
        InputArgument(name="updated_simulators_for_deployment", required=False, is_array=False,
                      description="""
                      Comma separated ID of all simulators the deployment should be part of. These simulators can be
                      retrieved by calling get-all-available-simulator-details command and that command will
                      show the results of the all available simulators and the ids of those simulators can be used as
                      comma separated values in this field for those simulators to act as a group.
                      """),
        InputArgument(name="updated_deployment_name", required=False, is_array=False,
                      description="""
                      This fields value will be the name which the deployment name will be updated to. 
                      """),
        InputArgument(name="updated_deployment_description", required=False, is_array=False,
                      description="description of the deployment to which value this should be updated to."),
    ],
    outputs_prefix="updated_deployment_data",
    outputs_list=[
        OutputArgument(name="id", prefix="updated_deployment_data", output_type=int,
                       description="The ID of deployment whose values have been updated.\
                           ID cant be changed so this wont be updated."),
        OutputArgument(name="accountId", prefix="updated_deployment_data", output_type=str,
                       description="The accountId of user who created the deployment."),
        OutputArgument(name="name", prefix="updated_deployment_data", output_type=str,
                       description="The name of deployment which has been updated to the name given in updated_deployment_name.\
                        this will be the name shown in deployment name field of table in deployments page in safebreach UI"),
        OutputArgument(name="createdAt", prefix="updated_deployment_data", output_type=str,
                       description="The creation date and time of deployment whose data has been updated."),
        OutputArgument(name="updatedAt", prefix="updated_deployment_data", output_type=str,
                       description="The last updated date and time of deployment whose data has been updated.\
                       This will generally be closer to the update deployment command run time for reference"),
        OutputArgument(name="description", prefix="updated_deployment_data", output_type=str,
                       description="The updated description of deployment which is provided in updated_deployment_description\
                       field of input . This will now be the description which is shown in description field of deployments\
                       table of safebreach UI"),
        OutputArgument(name="simulators", prefix="updated_deployment_data", output_type=str,
                       description="The simulators that are part of deployment. unless any simulators are given as input this \
                           field won't be updated this field doesn't reflect changes if simulators given as input are deleted"),
    ],
    description="""
    This command updates a deployment with given data. The deployment_id field of this command can  be retrieved from 
    get-all-deployments command. If the user wants to search with deployment ID then they can search it that way or 
    if user just wants to search with name then they can just give name field and the command internally searches the deployment 
    with given name and updates it.
    """)
def update_deployment(client: Client):
    """This function is executed on command "safebreach-update-deployment"

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: updated deployment data as a table and a dictionary
    """
    updated_deployment = client.update_deployment()

    human_readable = tableToMarkdown(name="Updated Deployment", t=updated_deployment.get("data", {}),
                                     headerTransform=deployment_transformer,
                                     headers=['id', "accountId", 'name', 'createdAt',
                                              "description", "nodes", "updatedAt"])
    outputs = updated_deployment.get("data", {})
    demisto.info(f"json output for update deployment is {outputs}")

    result = CommandResults(
        outputs_prefix="updated_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-delete-deployment",
    inputs_list=[
        InputArgument(name="deployment_id", required=True, is_array=False, description="""
                      ID of the deployment to delete. this can be searched with list-deployments command or
                      from UI. this will be taken as id of deployment which we want to delete.
                      """)
    ],
    outputs_prefix="deleted_deployment_data",
    outputs_list=[
        OutputArgument(name="id", prefix="deleted_deployment_data", output_type=int,
                       description="The ID of deployment which has been deleted.",),
        OutputArgument(name="accountId", prefix="deleted_deployment_data", output_type=str,
                       description="The account Id of user who deleted the deployment."),
        OutputArgument(name="name", prefix="deleted_deployment_data", output_type=str,
                       description="The name of deployment before the deployment was deleted.",),
        OutputArgument(name="createdAt", prefix="deleted_deployment_data", output_type=str,
                       description="The creation date and time of deployment which has been deleted."),
        OutputArgument(name="description", prefix="deleted_deployment_data", output_type=str,
                       description="The description of deployment before it was deleted."),
        OutputArgument(name="simulators", prefix="deleted_deployment_data", output_type=str,
                       description="The simulators that are part of deployment before it was deleted."),
    ],
    description="""
    This command deletes a deployment with given data.The deployment_id field of this command can  be retrieved from 
    get-all-deployments command. If the user wants to search with deployment ID then they can search it that way or 
    if user just wants to search with name then they can just give name field and the command internally searches the deployment 
    with given name and deletes it.""")
def delete_deployment(client: Client):
    """This function is executed on command "safebreach-delete-deployment"

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,dict: deleted deployment data as a table and a dictionary
    """
    deleted_deployment = client.delete_deployment()

    human_readable = tableToMarkdown(name="Deleted Deployment", t=deleted_deployment.get("data", {}),
                                     headerTransform=deployment_transformer,
                                     headers=['id', "accountId", 'name', 'createdAt',
                                              "description", "nodes", "updatedAt"])
    outputs = deleted_deployment.get("data", {})
    demisto.info(f"json output for delete deployment is {outputs}")

    result = CommandResults(
        outputs_prefix="deleted_deployment_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-generate-api-key",
    inputs_list=[
        InputArgument(name="name", required=True, is_array=False,
                      description="""
                      Name of the API Key to create. This will be the name shown in UI for API key under API keys section
                      """,),
        InputArgument(name="description", required=False, is_array=False, description="""
                      Description of the API Key to create. This is not a required field but it is recommended to store a 
                      description for easier identification if your use case requires using multiple API keys for multiple tasks.
                      """),
    ],
    outputs_prefix="generated_api_key",
    outputs_list=[
        OutputArgument(name="name", prefix="generated_api_key", output_type=int,
                       description="The Name of API Key generated through this command, \
                           This will match the input name of the command.",),
        OutputArgument(name="description", prefix="generated_api_key", output_type=str,
                       description="The Description of API Key created. \
                           this will be same as input description given for the command."),
        OutputArgument(name="createdBy", prefix="generated_api_key", output_type=str,
                       description="The id of user who generated this API key."),
        OutputArgument(name="createdAt", prefix="generated_api_key", output_type=str,
                       description="The creation date and time of API key."),
        OutputArgument(name="key", prefix="generated_api_key", output_type=str,
                       description="The value of API key generated. store this for further use as this will only be shown once"),
        OutputArgument(name="roles", prefix="generated_api_key", output_type=str,
                       description="The roles allowed for this api key. \
                           This will generally be the roles assigned to user who created the key."),
        OutputArgument(name="role", description="The role of API Key.", prefix="generated_api_key",
                       output_type=str),
    ],
    description="""
    This command creates a API Key with given data. The API key created will be shown in API keys section 
    of safebreach UI with name and description as given in input fields "name" and "description". Name is a required value
    but description isn't, The API key generated can be seen only once, so it is recommended to store/save it for further use.
    """)
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
    demisto.info(f"json output for create API key is {outputs}")

    result = CommandResults(
        outputs_prefix="generated_api_key",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-delete-api-key",
    inputs_list=[
        InputArgument(name="key_name", required=True, is_array=False, description="""
                      Name of the API Key to Delete. This will be used for searching key with given name
                      and then once it matches, that API key will be deleted
                      """),
    ],
    outputs_prefix="deleted_api_key",
    outputs_list=[
        OutputArgument(name="name", description="The Name of API Key deleted.", prefix="deleted_api_key", output_type=int),
        OutputArgument(name="description", description="Description of API Key deleted.", prefix="deleted_api_key",
                       output_type=str),
        OutputArgument(name="createdBy", description="The id of user who generated this API key.", prefix="deleted_api_key",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time and date of API key.", prefix="deleted_api_key",
                       output_type=str),
        OutputArgument(name="deletedAt", prefix="deleted_api_key", output_type=str,
                       description="The deletion time and date of API key. The deletion date and time are generally\
                       close to the command execution time and date."),
    ],
    description="""
    This command deletes a API key with given name. When given an input key name, it will internally retrieve all
    active keys and then delete the one with name matching the name entered, the match is not case sensitive match
    but its exact word match so please enter key name exactly as shown in UI to delete it.
    """)
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
    demisto.info(f"json output for delete api key is {outputs}")

    result = CommandResults(
        outputs_prefix="deleted_api_key",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def integration_issues_transformer(header):
    return_map = {
        "connector": "integration_id",
        "action": "action",
        "success": "success_state",
        "error": "error_description",
        "timestamp": "timestamp"
    }
    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-get-integration-issues",
    inputs_list=None,
    outputs_prefix="integration_errors",
    outputs_list=[
        OutputArgument(name="integration_id", prefix="integration_errors", output_type=int,
                       description="The connector ID of Integration connector. A general notation that has been followed here is\
                       as follows, if the  id has _default at the end then its a default connector else its a custom connector",),
        OutputArgument(name="action", prefix="integration_errors", output_type=str,
                       description="The action of Integration connector error. This describes where exactly did the error occur,\
                        if its search,then it implies error/warning happened when connector was trying that process",),
        OutputArgument(name="success_state", prefix="integration_errors", output_type=str,
                       description="status of connector error. This implies whether the connector was able to \
                       successfully perform the operation or if it failed partway. \
                       So false implies it failed partway and true implies it was successfully completed"),
        OutputArgument(name="error_description", prefix="integration_errors", output_type=str,
                       description="This is the exact error description shown on safebreach connector error/warning page.\
                        This description can be used for understanding of what exactly happened for the connector to fail."),
        OutputArgument(name="timestamp", prefix="integration_errors", output_type=str,
                       description="Time at which error/warning occurred. This can be used to pinpoint error which occurred\
                       across connectors if time of origin was remembered",),
    ],
    description="""
    This command gives all connector related issues and warning. this will show the connector error and warnings which are 
    generally displayed in installed integrations page.
    """)
def get_all_integration_error_logs(client: Client):
    """This function retrieves all error logs and shows them in form of table

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,Dict: This function returns all errors along with connector details in a table and we get data as json
    """
    formatted_error_logs = []
    error_logs = client.get_all_integration_error_logs()
    demisto.info(f"integration logs are {len(error_logs.get('result'))}")

    formatted_error_logs = client.flatten_error_logs_for_table_view(error_logs.get("result"))
    human_readable = tableToMarkdown(
        name="Integration Connector errors",
        headerTransform=integration_issues_transformer,
        t=formatted_error_logs,
        headers=["connector", "action", "success", "error", "timestamp"])
    outputs = error_logs.get("result")
    demisto.info(f"json output for get_all_integration_logs is {outputs}")

    result = CommandResults(
        outputs_prefix="Integration Error Data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-delete-integration-issues",
    inputs_list=[
        InputArgument(name="integration_id", required=True, is_array=False,
                      description="""
                      The connector ID of Integration to have its errors/warnings deleted. this is used to search for integration 
                      connector which will have its logs cleared, there is no way to clear just errors or just warnings here and 
                      this connector with this will be having all errors and warnings cleared.
                      """,),
    ],
    outputs_prefix="errors_cleared",
    outputs_list=[
        OutputArgument(name="error", description="Error count after deletion of errors for the given connector.",
                       prefix="integration_errors", output_type=int),
        OutputArgument(name="result", description="error deletion status whether true or false.",
                       prefix="integration_errors", output_type=str),
    ],
    description="""
    This command deletes connector related errors and warnings. This command needs connector id as input which will be
    used to delete the errors/warnings for the given connector id. the connector ids can be retrieved by using command
    get-all-integration-issues and this command will give connector id which can be used for input. 
    """)
def delete_integration_error_logs(client: Client):
    """This function deletes integration errors of a given connector

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,Dict: This returns a table of data showing deleted details and dict showing same in outputs
    """
    error_logs = client.delete_integration_error_logs()
    headers = ["result", "error"]
    if error_logs.get("errorMessage"):
        # should we throw a connector not found here or just show it as success saying no connector found
        headers = ["error", "errorMessage"]
    human_readable = tableToMarkdown(
        name="Integration Connector errors status",
        t=error_logs,
        headers=headers)
    outputs = error_logs
    demisto.info(f"json output for delete integration error logs is {outputs}")

    result = CommandResults(
        outputs_prefix="errors_cleared",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def simulator_count_transformer(header):
    return_map = {
        "contactName": "contact_name",
        "contactEmail": "contact_email",
        "userQuota": "user_quota",
        "nodesQuota": "simulator_quota",
        "registrationDate": "registration_date",
        "activationDate": "activation_date",
        "expirationDate": "expiration_date",
    }
    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-get-available-simulator-count",
    inputs_list=None,
    outputs_prefix="account_details",
    outputs_list=[
        OutputArgument(name="id", prefix="account_details", output_type=int,
                       description="The account ID which is being used by integration."),
        OutputArgument(name="name", description="The Account Name of account being queried.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="contact_name", description="Contact name for given account.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="contact_email", description="Email of the contact person.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="user_quota", prefix="account_details", output_type=str,
                       description="User Quota for the given account, maximum users which are allowed for the account."),
        OutputArgument(name="simulators_quota", prefix="account_details", output_type=int,
                       description="The simulator quota for the given account. the maximum number of simulators \
                       which are permitted for the account."),
        OutputArgument(name="registration_date", description="The registration date of given account.",
                       prefix="account_details", output_type=int),
        OutputArgument(name="activation_date", description="The Activation date of given account.",
                       prefix="account_details", output_type=str),
        OutputArgument(name="expiration_date", description="Account expiration date.",
                       prefix="account_details", output_type=str),
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
        headerTransform=simulator_count_transformer,
        headers=["id", "name", "contactName", "contactEmail", "userQuota", "nodesQuota", "registrationDate",
                 "activationDate", "expirationDate"])
    outputs = {
        'account_details': simulator_details.get("data"),
        "simulator_quota": simulator_details.get("data").get("nodesQuota")
    }
    demisto.info(f"json output for get_simulator_quota is {outputs}")

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
    description="""
    This command to get all available simulators. if details is set to true then it retrieves simulator details like name, 
    hostname, internal and external ips, types of targets and attacker configurations this simulator is associated with etc.
    if its set to false then it retrieves just name, id, simulation users, proxies etc. if deleted is set to true then it
    retrieves the data which has been deleted
    """)
def get_all_simulator_details(client: Client):
    """This function returns simulator details of all simulators

    Args:
        client (Client): Client class for API calls

    Returns:
        List(dict): This is list of all simulators data
    """
    return get_simulators_and_display_in_table(client=client)


@metadata_collector.command(
    command_name="safebreach-get-simulator-with-id",
    inputs_list=[
        InputArgument(name="simulator_id", required=True, is_array=False,
                      description="This is simulator ID of simulator we want to search")
    ],
    outputs_prefix="simulator_details_with_id",
    outputs_list=simulators_output_fields,
    description="This command gives simulator with given name")
def get_simulator_with_name(client: Client):
    """this function returns simulator with given name as  table and dict

    Args:
        client (Client): Client class for API calls

    Returns:
        CommandResults,data: This is data of simulator with given name
    """
    return get_specific_simulator_details(client=client)


@metadata_collector.command(
    command_name="safebreach-delete-simulator",
    inputs_list=[
        InputArgument(name="simulator_id", required=True, is_array=False,
                      description="Id of the simulator we want to delete")],
    outputs_prefix="deleted_simulator_details",
    outputs_list=simulators_output_fields,
    description="This command deletes simulator with given ID.to get simulator_id use safebreach-get-all-simulators command")
def delete_simulator_with_given_name(client: Client):
    """This function deletes simulator with given id

    Args:
        client (Client): This is client class for API calls

    Returns:
        CommandResults,Dict: this is for table showing deleted simulator data and dict with data
    """
    deleted_simulator = client.delete_simulator_with_given_name()

    flattened_simulators, keys = client.flatten_simulator_details([deleted_simulator.get("data", {})])
    human_readable = tableToMarkdown(
        name="Deleted Simulators Details",
        t=flattened_simulators,
        headers=keys)
    outputs = deleted_simulator.get("data", {})
    demisto.info(f"json output of delete simulator with given name is {outputs}")

    result = CommandResults(
        outputs_prefix="deleted_simulator_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-update-simulator",
    inputs_list=[
        InputArgument(name="simulator_id", required=True, is_array=False, description="""
                      simulator id tells which simulator are we updating, if you want to know the simulator id 
                      with given name then run safebreach-get-all-simulator-details command.
                      """)
    ] + simulator_details_for_update_fields,
    outputs_prefix="updated_simulator_details",
    outputs_list=simulators_output_fields,
    description="""
    This command updates simulator with given id. the given inputs for update
    fields will be updated to the selected filed values will be updated to given value.
    """)
def update_simulator(client: Client):
    """This function updates simulator with given data having name as given input

    Args:
        client (Client): This is client class for API calls

    Returns:
        CommandResults,Dict: This will return table and dict containing updated simulator data
    """
    updated_simulator = client.update_simulator()

    flattened_simulators, keys = client.flatten_simulator_details([updated_simulator.get("data", {})])
    human_readable = tableToMarkdown(
        name="Updated Simulators Details",
        t=flattened_simulators,
        headers=keys)
    outputs = updated_simulator.get("data", {})
    demisto.info(f"json output of update simulator with a given name is {outputs}")

    result = CommandResults(
        outputs_prefix="updated_simulator_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-approve-simulator",
    inputs_list=[
        InputArgument(name="simulator_id", required=True, is_array=False, description="""
                      ID of simulator to approve, incase unsure then please call safebreach-get-all-simulators
                      and search for simulator name.
                      """)
    ],
    outputs_prefix="approved_simulator_details",
    outputs_list=simulators_output_fields,
    description="""
    This command approves simulator with given name with given id.
    """)
def approve_simulator_with_given_name(client: Client):
    """This function approves simulator with given data having name as given input

    Args:
        client (Client): This is client class for API calls

    Returns:
        CommandResults,Dict: This will return table and dict containing approved simulator data
    """
    approved_simulator = client.approve_simulator_with_given_name()

    flattened_simulators, keys = client.flatten_simulator_details([approved_simulator.get("data", {})])
    human_readable = tableToMarkdown(
        name="Approved Simulators Details",
        t=flattened_simulators,
        headers=keys)
    outputs = approved_simulator.get("data", {})
    demisto.info(f"json output of approve simulator with a given name is {outputs}")

    result = CommandResults(
        outputs_prefix="approved_simulator_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-rotate-verification-token",
    inputs_list=None,
    outputs_list=[
        OutputArgument(name="new_token", output_type=str, description="new Token which has been generated due to the api call"),
    ],
    description="""
    This command rotates generated verification token meaning it creates a new token which will be used for verification 
    of simulator and adding the simulator.
    """)
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
        name="new Token Details",
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
    command_name="safebreach-get-tests",
    inputs_list=[
        InputArgument(name="include_archived", options=["true", "false"], default="false", required=False, is_array=False,
                      description="""
                      Should archived tests be included in search. Archived tests are tests which have been 
                      set aside for further use in an inactive state. if this is set to false then archived tests
                      wont be pulled but  if set to true then they will be pulled and shown.
                      """,
                      ),
        InputArgument(name="entries_per_page", required=False, is_array=False, description="""
                      number of entries to be retrieved. for viewing, this will work in combination with sort_by field and
                      things will be sorted in decreasing order so if you chose 100 entries here and if endTime is chosen as sort
                      then it will show last 100 executions with latest end time.
                      """),
        InputArgument(name="plan_id", required=False, is_array=False,
                      description="""
                      plan Id of test. this can be found on UI, if unsure about this then please run safebreach-get-tests 
                      instead of this with same parameters as inputs.
                      """),
        InputArgument(name="status", required=False, is_array=False, options=["CANCELED", "COMPLETED"],
                      description="tests with this status will be searched and filtered."),
        InputArgument(name="simulation_id", required=False, is_array=False, description="Unique ID of the simulation."),
        InputArgument(name="sort_by", required=False, is_array=False, options=["endTime", "startTime", "testID", "stepRunId"],
                      default="endTime", description="""
                      how to sort the results retrieved, there are 4 options:
                      1. sorting by endTime will show results in terms of decreasing order of simulations end time.
                      2. sorting by start time will show results in terms of the decreasing order of simulation start time.
                      3. testID - this is test id and sorting by this will be decreasing order of test id.
                      4. stepRunId -
                      """),
    ],
    outputs_prefix="test_results",
    outputs_list=test_summaries_output_fields,
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
    command_name="safebreach-get-test-with-plan-id",
    inputs_list=[
        InputArgument(name="plan_id", required=True, is_array=False,
                      description="""
                      plan Id of test. this can be found on UI, if unsure about this then please run safebreach-get-tests 
                      instead of this with same parameters as inputs.
                      """)
    ],
    outputs_prefix="test_results",
    outputs_list=test_summaries_output_fields,
    description="""
    This command gets tests with given plan ID and the order is based on sort by column.
    """)
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
    command_name="safebreach-delete-test-with-id",
    inputs_list=[
        InputArgument(name="test_id", description="test id of the test summary which we want to search the test with.",
                      required=False, is_array=False),
    ],
    outputs_prefix="deleted_test_results",
    outputs_list=test_summaries_output_fields,
    description="This command deletes tests with given test ID.")
def delete_test_result_of_test(client: Client):
    """This function deletes test with given Test ID

    Args:
        client (Client): Client class for API call

    Returns:
        CommandResults,Dict: A table showing deletion results and a dict of outputs showing the same
    """
    test_summaries = client.delete_test_result_of_test()
    demisto.info(f"output of delete_test_result_of_test is {test_summaries}")
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


@metadata_collector.command(
    command_name="safebreach-get-queued-running-tests",
    inputs_list=None,
    outputs_prefix="active_tests",
    outputs_list=tests_outputs,
    description="This command gets tests which are in running or queued state.")
def get_all_running_tests_summary(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    running_tests = client.get_active_tests()
    demisto.info(f"the get_all_running_tests_summary function gave response {running_tests}")

    flattened_running_tests_for_table = client.flatten_tests_data(running_tests.get("data", {}))
    human_readable = tableToMarkdown(
        name="Running Tests",
        t=flattened_running_tests_for_table,
        headerTransform=test_outputs_headers_transform,
        headers=test_outputs_headers_list)
    outputs = running_tests
    demisto.info(f"json output of get_all_running_tests_summary function gave response {running_tests}")

    result = CommandResults(
        outputs_prefix="tests_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


def simulations_output_transform(header):
    return_map = {
        "status": "status",
        "timestamp": "timestamp",
        "numOfTasks": "numOfTasks",
        "planRunId": "test id",
        "stepRunId": "stepRunId",
        "jobId": "jobId",
        "taskId": "taskId",
        "moveId": "moveId",
        "moveRevision": "moveRevision",
        "simulator_ids_involved": "simulator_ids_involved",
        "simulator_names_involved": "simulator_names_involved",
        "timeout": "timeout",
        "packageId": "packageId"
    }
    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-get-queued-running-simulations",
    inputs_list=None,
    outputs_prefix="active_simulations",
    outputs_list=[
        OutputArgument(name="status", description="the status of the simulation, if its running or queued.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="timestamp", description="the time at which simulation was triggered.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="numOfTasks", description="the number of tasks involved in the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="test id", description="this is test ID of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="stepRunId", description="the step id of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="jobId", description="the job id of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="taskId", description="the task ID of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="moveId", description="the move ID of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="moveRevision", description="the move revision of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="simulator_ids_involved", description="the simulators involved in the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="simulator_names_involved", description="the names of simulators the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="timeout", description="the timeout of the simulation if its failing etc.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="packageId", description="the package ID of the simulation.",
                       prefix="active_tests", output_type=str),
    ],
    description="This command gets simulations which are in running or queued state.")
def get_all_running_simulations_summary(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    running_simulations = client.get_active_simulations()
    flattened_simulations_data_for_table = client.flatten_simulations_data(running_simulations.get("data", {}))
    demisto.info(f"the get_all_running_simulations_summary function gave response {running_simulations}")
    human_readable = tableToMarkdown(
        name="Running Simulations",
        t=flattened_simulations_data_for_table,
        headerTransform=simulations_output_transform,
        headers=[
            "status", "timestamp", "numOfTasks", "planRunId", "stepRunId", "jobId", "taskId", "moveId",
            "moveRevision", "simulator_ids_involved", "simulator_names_involved", "timeout", "packageId",
        ])

    outputs = running_simulations
    demisto.info(f"json output for get_all_running_simulations_summary is {running_simulations}")
    result = CommandResults(
        outputs_prefix="active_simulations",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-pause-resume-simulations-tests",
    inputs_list=[
        InputArgument(name="simulation_or_test_state", options=["resume", "pause"], required=True, is_array=False,
                      description="""State of tests/simulators to set to:
                       1. pause will set all simulations/tests which are in queue/running to paused stated and resume all 
                       will be the state of button in running simulations page.
                       2. resume will queue all simulations/tests and will set them to running/queued state depending on priority.
                       Note that this doe not affect the schedules and scheduled tasks unless they are running or active at the
                       moment of execution of the command.
                       """
                      )],
    outputs_prefix="simulations_tests_status",
    outputs_list=[
        OutputArgument(name="status", prefix="simulations_tests_status", output_type=str,
                       description="the status of the simulations/tests.",)
    ],
    description="""
    This command gets simulations/tests which are in running or queued state and pauses/resumes them based on input selected.
    the state selected will be applied for all running/queued state tasks whether they are simulations or tests.
    """)
def pause_resume_tests_and_simulations(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    simulations_status = client.set_simulations_status()
    human_readable = tableToMarkdown(
        name="Simulations/tests status",
        t=simulations_status.get("data"),
        headers=["status"])

    outputs = simulations_status
    result = CommandResults(
        outputs_prefix="simulations_tests_status",
        outputs=outputs.get("data"),
        readable_output=human_readable
    )

    return result


def safebreach_schedules_transformer(header):
    return_map = {
        "id": "id",
        "isEnabled": "isEnabled",
        "name": "name",
        "user_schedule": "user_schedule",
        "runDate": "runDate",
        "cronTimezone": "cronTimezone",
        "taskId": "taskId",
        "description": "description",
        "matrixId": "plan_id",
        "createdAt": "createdAt",
        "updatedAt": "updatedAt",
        "deletedAt": "deletedAt"
    }

    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-get-schedules",
    inputs_list=None,
    outputs_prefix="schedules",
    outputs_list=[
        OutputArgument(name="id", description="the Id of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="isEnabled", description="if simulation is enabled.",
                       prefix="schedules", output_type=bool),
        # OutputArgument(name="name", description="the name of the schedule.",
        #                prefix="schedules", output_type=str),
        # OutputArgument(name="cronString", description="the cron expression the schedule.",
        #                prefix="schedules", output_type=str),
        OutputArgument(name="user_schedule", description="the user readable form of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="runDate", description="the run date of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="cronTimezone", description="the time zone of the schedule.",
                       prefix="planId", output_type=str),
        # OutputArgument(name="taskId", description="the plan ID of the schedule.",
        #                prefix="schedules", output_type=str),
        OutputArgument(name="description", description="the description of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="plan_id", description="the matrix ID of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="createdAt", description="the creation datetime of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="updatedAt", description="the updated datetime of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="deletedAt", description="the deletion time of the schedule.",
                       prefix="schedules", output_type=str),
    ],
    description="This command retrieves schedules from safebreach which user has set and they will display it to user")
def get_schedules(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    headers = ["id", "isEnabled", "user_schedule", "runDate",
               "cronTimezone", "description", "matrixId",
               "createdAt", "updatedAt", "deletedAt"
               ]

    schedules_data = client.get_schedules()
    new_schedules_data = client.append_cron_to_schedule(deepcopy(schedules_data.get("data")))
    demisto.info(f"the get_schedules function gave response {schedules_data}")
    human_readable = tableToMarkdown(
        name="Schedules",
        headerTransform=safebreach_schedules_transformer,
        t=new_schedules_data,
        headers=headers)

    outputs = schedules_data.get("data")
    result = CommandResults(
        outputs_prefix="schedules",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-delete-schedule",
    inputs_list=[
        InputArgument(name="schedule_id", description="schedule ID of schedule to delete",
                      required=True, is_array=False)
    ],
    outputs_prefix="deleted_Schedule",
    outputs_list=[
        OutputArgument(name="id", description="the Id of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="isEnabled", description="if schedule is enabled.",
                       prefix="deleted_Schedule", output_type=bool),
        # OutputArgument(name="name", description="the name of the schedule.",
        #                prefix="deleted_Schedule", output_type=str),
        # OutputArgument(name="cronString", description="the cron expression the schedule.",
        #                prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="user_schedule", description="the user readable form of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="runDate", description="the run date of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="cronTimezone", description="the time zone of the schedule.",
                       prefix="planId", output_type=str),
        # OutputArgument(name="taskId", description="the plan ID of the schedule.",
        #                prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="description", description="the description of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="plan_id", description="the plan ID of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="createdAt", description="the creation datetime of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="updatedAt", description="the updated datetime of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="deletedAt", description="the deletion time of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
    ],
    description="This command gets simulations which are in running or queued state.")
def delete_schedules(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    headers = ["id", "isEnabled", "user_schedule", "runDate",
               "cronTimezone", "description", "matrixId",
               "createdAt", "updatedAt", "deletedAt"
               ]

    schedules_data = client.delete_schedule()
    demisto.info(f"the delete_schedules function with id {demisto.args().get('schedule_id')} gave response {schedules_data}")

    new_schedules_data = client.append_cron_to_schedule([deepcopy(schedules_data.get("data"))])
    human_readable = tableToMarkdown(
        name="Deleted Schedule",
        headerTransform=safebreach_schedules_transformer,
        t=new_schedules_data,
        headers=headers)

    outputs = schedules_data
    result = CommandResults(
        outputs_prefix="deleted_Schedule",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-prebuilt-scenarios",
    inputs_list=None,
    outputs_prefix="prebuilt_scenarios",
    outputs_list=[
        OutputArgument(name="id", description="the Id of scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="name", description="the name of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="description", description="the description of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="createdBy", description="user id of user, who created the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="createdAt", description="creation datetime of scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="updatedAt", description="the update datetime of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="recommended", prefix="prebuilt_scenarios", output_type=str,
                       description="the recommendation status of the scenario.",),
        OutputArgument(name="tags_list", description="the tags related to the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="categories", description="the category ids of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="steps_order", description="the order of steps involved in the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="order", description="the order of execution related to the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="minApiVer", description="the minimum version of API required for scenario to be executed",
                       prefix="prebuilt_scenarios", output_type=str)
    ],
    description="""
    This command gets scenarios which are built by safebreach. They will be available by default even in new instance
    of your safebreach instance. They can be modified and saved as custom scenarios or used as it is.
    """)
def get_prebuilt_scenarios(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    prebuilt_scenarios = client.get_prebuilt_scenarios()
    demisto.info(f"output of get_prebuilt_scenarios function call is {prebuilt_scenarios}")

    flattened_simulations_data_for_table = client.extract_default_scenario_fields(prebuilt_scenarios)
    human_readable = tableToMarkdown(
        name="Scenarios",
        t=flattened_simulations_data_for_table,
        headers=[
            "id", "name", "description", "createdBy", "createdAt", "updatedAt", "recommended",
            "tags_list", "categories", "steps_order", "order", "minApiVer"
        ])

    demisto.info(f"json output for get_prebuilt_scenarios function is {prebuilt_scenarios}")
    outputs = prebuilt_scenarios
    result = CommandResults(
        outputs_prefix="prebuilt_scenarios",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-custom-scenarios",
    inputs_list=[
        InputArgument(name="schedule_details", default="true", options=["false", "true"], required=False, is_array=False,
                      description="""
                      Whether to get details of custom scenarios, 
                      set this to true every time unless you explicitly dont need details
                      """),
    ],
    outputs_prefix="custom_scenarios",
    outputs_list=[
        OutputArgument(name="id", description="the Id of scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="name", description="the name of the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="description", description="the description of the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="successCriteria", description="success criteria the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="originalScenarioId", description="original scenario id of scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="actions_list", description="actions list of the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="edges_count", description="edges count for the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="steps_order", description="the order of steps of the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="createdAt", description="the creation datetime of the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="updatedAt", description="the last updated time the scenario.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="custom_data_object_for_rerun_simulation", description="the data which can be used for \
            rerun-simulation command.", prefix="custom_scenarios", output_type=str),
        OutputArgument(name="custom_data_for_rerun_test", description="the data which can be used for rerun-test command.",
                       prefix="custom_scenarios", output_type=str),
    ],
    description="""
    This command  retrieves scenarios which are saved by user as custom scenarios. they generally have configurations and 
    everything set up and will be ready to run as tests. this command can be used to chain as predecessor for safebreach-
    requeue-test-simulation command and use the test-id parameter for requeuing the given test.
    """)
def get_custom_scenarios(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    custom_scenarios = client.get_custom_scenarios()
    demisto.info(f"output of get_custom_scenarios function for command {demisto.command()} with details input \
        {demisto.args().get('schedule_details')} is {custom_scenarios}")

    if demisto.args().get("schedule_details") == "true":
        flattened_simulations_data_for_table = client.extract_custom_scenario_fields(custom_scenarios.get("data", {}))
    else:
        flattened_simulations_data_for_table = custom_scenarios.get("data", {})

    human_readable = tableToMarkdown(
        name="Scenarios",
        t=flattened_simulations_data_for_table,
        headers=["id", "name", "description", "successCriteria", "originalScenarioId",
                 "actions_list", "edges_count", "steps_order", "createdAt", "updatedAt",
                 "custom_data_object_for_rerun_simulation"])

    demisto.info(f"json output of custom scenarios call is {custom_scenarios}")
    outputs = custom_scenarios
    result = CommandResults(
        outputs_prefix="custom_scenarios",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-services-status",
    inputs_list=None,
    outputs_prefix="services_status",
    outputs_list=[
        OutputArgument(name="name", description="the name of the service.",
                       prefix="services_status", output_type=str),
        OutputArgument(name="version", description="version of the service.",
                       prefix="services_status", output_type=str),
        OutputArgument(name="connection status", description="connection status of service.",
                       prefix="services_status", output_type=str),
        OutputArgument(name="error", description="error status of service.",
                       prefix="services_status", output_type=str),
    ],
    description="""
    This command retrieves status of services from safebreach and shows them as table for user, incase they are down then
    from when they are down or when it was last up will also be shown here.
    """)
def get_services_status(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    services = client.get_services_status()
    demisto.info(f"result of services API call is {services}")

    modified_services_data = client.format_services_response(services)
    human_readable = tableToMarkdown(
        name="Services",
        t=modified_services_data,
        headers=["name", "version", "connection_status"])
    demisto.info(f"json output of services API call is {modified_services_data}")

    outputs = services
    result = CommandResults(
        outputs_prefix="services_status",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def simulations_transformer(header):
    return_map = {
        "planName": "plan_name",
        "attackerNodeName": "attacker_node_name",
        "id": "simulation_id",
        "finalStatus": "final_status",
        "resultDetails": "result_details",
        "securityAction": "security_action",
        "targetNodeName": "target_node_name",
        "moveDesc": "move_description",
        "attacks_involved": "attacks_involved"
    }

    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-get-simulation-results",
    inputs_list=[
        InputArgument(name="test_id", required=False, is_array=False,
                      description="This is test of of the test whose simulations we will retrieve with this command.",),
    ],
    outputs_prefix="simulation_details",
    outputs_list=[
        OutputArgument(name="simulation_id", description="the id of the simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="plan_name", description="name of the plan to which this simulation belongs to.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="attacker_node_name", description="Name of attacker node of simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="target_node_name", description="name of target of simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="dest_node_name", description="name of destination of simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="status", description="final status of simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="result", description="result of simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="security_action", description="security action of simulation.",
                       prefix="simulation_details", output_type=str),
        OutputArgument(name="attacks_involved", description="attack types involved in of simulation.",
                       prefix="simulation_details", output_type=str),
        # OutputArgument(name="move_description", description="moves involved in of simulation.",
        #                prefix="simulation_details", output_type=str),
    ],
    description="""
    this command is used to get simulations and their data related to a given test, 
    this can be used as predecessor command to rerun-simulations command for easier queueing of simulations.
    This command does not have any limiters with pagination implemented so there might be huge data retrieved.
    """)
def get_simulations(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """

    headers = ["planName", "attackerNodeName", "id", "finalStatus",
               "resultDetails", "securityAction", "targetNodeName", "attacks_involved"]
    simulations = client.get_simulations()
    demisto.info(f"result of simulations API call is {simulations}")
    modified_simulations_data = format_simulations_data(simulations.get("simulations"))
    human_readable = tableToMarkdown(
        name="Simulations Details for test",
        t=modified_simulations_data,
        headerTransform=simulations_transformer,
        headers=headers)
    demisto.info(f"json output of simulations API call is {modified_simulations_data}")

    outputs = simulations
    result = CommandResults(
        outputs_prefix="simulation_details",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-get-verification-token",
    inputs_list=None,
    outputs_prefix="verification_token",
    outputs_list=[
        OutputArgument(name="token", description="the value of new verification token.",
                       prefix="verification_token", output_type=str),
    ],
    description="""
    This command retrieves existing verification token needed for verification of the simulators.
    """)
def get_verification_token(client):
    token_data = client.get_verification_token()
    demisto.info(f"output of get_verification_token function for command {demisto.command()} is {token_data}")
    human_readable = tableToMarkdown(
        name="Verification Token",
        t=token_data.get("data"),
        headers=["secret"])

    outputs = token_data
    result = CommandResults(
        outputs_prefix="verification_token",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


def tests_scenarios_transformer(header):
    return_map = {
        "name": "name",
        "originalScenarioId": "originalScenarioId",
        "actions_list": "actions_list",
        "edges_count": "edges_count",
        "steps_order": "steps_order",
        "planRunId": "test_id",
        "ranBy": "ranBy",
        "ranFrom": "ranFrom",
        "enableFeedbackLoop": "enableFeedbackLoop",
        "priority": "priority",
        "retrySimulations": "retrySimulations",
    }
    return return_map.get(header, header)


@metadata_collector.command(
    command_name="safebreach-rerun-test",
    inputs_list=[
        InputArgument(name="position", description="position in queue to put the given test data at.",
                      required=False, is_array=False),
        InputArgument(name="enable_feedback_loop", description="this argument is used to enable/disable feedback loop",
                      default="true", options=["false", "true"], required=False, is_array=False),
        InputArgument(name="retry_simulation", default="", options=["", "false", "true"], required=False, is_array=False,
                      description="this argument is used to retry according to retry policy \
                mention in retry policy field",),
        InputArgument(name="wait_for_retry", description="this arguments tells flow to retry the adding to queue after the \
                current step execution is completed", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="priority", description="the priority of this test action",
                      default="low", options=["low", "high"], required=False, is_array=False),
        InputArgument(name="retry_policy", required=False, is_array=False, description="""
                      the retry policy of test 
                      """,),
        InputArgument(name="test_id", description="test id for the given test, \
            this is be planRunId field from get-all-tests-summary command", required=True, is_array=False),
        InputArgument(name="test_name", description="test name for the given test",
                      required=True, is_array=False),
    ],
    outputs_prefix="changed_data",
    outputs_list=[
        OutputArgument(name="id", description="the Id of scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="name", description="the name of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="description", description="the description of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="successCriteria", description="success criteria the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="originalScenarioId", description="original scenario id of scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="actions_list", description="actions list of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="edges_count", description="edges count for the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="steps_order", description="the order of steps of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="createdAt", description="the creation datetime of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="updatedAt", description="the last updated time the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="planId", description="the plan id of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="ranBy", description="the user id of the user who ran the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="ranFrom", description="where the user ran the scenario from.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="enableFeedbackLoop", description="feedback loop status of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="planRunId", description="plan run id of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="priority", description="priority of the scenario.",
                       prefix="changed_data", output_type=str),
        OutputArgument(name="retrySimulations", description="retry status of the scenario.",
                       prefix="changed_data", output_type=str),
    ],
    description="this commands puts given test data at a given position, for this command to get test data input,\
        run safebreach-custom-scenarios-list and copy field 'data for rerun test' from table ")
def rerun_test(client):

    rerun_results = client.rerun_test_or_simulation()
    demisto.info(f"output of rerun_test function for command {demisto.command()} is {rerun_results}")

    flattened_simulations_data_for_table = client.extract_test_fields(rerun_results.get("data", {}))
    human_readable = tableToMarkdown(
        name="test",
        headerTransform=tests_scenarios_transformer,
        t=flattened_simulations_data_for_table,
        headers=["name", "originalScenarioId", "actions_list", "edges_count", "steps_order",
                 "planRunId", "ranBy", "ranFrom", "enableFeedbackLoop", "planRunId", "priority", "retrySimulations"])
    demisto.info(f"json output of rerun_test is {flattened_simulations_data_for_table}")

    outputs = rerun_results
    result = CommandResults(
        outputs_prefix="changed_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


@metadata_collector.command(
    command_name="safebreach-rerun-simulation",
    inputs_list=[
        InputArgument(name="position", description="position in queue to put the given simulation data at.",
                      required=False, is_array=False),
        InputArgument(name="enable_feedback_loop", description="this argument is used to enable/disable feedback loop",
                      default="true", options=["false", "true"], required=False, is_array=False),
        InputArgument(name="retry_simulation", description="this argument is used to retry according to retry policy \
                mention in retry policy field", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="wait_for_retry", description="this arguments tells flow to retry the adding to queue after the \
                current step execution is completed", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="priority", description="the priority of this simulation action",
                      default="low", options=["low", "high"], required=False, is_array=False),
        InputArgument(name="simulation_name", description="simulation name for the given simulation",
                      required=True, is_array=False),
        InputArgument(name="simulation_ids", required=True, is_array=False,
                      description="ids of simulation we want to queue,\
                          please give ids of simulations as comma separated numbers",),
    ],
    outputs_prefix="changed_data",
    outputs_list=[
        OutputArgument(name="id", description="the Id of simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="name", description="the name of the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="description", description="the description of the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="successCriteria", description="success criteria the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="originalScenarioId", description="original simulation id of simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="actions_list", description="actions list of the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="edges_count", description="edges count for the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="steps_order", description="the order of steps of the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="createdAt", description="the creation datetime of the simulation.",
                       prefix="custom_scenarios", output_type=str),
        OutputArgument(name="updatedAt", description="the last updated time the simulation.",
                       prefix="custom_scenarios", output_type=str),
    ],
    description="this commands puts given simulation data at a given position, for this command to get test data input,\
        run safebreach-custom-scenarios-list and copy field 'data for rerun simulation' from table ")
def rerun_simulation(client):

    rerun_results = client.rerun_test_or_simulation()
    demisto.info(f"output of rerun_simulation function for command {demisto.command()} is {rerun_results}")
    flattened_simulations_data_for_table = client.extract_custom_scenario_fields([rerun_results.get("data", {})])
    human_readable = tableToMarkdown(
        name="Scenarios",
        headerTransform=tests_scenarios_transformer,
        t=flattened_simulations_data_for_table,
        headers=["name", "actions_list", "edges_count", "steps_order", "ranBy", "ranFrom",
                 "enableFeedbackLoop", "planRunId", "priority", "retrySimulations"])
    demisto.info(f"json output of services rerun_simulation call is {flattened_simulations_data_for_table}")
    outputs = rerun_results
    result = CommandResults(
        outputs_prefix="changed_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


class CronString:

    def __init__(self, cron_string, time_zone):
        self.cron_string = cron_string
        self.final_string = ""
        self.time_zone = time_zone or "UTC"
        self.parse()

    def parse(self):
        comp_array = self.cron_string.split(" ")
        self.parse_hours_and_minutes(comp_array[0], comp_array[1])
        if comp_array[2] != "*":
            self.parse_days_of_month(comp_array[2])
        elif comp_array[-1] != "*":
            self.parse_day_of_week(comp_array[-1])
        else:
            self.final_string += "every day"

    def parse_hours_and_minutes(self, minutes, hours):
        self.final_string += f"At {hours} hours and {minutes} minutes "

    def parse_days_of_month(self, days_of_month):
        days = days_of_month.split(",")
        days_list = []
        for days_range in days:
            if "-" in days_range:
                days_present = days_range.split("-")
                days_list += list(map(str, range(int(days_present[0]), int(days_present[1]))))
            else:
                days_list.append(days_range)
        if days_list:
            self.final_string += f"on days {', '.join(days_list)} every month"

    def parse_day_of_week(self, days_of_week):
        days = days_of_week.split(",")
        days_list = []
        for days_range in days:
            if "-" in days_range:
                days_present = days_range.split("-")
                days_list += list(map(str, range(int(days_present[0]), int(days_present[1]))))
            else:
                days_list.append(days_range)
        if days_list:
            self.final_string += f"on days {', '.join(days_list)} every week"

    def __str__(self):
        return self.final_string + "."

    def to_string(self):
        return f"{self.final_string} on timezone {self.time_zone}."


def main() -> None:
    """
    Execution starts here
    """
    client = Client(
        api_key=demisto.params().get("api_key"),
        account_id=demisto.params().get("account_id"),
        base_url=demisto.params().get("base_url"),
        verify=demisto.params().get("verify"),
        proxy=demisto.params().get("proxy"))
    demisto.debug(f'Command being called is {demisto.command()}')
    try:

        if demisto.command() == 'test-module':
            # This is the call made when pressing the integration Test button.
            result = client.get_all_users_for_test()
            return_results(result)

        elif demisto.command() == "safebreach-get-services-status":
            result = get_services_status(client=client)
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

        elif demisto.command() == "safebreach-get-integration-issues":
            result = get_all_integration_error_logs(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-integration-issues":
            result = delete_integration_error_logs(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-available-simulator-count":
            result = get_simulator_quota_with_table(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-available-simulator-details":
            result = get_all_simulator_details(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-simulator-with-id":
            result = get_simulator_with_name(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-simulator":
            result = delete_simulator_with_given_name(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-update-simulator":
            result = update_simulator(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-verification-token":
            result = get_verification_token(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-rotate-verification-token":
            result = return_rotated_verification_token(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-tests":
            result = get_all_tests_summary(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-test-with-plan-id":
            result = get_all_tests_summary_with_plan_id(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-test-with-id":
            result = delete_test_result_of_test(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-queued-running-tests":
            result = get_all_running_tests_summary(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-queued-running-simulations":
            result = get_all_running_simulations_summary(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-pause-resume-simulations-tests":
            result = pause_resume_tests_and_simulations(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-schedules":
            result = get_schedules(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-schedule":
            result = delete_schedules(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-prebuilt-scenarios":
            result = get_prebuilt_scenarios(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-custom-scenarios":
            result = get_custom_scenarios(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-approve-simulator":
            result = approve_simulator_with_given_name(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-rerun-test":
            result = rerun_test(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-rerun-simulation":
            result = rerun_simulation(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-simulation-results":
            result = get_simulations(client=client)
            return_results(result)

    except Exception as error:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(error)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
