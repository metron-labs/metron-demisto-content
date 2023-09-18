import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401
from copy import deepcopy
from functools import reduce

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

bool_map = {
    "true": True,
    "false": False,
    "True": True,
    "False": False
}

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
    OutputArgument(name="planRunId", description="plan run id.", output_type=str),
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


class Client(BaseClient):
    """
        Client class to interact with the service API

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
        """
            This function handles actual API call throughout the integration

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
        """
            This function handles errors related to SBcodes if the endpoint gives sbcode in errors

        Args:
            response (dict): all errors given by 400 response code will be accepted as dictionary and are formatted based on 
            the state of error

        Raises:
            Exception: all errors will be formatted and then thrown as exception string which will show as error_results in XSOAR
        """
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
                        return_obj['node_ids_involved'] = ""
                        return_obj["node_names_involved"] = ""
                        for object in data["actions"]:
                            return_obj['node_ids_involved'] = f"{return_obj['node_ids_involved']} ; {object['nodeId']}"
                            return_obj['node_names_involved'] = f"{return_obj['node_names_involved']} \
                                ; {object.get('nodeNameInMove','') or object.get('nodeNameInMoveDescription','')}"
                    else:
                        return_obj[key] = data[key]
                return_list.append(return_obj)

        return return_list

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
            "status": demisto.args().get("Simulation/Test State")
        }
        simulations_details = self.get_response(url=url, method=method, body=data)
        return simulations_details

    def get_schedules(self):
        account_id = demisto.params().get("account_id", 0)

        method = "GET"
        url = f"/config/v1/accounts/{account_id}/schedules"
        request_params = {
            "details": demisto.args().get("details"),
            "deleted": demisto.args().get("deleted")
        }
        schedule_data = self.get_response(url=url, method=method, request_params=request_params)
        return schedule_data

    def delete_schedule(self):
        account_id = demisto.params().get("account_id", 0)
        schedule_id = demisto.args().get("schedule ID")

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
                    steps_involved = ""
                    return_obj["steps_order"] = reduce(
                        lambda steps_involved, step: f"{steps_involved}, {step.get('name')}", scenario[key], steps_involved)
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
                    actions_involved = ""
                    return_obj["actions_list"] = reduce(
                        lambda actions_involved, action: f"""{actions_involved}, {action.get('type')}\
                            with identity:{action.get('data',{}).get('uuid','') or action.get('data',{}).get('id','')}""",
                        scenario[key], actions_involved)
                elif key == "steps" and scenario[key]:
                    steps_involved = ""
                    return_obj["steps_order"] = reduce(
                        lambda steps_involved, step: f"{steps_involved}, {step.get('name')}", scenario[key], steps_involved)
                elif key == "edges":
                    return_obj["edges_count"] = len(scenario[key])
                return_obj[key] = scenario[key]
            # this part of code is for modifying test data that can be used for rerun test command
            if demisto.command() != "safebreach-rerun-scenario":
                custom_data_obj = deepcopy(return_obj)
                custom_data_obj.pop("createdAt")
                custom_data_obj.pop("updatedAt")
                custom_data_obj.pop("description")
                custom_data_obj["successCriteria"] = \
                    custom_data_obj["successCriteria"] if not custom_data_obj["successCriteria"] else {}
                return_obj["custom_data_for_rerun_test"] = custom_data_obj
            # this part of code is for modifying test data that can be used for rerun simulation command
            custom_data_object_for_rerun_scenario = deepcopy(return_obj)
            for key in list(custom_data_object_for_rerun_scenario.keys()):
                if key not in ["name", "steps"]:
                    custom_data_object_for_rerun_scenario.pop(key)
            return_obj["custom_data_object_for_rerun_scenario"] = custom_data_object_for_rerun_scenario
            return_list.append(return_obj)

        return return_list

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
            "details": demisto.args().get("schedule details")
        }
        scenarios = self.get_response(url=url, method=method, request_params=request_params)
        return scenarios

    def get_services_status(self):

        method = "GET"
        url = "/lighthouse/v1/services"
        services_data = self.get_response(url=url, method=method)
        return services_data

    def get_verification_token(self):

        account_id = demisto.params().get("account_id", 0)
        method = "GET"
        url = f"/config/v1/accounts/{account_id}/nodes/secret"
        verification_data = self.get_response(url=url, method=method)
        return verification_data

    def rerun_test_or_simulation(self):

        account_id = demisto.params().get("account_id", 0)
        test_data = demisto.args().get("test data") if demisto.args().get("test data") else demisto.args().get("simulation data")
        if isinstance(test_data, dict):
            pass
        elif isinstance(test_data, str):
            try:
                test_data = json.loads(test_data)
            except json.decoder.JSONDecodeError:
                raise Exception("improper test data has been given for input,\
                    please validate and try again")

        position = demisto.args().get("position")
        feedback_loop = demisto.args().get("enable feedback loop")
        retry_simulations = demisto.args().get("retry simulation")
        wait_for_retry = demisto.args().get("wait for retry")
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

        method = "POST"
        url = f"/orch/v3/accounts/{account_id}/queue"
        tests_data = self.get_response(url=url, method=method, body={"plan": test_data}, request_params=request_params)
        return tests_data


@metadata_collector.command(
    command_name="safebreach-get-active-running-tests",
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
    flattened_running_tests_for_table = client.flatten_tests_data(running_tests.get("data", {}))
    human_readable = tableToMarkdown(
        name="Running Tests",
        t=flattened_running_tests_for_table,
        headers=test_outputs_headers_list)
    outputs = running_tests

    result = CommandResults(
        outputs_prefix="tests_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-active-running-simulations",
    inputs_list=None,
    outputs_prefix="active_simulations",
    outputs_list=[
        OutputArgument(name="status", description="the status of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="timestamp", description="the time of the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="numOfTasks", description="the number of steps involved in the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="planRunId", description="the planRunId of the simulation.",
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
        OutputArgument(name="node_ids_involved", description="the nodes involved in the simulation.",
                       prefix="active_tests", output_type=str),
        OutputArgument(name="node_names_involved", description="the names of nodes the simulation.",
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
    human_readable = tableToMarkdown(
        name="Running Simulations",
        t=flattened_simulations_data_for_table,
        headers=[
            "status", "timestamp", "numOfTasks", "planRunId", "stepRunId", "jobId", "taskId", "moveId",
            "moveRevision", "node_ids_involved", "node_names_involved", "timeout", "packageId",
        ])

    outputs = running_simulations
    result = CommandResults(
        outputs_prefix="active_simulations",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-play-pause-simulations-tests",
    inputs_list=[
        InputArgument(name="Simulation/Test State", description="State of tests/simulators to set to",
                      options=["resume", "pause"], required=True, is_array=False)],
    outputs_prefix="simulations_tests_status",
    outputs_list=[
        OutputArgument(name="status", description="the status of the simulations/tests.",
                       prefix="simulations_tests_status", output_type=str)
    ],
    description="This command gets simulations which are in running or queued state.")
def pause_resume_tests_and_simulations(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    simulations_status = client.set_simulations_status()
    human_readable = tableToMarkdown(
        name="Simulations/tests Status",
        t=simulations_status.get("data"),
        headers=["status"])

    outputs = simulations_status
    result = CommandResults(
        outputs_prefix="simulations_tests_status",
        outputs=outputs.get("data"),
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-get-schedules",
    inputs_list=[
        InputArgument(name="deleted", description="should deleted be retrieved.",
                      options=["true", "false"], default="true", required=False, is_array=False),
        InputArgument(name="details", description="Should details tests be included in result.",
                      options=["true", "false"], default="true", required=False, is_array=False),
    ],
    outputs_prefix="schedules",
    outputs_list=[
        OutputArgument(name="id", description="the Id of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="isEnabled", description="if simulation is enabled.",
                       prefix="schedules", output_type=bool),
        OutputArgument(name="name", description="the name of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="cronString", description="the cron expression the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="runDate", description="the run date of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="cronTimezone", description="the time zone of the schedule.",
                       prefix="planId", output_type=str),
        OutputArgument(name="taskId", description="the plan ID of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="description", description="the description of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="matrixId", description="the matrix ID of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="createdAt", description="the creation datetime of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="updatedAt", description="the updated datetime of the schedule.",
                       prefix="schedules", output_type=str),
        OutputArgument(name="deletedAt", description="the deletion time of the schedule.",
                       prefix="schedules", output_type=str),
    ],
    description="This command gets simulations which are in running or queued state.")
def get_schedules(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    headers = ["id", "isEnabled", "name", "cronString", "runDate",
               "cronTimezone", "taskId", "description", "matrixId",
               "createdAt", "updatedAt", "deletedAt"
               ]
    if demisto.args().get("schedule details") == "false":
        headers = ["id", "name"]

    schedules_data = client.get_schedules()
    human_readable = tableToMarkdown(
        name="Schedules",
        t=schedules_data.get("data"),
        headers=headers)

    outputs = schedules_data
    result = CommandResults(
        outputs_prefix="schedules",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-delete-schedule",
    inputs_list=[
        InputArgument(name="schedule ID", description="schedule ID",
                      required=True, is_array=False)
    ],
    outputs_prefix="deleted_Schedule",
    outputs_list=[
        OutputArgument(name="id", description="the Id of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="isEnabled", description="if simulation is enabled.",
                       prefix="deleted_Schedule", output_type=bool),
        OutputArgument(name="name", description="the name of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="cronString", description="the cron expression the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="runDate", description="the run date of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="cronTimezone", description="the time zone of the schedule.",
                       prefix="planId", output_type=str),
        OutputArgument(name="taskId", description="the plan ID of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="description", description="the description of the schedule.",
                       prefix="deleted_Schedule", output_type=str),
        OutputArgument(name="matrixId", description="the matrix ID of the schedule.",
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
    headers = ["id", "isEnabled", "name", "cronString", "runDate",
               "cronTimezone", "taskId", "description", "matrixId",
               "createdAt", "updatedAt", "deletedAt"
               ]

    schedules_data = client.delete_schedule()
    human_readable = tableToMarkdown(
        name="Deleted Schedule",
        t=schedules_data.get("data"),
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
        OutputArgument(name="recommended", description="the recommendation status of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="tags_list", description="the tags of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="categories", description="the category ids of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="steps_order", description="the order of steps involved in the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="order", description="the order of the scenario.",
                       prefix="prebuilt_scenarios", output_type=str),
        OutputArgument(name="minApiVer", description="the minimum version of API required for scenario to be executed",
                       prefix="prebuilt_scenarios", output_type=str)
    ],
    description="This command gets simulations which are in running or queued state.")
def get_prebuilt_scenarios(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    prebuilt_scenarios = client.get_prebuilt_scenarios()
    flattened_simulations_data_for_table = client.extract_default_scenario_fields(prebuilt_scenarios)
    human_readable = tableToMarkdown(
        name="Scenarios",
        t=flattened_simulations_data_for_table,
        headers=[
            "id", "name", "description", "createdBy", "createdAt", "updatedAt", "recommended",
            "tags_list", "categories", "steps_order", "order", "minApiVer"
        ])

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
        InputArgument(name="schedule details", description="Whether to get details of custom scenarios,\
                set this to true every time unless you explicitly dont need details",
                      default="true", options=["false", "true"], required=False, is_array=False),
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
    ],
    description="This command gets simulations which are in running or queued state.")
def get_custom_scenarios(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    custom_scenarios = client.get_custom_scenarios()
    if demisto.args().get("schedule details") == "true":
        flattened_simulations_data_for_table = client.extract_custom_scenario_fields(custom_scenarios.get("data", {}))
    else:
        flattened_simulations_data_for_table = custom_scenarios.get("data", {})
    human_readable = tableToMarkdown(
        name="Scenarios",
        t=flattened_simulations_data_for_table,
        headers=["id", "name", "description", "successCriteria", "originalScenarioId",
                 "actions_list", "edges_count", "steps_order", "createdAt", "updatedAt"])

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
    description="This command gets simulations which are in running or queued state.")
def get_services_status(client: Client):
    """This function gets all running tests summary and shows in a table

    Args:
        client (Client): Client class object for API calls

    Returns:
        CommandResults,Dict: This returns all tests related summary as a table and gives a dictionary as outputs for the same
    """
    services = client.get_services_status()
    modified_services_data = client.format_services_response(services)
    human_readable = tableToMarkdown(
        name="Services",
        t=modified_services_data,
        headers=["name", "version", "connection_status"])

    outputs = services
    result = CommandResults(
        outputs_prefix="services_status",
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
    description="This command gets simulations which are in running or queued state.")
def get_verification_token(client):
    token_data = client.get_verification_token()
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


@metadata_collector.command(
    command_name="safebreach-rerun-test",
    inputs_list=[
        InputArgument(name="position", description="position in queue to put the given test data at.",
                      required=False, is_array=False),
        InputArgument(name="enable feedback loop", description="this argument is used to enable/disable feedback loop",
                      default="true", options=["false", "true"], required=False, is_array=False),
        InputArgument(name="retry simulation", description="this argument is used to retry according to retry policy \
                mention in retry policy field", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="wait for retry", description="this arguments tells flow to retry the adding to queue after the \
                current step execution is completed", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="priority", description="the priority of this test action",
                      default="low", options=["low", "high"], required=False, is_array=False),
        InputArgument(name="test data", description="test data for the given test",
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
    flattened_simulations_data_for_table = client.extract_custom_scenario_fields([rerun_results.get("data", {})])
    human_readable = tableToMarkdown(
        name="Scenarios",
        t=flattened_simulations_data_for_table,
        headers=["id", "name", "description", "successCriteria", "originalScenarioId",
                 "actions_list", "edges_count", "steps_order", "createdAt", "updatedAt",
                 "planId", "ranBy", "ranFrom", "enableFeedbackLoop", "planRunId", "priority", "retrySimulations"])

    outputs = rerun_results
    result = CommandResults(
        outputs_prefix="changed_data",
        outputs=outputs,
        readable_output=human_readable
    )

    return result


@metadata_collector.command(
    command_name="safebreach-rerun-scenario",
    inputs_list=[
        InputArgument(name="position", description="position in queue to put the given simulation data at.",
                      required=False, is_array=False),
        InputArgument(name="enable feedback loop", description="this argument is used to enable/disable feedback loop",
                      default="true", options=["false", "true"], required=False, is_array=False),
        InputArgument(name="retry simulation", description="this argument is used to retry according to retry policy \
                mention in retry policy field", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="wait for retry", description="this arguments tells flow to retry the adding to queue after the \
                current step execution is completed", default="", options=["", "false", "true"], required=False, is_array=False),
        InputArgument(name="priority", description="the priority of this simulation action",
                      default="low", options=["low", "high"], required=False, is_array=False),
        InputArgument(name="simulation data", description="simulation data for the given simulation",
                      required=True, is_array=False),
    ],
    outputs_prefix="changed_data",
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
    ],
    description="this commands puts given simulation data at a given position, for this command to get test data input,\
        run safebreach-custom-scenarios-list and copy field 'data for rerun simulation' from table ")
def rerun_scenario(client):

    rerun_results = client.rerun_test_or_simulation()
    flattened_simulations_data_for_table = client.extract_custom_scenario_fields([rerun_results.get("data", {})])
    human_readable = tableToMarkdown(
        name="Scenarios",
        t=flattened_simulations_data_for_table,
        headers=["name", "actions_list", "edges_count", "steps_order", "ranBy", "ranFrom",
                 "enableFeedbackLoop", "planRunId", "priority", "retrySimulations"])

    outputs = rerun_results
    result = CommandResults(
        outputs_prefix="changed_data",
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

        elif demisto.command() == "safebreach-get-active-running-tests":
            result = get_all_running_tests_summary(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-active-running-simulations":
            result = get_all_running_simulations_summary(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-play-pause-simulations-tests":
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

        elif demisto.command() == "safebreach-get-services-status":
            result = get_services_status(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-get-verification-token":
            result = get_verification_token(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-rerun-test":
            result = rerun_test(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-rerun-scenario":
            result = rerun_scenario(client=client)
            return_results(result)

    except Exception as error:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(error)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
