import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

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
            result = client.get_all_users_for_test()
            return_results(result)

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

    except Exception as e:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
