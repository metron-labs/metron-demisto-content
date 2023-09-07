import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

# these are output fields related to test data that we are showing,
# TODO: need inputs related to fields of interest
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
    Execution begins here for most part
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

        elif demisto.command() == "safebreach-get-integration-errors":
            result = get_all_error_logs(client=client)
            return_results(result)

        elif demisto.command() == "safebreach-delete-integration-errors":
            result = delete_integration_error_logs(client=client)
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

    except Exception as e:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
