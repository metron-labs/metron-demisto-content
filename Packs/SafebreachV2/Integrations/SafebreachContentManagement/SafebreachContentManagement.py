import demistomock as demisto  # noqa: F401
from CommonServerPython import *  # noqa: F401

DATE_FORMAT = '%Y-%m-%d %H:%M:%S UTC'  # ISO8601 format with UTC, default in XSOAR

bool_map = {
    "true": True,
    "false": False,
    "True": True,
    "False": False,
    True: True,
    False: False
}

metadata_collector = YMLMetadataCollector(
    integration_name="Safebreach Content Management",
    description="""
    This Integration aims to provide easy access to safebreach from XSOAR.
    Following are the things that user can get access through XSOAR command integration:
    1. User get, create, update and delete. 
    2. Deployment create, update and delete.
    3. Tests get and delete.
    4. Nodes get, update, delete.
    5. Get current tests/simulation status and/or queue them.
    """,
    display="Safebreach Content Management",
    category="Deception & Breach Simulation",
    docker_image="demisto/python3:3.10.13.74666",
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
        user_email = demisto.args().get("Email", "").strip()
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

    def create_user_data(self):
        """This function takes user inputs and then formats it and 
        then calls create user endpoint.

        Returns:
            dict: created user data
        """
        account_id = demisto.params().get("account_id", 0)
        name = demisto.args().get("Name", "").strip()
        email = demisto.args().get("Email", "").strip()
        is_active = bool_map.get(demisto.args().get("Is Active"), "false")
        send_email_post_creation = bool_map.get(demisto.args().get("Email Post Creation"), "false")
        password = demisto.args().get("Password")
        admin_name = demisto.args().get("Admin Name", "").strip()
        change_password = bool_map.get(demisto.args().get("Change Password on create"), "false")
        role = demisto.args().get("User role", "").strip()
        deployment_list = demisto.args().get("Deployments", [])
        deployment_list = list(deployment_list) if deployment_list else []

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

        user_id = demisto.args().get("User ID")
        user_email = demisto.args().get("Email", "").strip()

        name = demisto.args().get("Name", "").strip()
        is_active = bool_map[demisto.args().get("Is Active", "False")]
        description = demisto.args().get("User Description", "").strip()
        role = demisto.args().get("User role", "").strip()
        password = demisto.args().get("Password")
        deployment_list = demisto.args().get("Deployments", [])
        deployment_list = list(deployment_list) if deployment_list else []
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

    name = demisto.args().get("name", "a random non existent name which shouldn't be searchable")
    email = demisto.args().get("email", "").strip()
    user_list = client.get_users_list()
    demisto.info(f"retrieved user list which has {len(user_list)} users")

    filtered_user_list = list(
        filter(lambda user_data: ((name in user_data['name'] if name else False) or (email in user_data['email'])), user_list))
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
        OutputArgument(name="id", description="The ID of User updated.", prefix="updated_user_data", output_type=int),
        OutputArgument(name="name", description="The name of User updated.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="email", description="The email of User updated.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="createdAt", description="The creation time of User updated.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="deletedAt", description="The Deletion time of User updated.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="roles", description="The roles of User updated.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="description", description="The description of User updated.", prefix="updated_user_data",
                       output_type=str),
        OutputArgument(name="role", description="The role of User updated.", prefix="updated_user_data",
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
    demisto.info(f"json output for delete uer is {outputs}")

    result = CommandResults(
        outputs_prefix="deleted_user_data",
        outputs=outputs,
        readable_output=human_readable
    )
    return result


def main() -> None:

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

    except Exception as e:
        demisto.error(f"Error generated while executing {demisto.command}, \n {traceback.format_exc()}")
        return_error(f'Failed to execute {demisto.command()} command .\nError:\n{str(e)}')


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
