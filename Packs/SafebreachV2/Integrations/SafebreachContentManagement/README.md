
    This Integration aims to provide easy access to safebreach from XSOAR.
    Following are the things that user can get access through XSOAR command integration:
    1. User get, create, update and delete. 
    2. Deployment create, update and delete.
    3. Tests get and delete.
    4. Nodes get, update, delete.
    5. Get current tests/simulation status and/or queue them.
    
This integration was integrated and tested with version 0.0.1 of Safebreach Content Management.

## Configure Safebreach Content Management on Cortex XSOAR

1. Navigate to **Settings** > **Integrations** > **Servers & Services**.
2. Search for Safebreach Content Management.
3. Click **Add instance** to create and configure a new integration instance.

    | **Parameter** | **Description** | **Required** |
    | --- | --- | --- |
    | Server URL | This is base URL for your instance. | True |
    | API Key | This is API key for your instance, this can be created in safebreach user                       administration&gt;APIkeys and then it must be saved as there is no way to view this again | True |
    | Account ID | This is account ID of account with which we want to get data from safebreach | True |
    | Verify SSL Certificate | This Field is useful for checking if the certificate of SSL for HTTPS is valid or not | False |
    | Use system proxy settings | This Field is useful for asking integration to use default system proxy settings. | False |

4. Click **Test** to validate the URLs, token, and connection.

## Commands

You can execute these commands from the Cortex XSOAR CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.

### safebreach-approve-simulator-with-given-name

***

    This command approves simulator with given name with given details in simulator_or_node_name.
    

#### Base Command

`safebreach-approve-simulator-with-given-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| simulator_or_node_name | <br/>                      Name of simulator/node to search with. this is name which will be used to search the list of simulators <br/>                      which will be retrieved and of which whose name matches this input value.<br/>                      . | Required | 
| details | <br/>                      If simulator details are to be retrieved while searching. this should be selected to true if the command is<br/>                      "safebreach-get-simulator-with-name" and if its false then only very small number of fields will be <br/>                      retrieved thus making search with name impossible.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| deleted | <br/>                      If deleted are to be included for search. Incase the simulator we are searching for is deleted one then<br/>                      set this to true and then search. else keep it as default and set to false.<br/>                      . Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| approved_simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| approved_simulator_details.simulator_id | String | The Id of given simulator. | 
| approved_simulator_details.name | String | name for given simulator. | 
| approved_simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| approved_simulator_details.is_critical | String | Whether the simulator is critical. | 
| approved_simulator_details.is_exfiltration | String | If Simulator is exfiltration target. | 
| approved_simulator_details.is_infiltration | String | If simulator is infiltration target. | 
| approved_simulator_details.is_mail_target | String | If simulator is mail target. | 
| approved_simulator_details.is_mail_attacker | String | If simulator is mail attacker. | 
| approved_simulator_details.is_pre_executor | String | Whether the node is pre executor. | 
| approved_simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| approved_simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| approved_simulator_details.external_ip | String | external ip of given simulator. | 
| approved_simulator_details.internal_ip | String | internal ip of given simulator. | 
| approved_simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| approved_simulator_details.preferred_interface | String | Preferred simulator interface. | 
| approved_simulator_details.preferred_ip | String | Preferred Ip of simulator. | 
| approved_simulator_details.hostname | String | Hostname of given simulator. | 
| approved_simulator_details.connection_type | String | connection_type of given simulator. | 
| approved_simulator_details.simulator_status | String | status of the simulator. | 
| approved_simulator_details.connection_status | String | connection status of node/simulator. | 
| approved_simulator_details.simulator_framework_version | String | Framework version of simulator. | 
| approved_simulator_details.operating_system_type | String | operating system type of given simulator. | 
| approved_simulator_details.operating_system | String | Operating system of given simulator. | 
| approved_simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| approved_simulator_details.deployments | String | deployments simulator is part of. | 
| approved_simulator_details.created_at | String | Creation datetime of simulator. | 
| approved_simulator_details.updated_at | String | Update datetime of given simulator. | 
| approved_simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| approved_simulator_details.assets | String | Assets of given simulator. | 
| approved_simulator_details.simulation_users | String | simulator users list. | 
| approved_simulator_details.proxies | String | Proxies of simulator. | 
| approved_simulator_details.advanced_actions | String | Advanced simulator details. | 

### safebreach-generate-api-key

***

    This command creates a API Key with given data. The API key created will be shown in API keys section 
    of safebreach UI with name and description as given in input fields "name" and "description". Name is a required value
    but description isn't, The API key generated can be seen only once, so it is recommended to store/save it for further use.
    

#### Base Command

`safebreach-generate-api-key`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| name | Name of the API Key to create. This will be the name shown in UI for API key under API keys section. | Required | 
| description | <br/>                      Description of the API Key to create. This is not a required field but it is recommended to store a <br/>                      description for easier identification if your use case requires using multiple API keys for multiple tasks.<br/>                      . | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| generated_api_key.name | Number | The Name of API Key generated through this command,                            This will match the input name of the command. | 
| generated_api_key.description | String | The Description of API Key created.                            this will be same as input description given for the command. | 
| generated_api_key.createdBy | String | The id of user who generated this API key. | 
| generated_api_key.createdAt | String | The creation date and time of API key. | 
| generated_api_key.key | String | The value of API key generated. store this for further use as this will only be shown once. | 
| generated_api_key.roles | String | The roles allowed for this api key.                            This will generally be the roles assigned to user who created the key. | 
| generated_api_key.role | String | The role of API Key. | 

### safebreach-create-deployment

***
This command creates a deployment with given data.

#### Base Command

`safebreach-create-deployment`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| name | Name of the deployment to create. this will be shown as name in deployments page of safebreach. | Required | 
| description | Description of the deployment to create. <br/>                      This will show as description of the deployment in your safebreach instance.<br/>                      It is generally preferable to give description while creating a deployment for easier identification. | Optional | 
| nodes | A deployment is a group of simulators which work as a single group. this field needs<br/>                      Comma separated IDs of all simulators that should be part of this deployment.<br/>                      the ID can be retrieved from safebreach-get-all-simulator-details command with<br/>                      details input set to true so that the details can be seen. Care should be taken when giving <br/>                      simulator IDs as comma separated values as if any simulator has been deleted then this deployment <br/>                      wont contain that simulator on creation. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| created_deployment_data.id | Number | The ID of deployment created. this Id can be used to update ,delete deployment as                       deployment_id field of the deployment. | 
| created_deployment_data.accountId | String | This field shows account ID of user who has created the account. | 
| created_deployment_data.name | String | The name of deployment created. this will be name which will be shown on deployments page                       of safebreach and name that is given as input to the command. | 
| created_deployment_data.createdAt | String | The creation date and time of deployment , this will be closer to                       command execution time if the deployment creation is successful. | 
| created_deployment_data.description | String | The description of the deployment created will be shown in description                            part of the table in safebreach. | 
| created_deployment_data.nodes | String | The nodes that are part of deployment. In case any nodes are given during                       creation that are deleted before the creation time then the deployment wont contain those nodes. | 

### safebreach-create-user

***
This command creates a user with given data.

#### Base Command

`safebreach-create-user`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| name | Name of the user to create. | Required | 
| email | Email of the user to Create. | Required | 
| is_active | <br/>                      Whether the user is active upon creation. if this is set to true then user will be active as soon<br/>                      as this command succeeds but if set to false then the user has to activated and if user will have to<br/>                      do reset password process to become active. by default the user will be active.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| email_post_creation | <br/>                      This field sends email to user post creation if this field is set to true, by default this field is set <br/>                      to false. set this to true if user has to be sent email post creation else set this to false.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| password | <br/>                      This will be set as password for the created user. incase needed the flag change password can be set to<br/>                      true if its needed for user to change password on first login.<br/>                      . | Required | 
| admin_name | <br/>                      Name of the Admin creating user. This will be populated in created by field of user page in safebreach.<br/>                      . | Optional | 
| change_password_on_create | <br/>                      Should user change password on creation. when this is set to true then user will have to reset password on<br/>                      the next login, this can be used if we want user to reset password as soon as they login.<br/>                      . Possible values are: true, false. Default is false. | Optional | 
| user_role | <br/>                      Role of the user being Created. The user will have the permissions of role they are being assigned here.<br/>                      choices are viewer, administrator, content developer, operator.<br/>                      . Possible values are: viewer, administrator, contentDeveloper, operator. Default is viewer. | Optional | 
| deployments | <br/>                      Comma separated ID of all deployments the user should be part of. The deployment IDs can be retrieved from<br/>                      get-deployments-list command or from UI directly but care should be noted that only deployment ids of <br/>                      deployments which haven't been deleted will be shown here and after creation of user. for example<br/>                      if 1,2,3 are deployment ids given while creation but if 2 is deleted then when user is created , he will<br/>                      only have 1,3.<br/>                      . | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| created_user_data.id | Number | The ID of User created. | 
| created_user_data.name | String | The name of User created. | 
| created_user_data.email | String | The email of User created. | 
| created_user_data.createdAt | String | The creation time of User. | 
| created_user_data.deletedAt | String | The Deletion time of User . This will be empty unless the user is deleted. | 
| created_user_data.roles | String | The roles and permissions of User created. | 
| created_user_data.description | String | The description of User if any is given at creation time, it will be populated here. | 
| created_user_data.role | String | The role assigned to user during creation. | 
| created_user_data.deployments | String | The deployments user is part of. | 

### safebreach-delete-api-key

***

    This command deletes a API key with given name. When given an input key name, it will internally retrieve all
    active keys and then delete the one with name matching the name entered, the match is not case sensitive match
    but its exact word match so please enter key name exactly as shown in UI to delete it.
    

#### Base Command

`safebreach-delete-api-key`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| key_name | Name of the API Key to Delete. This will be used for searching key with given name<br/>                      and then once it matches, that API key will be deleted. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_api_key.name | Number | The Name of API Key deleted. | 
| deleted_api_key.description | String | Description of API Key deleted. | 
| deleted_api_key.createdBy | String | The id of user who generated this API key. | 
| deleted_api_key.createdAt | String | The creation time and date of API key. | 
| deleted_api_key.deletedAt | String | The deletion time and date of API key. The deletion date and time are generally                       close to the command execution time and date. | 

### safebreach-delete-deployment

***

    This command deletes a deployment with given data.The deployment_id field of this command can  be retrieved from 
    get-all-deployments command. If the user wants to search with deployment ID then they can search it that way or 
    if user just wants to search with name then they can just give name field and the command internally searches the deployment 
    with given name and deletes it.

#### Base Command

`safebreach-delete-deployment`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| deployment_id | <br/>                      ID of the deployment to delete. this can be searched with list-deployments command or<br/>                      from UI. this will be taken as id of deployment which we want to delete.<br/>                      . | Optional | 
| deployment_name | <br/>                      Name of the deployment to search whose data will be deleted. <br/>                      This field will be used to search the existing deployment names and find a deployment <br/>                      whose name matches this and that will be used as deployment whose data we are updating. <br/>                      . | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_deployment_data.id | Number | The ID of deployment which has been deleted. | 
| deleted_deployment_data.accountId | String | The account Id of user who deleted the deployment. | 
| deleted_deployment_data.name | String | The name of deployment before the deployment was deleted. | 
| deleted_deployment_data.createdAt | String | The creation date and time of deployment which has been deleted. | 
| deleted_deployment_data.description | String | The description of deployment before it was deleted. | 
| deleted_deployment_data.nodes | String | The nodes that are part of deployment before it was deleted. | 

### safebreach-delete-integration-errors

***

    This command deletes connector related errors and warnings. This command needs connector id as input which will be
    used to delete the errors/warnings for the given connector id. the connector ids can be retrieved by using command
    get-all-integration-issues and this command will give connector id which can be used for input. 
    

#### Base Command

`safebreach-delete-integration-errors`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| connector_id | <br/>                      The connector ID of Integration connector to have its errors/warnings deleted.<br/>                      this is used to search for integration connector which will have its logs cleared, there is no way to<br/>                      clear just errors or just warnings here and this connector with this will be having all errors and warnings<br/>                      cleared.<br/>                      . | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| errors_cleared.error | Number | Error count after deletion of errors for the given connector. | 
| errors_cleared.result | String | error deletion status whether true or false. | 

### safebreach-delete-schedule

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-delete-schedule`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| schedule_id | schedule ID of schedule to delete. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_Schedule.id | String | the Id of the schedule. | 
| deleted_Schedule.isEnabled | Boolean | if schedule is enabled. | 
| deleted_Schedule.name | String | the name of the schedule. | 
| deleted_Schedule.cronString | String | the cron expression the schedule. | 
| deleted_Schedule.runDate | String | the run date of the schedule. | 
| deleted_Schedule.cronTimezone | String | the time zone of the schedule. | 
| deleted_Schedule.taskId | String | the plan ID of the schedule. | 
| deleted_Schedule.description | String | the description of the schedule. | 
| deleted_Schedule.matrixId | String | the matrix ID of the schedule. | 
| deleted_Schedule.createdAt | String | the creation datetime of the schedule. | 
| deleted_Schedule.updatedAt | String | the updated datetime of the schedule. | 
| deleted_Schedule.deletedAt | String | the deletion time of the schedule. | 

### safebreach-delete-simulator-with-name

***
This command deletes simulator with given name in simulator_or_node_name field.

#### Base Command

`safebreach-delete-simulator-with-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| simulator_or_node_name | <br/>                      Name of simulator/node to search with. this is name which will be used to search the list of simulators <br/>                      which will be retrieved and of which whose name matches this input value.<br/>                      . | Required | 
| should_force_delete | setting this to false will evaluate the whether the simulator is connected or not and if its running a <br/>                       simulation then the simulator wont be deleted. but if it is set to true then this will delete the <br/>                       simulator irrespective of connection status. Possible values are: true, false. Default is false. | Required | 
| details | <br/>                      If simulator details are to be retrieved while searching. this should be selected to true if the command is<br/>                      "safebreach-get-simulator-with-name" and if its false then only very small number of fields will be <br/>                      retrieved thus making search with name impossible.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| deleted | if deleted are to be included for search. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| deleted_simulator_details.simulator_id | String | The Id of given simulator. | 
| deleted_simulator_details.name | String | name for given simulator. | 
| deleted_simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| deleted_simulator_details.is_critical | String | Whether the simulator is critical. | 
| deleted_simulator_details.is_exfiltration | String | If Simulator is exfiltration target. | 
| deleted_simulator_details.is_infiltration | String | If simulator is infiltration target. | 
| deleted_simulator_details.is_mail_target | String | If simulator is mail target. | 
| deleted_simulator_details.is_mail_attacker | String | If simulator is mail attacker. | 
| deleted_simulator_details.is_pre_executor | String | Whether the node is pre executor. | 
| deleted_simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| deleted_simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| deleted_simulator_details.external_ip | String | external ip of given simulator. | 
| deleted_simulator_details.internal_ip | String | internal ip of given simulator. | 
| deleted_simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| deleted_simulator_details.preferred_interface | String | Preferred simulator interface. | 
| deleted_simulator_details.preferred_ip | String | Preferred Ip of simulator. | 
| deleted_simulator_details.hostname | String | Hostname of given simulator. | 
| deleted_simulator_details.connection_type | String | connection_type of given simulator. | 
| deleted_simulator_details.simulator_status | String | status of the simulator. | 
| deleted_simulator_details.connection_status | String | connection status of node/simulator. | 
| deleted_simulator_details.simulator_framework_version | String | Framework version of simulator. | 
| deleted_simulator_details.operating_system_type | String | operating system type of given simulator. | 
| deleted_simulator_details.operating_system | String | Operating system of given simulator. | 
| deleted_simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| deleted_simulator_details.deployments | String | deployments simulator is part of. | 
| deleted_simulator_details.created_at | String | Creation datetime of simulator. | 
| deleted_simulator_details.updated_at | String | Update datetime of given simulator. | 
| deleted_simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| deleted_simulator_details.assets | String | Assets of given simulator. | 
| deleted_simulator_details.simulation_users | String | simulator users list. | 
| deleted_simulator_details.proxies | String | Proxies of simulator. | 
| deleted_simulator_details.advanced_actions | String | Advanced simulator details. | 

### safebreach-delete-test-summary-of-given-test

***
This command deletes tests with given plan ID.

#### Base Command

`safebreach-delete-test-summary-of-given-test`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| test_id | test id of the test summary which we want to search the test with. | Optional | 
| soft_delete | <br/>                      This field when set to true will delete the test from database directly but when set to false<br/>                      this will just set the status of test to deleted.<br/>                      . Possible values are: true, false. Default is false. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_test_results.planId | String | Plan ID of the simulation. | 
| deleted_test_results.planName | String | Test Name of the simulation. | 
| deleted_test_results.securityActionPerControl | String | Security Actions of the simulation. | 
| deleted_test_results.planRunId | String | Test id of the simulation. | 
| deleted_test_results.status | String | status of the simulation. | 
| deleted_test_results.plannedSimulationsAmount | String | Planned simulations amount of the simulation. | 
| deleted_test_results.simulatorExecutions | String | simulator executions of the simulation. | 
| deleted_test_results.ranBy | String | user who started the simulation. | 
| deleted_test_results.simulatorCount | String | simulators count of simulation. | 
| deleted_test_results.endTime | String | End Time of the simulation. | 
| deleted_test_results.startTime | String | start time of the simulation. | 
| deleted_test_results.finalStatus.stopped | String | stopped count of simulation. | 
| deleted_test_results.finalStatus.missed | String | missed count of simulation. | 
| deleted_test_results.finalStatus.logged | String | logged count of simulation. | 
| deleted_test_results.finalStatus.detected | String | detected count of simulation. | 
| deleted_test_results.finalStatus.prevented | String | prevented count of simulation. | 
| deleted_test_results.finalStatus.inconsistent | String | inconsistent count of simulation. | 
| deleted_test_results.finalStatus.drifted | String | drifted count of simulation. | 
| deleted_test_results.finalStatus.not_drifted | String | not drifted count of simulation. | 
| deleted_test_results.finalStatus.baseline | String | baseline count of simulation. | 

### safebreach-delete-user

***
This command deletes a user with given data.

#### Base Command

`safebreach-delete-user`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| user_id | user ID of user from safebreach to search. this can be retrieved in 2 ways,<br/>                      1. run get-all-users command and then look for user id of user with matching criteria<br/>                      but to see details its required that details parameter to be set to true,<br/>                      2. if you know user name or email then those can be used in safebreach-get-user-with-given-name-or-email<br/>                      command and then search for user with required details in displayed results for ID.<br/>                      This field is not  required, meaning even if just email is given , we will internally search user<br/>                      id with the matching email and use the user for further process. | Optional | 
| email | Email of the user to Search for updating user details. This is a required field.<br/>                      The user with matching email will be considered as user whose data will be updated. | Required | 
| should_include_details | <br/>                      This field when selected true will retrieve the details of users like name, email, role, whether the user <br/>                      is active, when the user is created, updated and when user is deleted if deleted and deployments related to<br/>                      user etc. if this field is set to false then we only retrieve name and id of user, thus when chaining <br/>                      commands like delete or update user, please set details to true.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| should_include_deleted | <br/>                      If deleted users are to be included while querying all users. by default this is set to true because<br/>                      there might be cases where its preferable to see deleted users too. this can be set to false to see <br/>                      only users who dont have their credentials deleted.<br/>                      . Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_user_data.id | Number | The ID of User whose data has been deleted. | 
| deleted_user_data.name | String | The name of User deleted. | 
| deleted_user_data.email | String | The email of User deleted. | 
| deleted_user_data.createdAt | String | the time at which the user who has been selected has been created. | 
| deleted_user_data.updatedAt | String | The last updated time of User selected for delete.                       this will be less than time choses to delete. | 
| deleted_user_data.deletedAt | String | The Deletion time of User selected to delete.                       this will be the execution time for the command or close to it. | 
| deleted_user_data.roles | String | The roles of User before they were deleted. | 
| deleted_user_data.description | String | The description of User who has been deleted. | 
| deleted_user_data.role | String | The roles and permissions of User who has been deleted. | 
| deleted_user_data.deployments | String | The deployments related to user before he was deleted. | 

### safebreach-get-integration-issues

***

    This command gives all connector related issues and warning. this will show the connector error and warnings which are 
    generally displayed in installed integrations page.
    

#### Base Command

`safebreach-get-integration-issues`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| integration_errors.connector | Number | The connector ID of Integration connector. A general notation that has been followed here is                       as follows, if the  id has _default at the end then its a default connector else its a custom connector. | 
| integration_errors.action | String | The action of Integration connector error. This describes where exactly did the error occur,        		 if its search,then it implies error/warning happened when connector was trying that process. | 
| integration_errors.success | String | status of connector error. This implies whether the connector was able to                        successfully perform the operation or if it failed partway.                        So false implies it failed partway and true implies it was successfully completed. | 
| integration_errors.error | String | This is the exact error description shown on safebreach connector error/warning page.                        This description can be used for understanding of what exactly happened for the connector to fail. | 
| integration_errors.timestamp | String | Time at which error/warning occurred. This can be used to pinpoint error which occurred                       across connectors if time of origin was remembered. | 

### safebreach-get-active-running-simulations

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-get-active-running-simulations`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| active_simulations.status | String | the status of the simulation, if its running or queued. | 
| active_simulations.timestamp | String | the time at which simulation was triggered. | 
| active_simulations.numOfTasks | String | the number of tasks involved in the simulation. | 
| active_simulations.test id | String | this is test ID of the simulation. | 
| active_simulations.stepRunId | String | the step id of the simulation. | 
| active_simulations.jobId | String | the job id of the simulation. | 
| active_simulations.taskId | String | the task ID of the simulation. | 
| active_simulations.moveId | String | the move ID of the simulation. | 
| active_simulations.moveRevision | String | the move revision of the simulation. | 
| active_simulations.node_ids_involved | String | the nodes involved in the simulation. | 
| active_simulations.node_names_involved | String | the names of nodes the simulation. | 
| active_simulations.timeout | String | the timeout of the simulation if its failing etc. | 
| active_simulations.packageId | String | the package ID of the simulation. | 

### safebreach-get-active-running-tests

***
This command gets tests which are in running or queued state.

#### Base Command

`safebreach-get-active-running-tests`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| active_tests.id | Number | Id of Actively running test. | 
| active_tests.name | String | Name of the test being run. | 
| active_tests.description | String | Details related to the test being run. | 
| active_tests.successCriteria | String | Plan Run ID of the simulation. | 
| active_tests.originalScenarioId | String | Original scenario ID of the running test. | 
| active_tests.actions count | String | number of actions. | 
| active_tests.edges count | String | number of edges. | 
| active_tests.createdAt | String | details related to when test is created. | 
| active_tests.updatedAt | String | details related to when test is last updated/changed. | 
| active_tests.steps count | String | number of steps in simulator. | 
| active_tests.planId | String | planId of the test. | 
| active_tests.originalPlan ID | String | original plan ID for reference. | 
| active_tests.ranBy | String | User who ran the plan. | 
| active_tests.ranFrom | String | Where the test ran from. | 
| active_tests.enableFeedbackLoop | String | Should feedback loop be enabled. | 
| active_tests.testID | String | plan run id. | 
| active_tests.priority | String | priority of tests. | 
| active_tests.retrySimulations | String | Should simulations be retried. | 
| active_tests.flowControl | String | Flow control of tests. | 
| active_tests.slot position | String | position in queue. | 
| active_tests.slot status | Boolean | is the test paused. | 
| active_tests.pauseDuration | String | is the test paused and if so till when. | 
| active_tests.totalJobs | String | Total number of jobs for this test. | 
| active_tests.pausedDate | String | when the test is paused. | 
| active_tests.expectedSimulationsAmount | String | number of simulations expected. | 
| active_tests.dispatchedSimulationsAmount | String | the number of simulations dispatched. | 
| active_tests.blockedSimulationsAmount | String | The number of simulations blocked. | 
| active_tests.unblockedSimulationsAmount | String | The number of simulations unblocked. | 
| active_tests.skippedSimulationsAmount | String | The number of simulations skipped. | 
| active_tests.failedSimulationsAmount | String | The number of simulations failed. | 
| active_tests.isPrepared | String | Total number of simulations that have been prepared. | 

### safebreach-get-available-simulator-details

***
This command to get all available simulators. if details is set to true then it retrieves simulator details like name, 
    hostname, internal and external ips, types of targets and attacker configurations this simulator is associated with etc.
    if its set to false then it retrieves just name, id, simulation users, proxies etc. if deleted is set to true then it
    retrieves the data which has been deleted.

#### Base Command

`safebreach-get-available-simulator-details`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| details | <br/>                      If simulator details are to be retrieved while searching. this should be selected to true if the command is<br/>                      "safebreach-get-simulator-with-name" and if its false then only very small number of fields will be <br/>                      retrieved thus making search with name impossible.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| deleted | <br/>                      if deleted simulators/nodes are to be included for search.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| secret | if secrets are to be included for search. Possible values are: true, false. | Optional | 
| should_include_proxies | if proxies are to be included for search. Possible values are: true, false. | Optional | 
| hostname | if hostname to be included for search. | Optional | 
| connection_type | if connectionType to be included for search. | Optional | 
| external_ip | if external IP details to be included for search. | Optional | 
| internal_ip | if Internal IP are to be included for search. | Optional | 
| os | operating system name to filter with, Eg: LINUX,WINDOWS etc. | Optional | 
| sort_direction | direction in which secrets are to be sorted. Possible values are: asc, desc. Default is asc. | Optional | 
| page_size | number of entries to search. | Optional | 
| is_enabled | if to search only enabled ones. Possible values are: true, false. | Optional | 
| is_connected | status of connection of nodes to search. Possible values are: true, false. | Optional | 
| is_critical | whether to search only for critical nodes or not. Possible values are: true, false. | Optional | 
| additional_details | Whether to show additional details or not. Possible values are: true, false. | Optional | 
| status | if simulator status are to be included for search. Possible values are: APPROVED, PENDING, ALL. Default is ALL. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| simulator_details.simulator_id | String | The Id of given simulator. | 
| simulator_details.name | String | name for given simulator. | 
| simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| simulator_details.is_critical | String | Whether the simulator is critical. | 
| simulator_details.is_exfiltration | String | If Simulator is exfiltration target. | 
| simulator_details.is_infiltration | String | If simulator is infiltration target. | 
| simulator_details.is_mail_target | String | If simulator is mail target. | 
| simulator_details.is_mail_attacker | String | If simulator is mail attacker. | 
| simulator_details.is_pre_executor | String | Whether the node is pre executor. | 
| simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| simulator_details.external_ip | String | external ip of given simulator. | 
| simulator_details.internal_ip | String | internal ip of given simulator. | 
| simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| simulator_details.preferred_interface | String | Preferred simulator interface. | 
| simulator_details.preferred_ip | String | Preferred Ip of simulator. | 
| simulator_details.hostname | String | Hostname of given simulator. | 
| simulator_details.connection_type | String | connection_type of given simulator. | 
| simulator_details.simulator_status | String | status of the simulator. | 
| simulator_details.connection_status | String | connection status of node/simulator. | 
| simulator_details.simulator_framework_version | String | Framework version of simulator. | 
| simulator_details.operating_system_type | String | operating system type of given simulator. | 
| simulator_details.operating_system | String | Operating system of given simulator. | 
| simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| simulator_details.deployments | String | deployments simulator is part of. | 
| simulator_details.created_at | String | Creation datetime of simulator. | 
| simulator_details.updated_at | String | Update datetime of given simulator. | 
| simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| simulator_details.assets | String | Assets of given simulator. | 
| simulator_details.simulation_users | String | simulator users list. | 
| simulator_details.proxies | String | Proxies of simulator. | 
| simulator_details.advanced_actions | String | Advanced simulator details. | 

### safebreach-get-test-summary

***
This command gets tests with given modifiers.

#### Base Command

`safebreach-get-test-summary`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| include_archived | Should archived tests be included in search. Possible values are: true, false. Default is true. | Optional | 
| entries_per_page | number of entries per page to be retrieved. | Optional | 
| plan_id | plan Id of test. | Optional | 
| status | Status of simulation. Possible values are: CANCELED, COMPLETED. Default is CANCELED. | Optional | 
| simulation_id | Unique ID of the simulation. | Optional | 
| sort_by | sort by option. Possible values are: endTime, startTime, testID, stepRunId. Default is endTime. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| test_results.planId | String | Plan ID of the simulation. | 
| test_results.planName | String | Test Name of the simulation. | 
| test_results.securityActionPerControl | String | Security Actions of the simulation. | 
| test_results.planRunId | String | Test id of the simulation. | 
| test_results.status | String | status of the simulation. | 
| test_results.plannedSimulationsAmount | String | Planned simulations amount of the simulation. | 
| test_results.simulatorExecutions | String | simulator executions of the simulation. | 
| test_results.ranBy | String | user who started the simulation. | 
| test_results.simulatorCount | String | simulators count of simulation. | 
| test_results.endTime | String | End Time of the simulation. | 
| test_results.startTime | String | start time of the simulation. | 
| test_results.finalStatus.stopped | String | stopped count of simulation. | 
| test_results.finalStatus.missed | String | missed count of simulation. | 
| test_results.finalStatus.logged | String | logged count of simulation. | 
| test_results.finalStatus.detected | String | detected count of simulation. | 
| test_results.finalStatus.prevented | String | prevented count of simulation. | 
| test_results.finalStatus.inconsistent | String | inconsistent count of simulation. | 
| test_results.finalStatus.drifted | String | drifted count of simulation. | 
| test_results.finalStatus.not_drifted | String | not drifted count of simulation. | 
| test_results.finalStatus.baseline | String | baseline count of simulation. | 

### safebreach-get-test-summary-with-plan-run-id

***

    This command gets tests with given plan ID and the order is based on sort by column.
    

#### Base Command

`safebreach-get-test-summary-with-plan-run-id`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| include_archived | <br/>                      Should archived tests be included in search. Archived tests are tests which have been <br/>                      set aside for further use in an inactive state. if this is set to false then archived tests<br/>                      wont be pulled but  if set to true then they will be pulled and shown.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| entries_per_page | <br/>                      number of entries to be retrieved. for viewing, this will work in combination with sort_by field and<br/>                      things will be sorted in decreasing order so if you chose 100 entries here and if endtime is chosen as sort<br/>                      then it will show last 100 executions with latest end time.<br/>                      . | Optional | 
| plan_id | <br/>                      plan Id of test. this can be found on UI, if unsure about this then please run safebreach-get-test-summary <br/>                      instead of this with same parameters as inputs.<br/>                      . | Required | 
| status | tests with this status will be searched and filtered. Possible values are: CANCELED, COMPLETED. | Optional | 
| simulation_id | Unique ID of the simulation. | Optional | 
| sort_by | how to sort the results retrieved, there are 4 options:<br/>                      1. sorting by endTime will show results in terms of decreasing order of simulations end time.<br/>                      2. sorting by start time will show results in terms of the decreasing order of simulation start time.<br/>                      3. testID - this is test id and sorting by this will be decreasing order of test id.<br/>                      4. stepRunId -. Possible values are: endTime, startTime, testID, stepRunId. Default is endTime. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| test_results.planId | String | Plan ID of the simulation. | 
| test_results.planName | String | Test Name of the simulation. | 
| test_results.securityActionPerControl | String | Security Actions of the simulation. | 
| test_results.planRunId | String | Test id of the simulation. | 
| test_results.status | String | status of the simulation. | 
| test_results.plannedSimulationsAmount | String | Planned simulations amount of the simulation. | 
| test_results.simulatorExecutions | String | simulator executions of the simulation. | 
| test_results.ranBy | String | user who started the simulation. | 
| test_results.simulatorCount | String | simulators count of simulation. | 
| test_results.endTime | String | End Time of the simulation. | 
| test_results.startTime | String | start time of the simulation. | 
| test_results.finalStatus.stopped | String | stopped count of simulation. | 
| test_results.finalStatus.missed | String | missed count of simulation. | 
| test_results.finalStatus.logged | String | logged count of simulation. | 
| test_results.finalStatus.detected | String | detected count of simulation. | 
| test_results.finalStatus.prevented | String | prevented count of simulation. | 
| test_results.finalStatus.inconsistent | String | inconsistent count of simulation. | 
| test_results.finalStatus.drifted | String | drifted count of simulation. | 
| test_results.finalStatus.not_drifted | String | not drifted count of simulation. | 
| test_results.finalStatus.baseline | String | baseline count of simulation. | 

### safebreach-get-all-users

***
This command gives all users depending on inputs given.

#### Base Command

`safebreach-get-all-users`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| should_include_details | <br/>                      This field when selected true will retrieve the details of users like name, email, role, whether the user <br/>                      is active, when the user is created, updated and when user is deleted if deleted and deployments related to<br/>                      user etc. if this field is set to false then we only retrieve name and id of user, thus when chaining <br/>                      commands like delete or update user, please set details to true.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| should_include_deleted | <br/>                      If deleted users are to be included while querying all users. by default this is set to true because<br/>                      there might be cases where its preferable to see deleted users too. this can be set to false to see <br/>                      only users who dont have their credentials deleted.<br/>                      . Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| user_data.id | Number | The ID of User retrieved. this can be used to further link this user with                       user_id field of safebreach-update-user or safebreach-delete-user commands. | 
| user_data.name | String | The name of User retrieved. | 
| user_data.email | String | The email of User retrieved. this can be used for updating user or                       deleting user for input email of commands safebreach-update-user or safebreach-delete-user. | 

### safebreach-get-custom-scenarios

***

    This command  retrieves scenarios which are saved by user as custom scenarios. they generally have configurations and 
    everything set up and will be ready to run as tests. this command can be used to chain as predecessor for safebreach-
    requeue-test-simulation command and use the test-id parameter for requeuing the given test.
    

#### Base Command

`safebreach-get-custom-scenarios`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| schedule_details | Whether to get details of custom scenarios, <br/>                      set this to true every time unless you explicitly dont need details. Possible values are: false, true. Default is true. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| custom_scenarios.id | String | the Id of scenario. | 
| custom_scenarios.name | String | the name of the scenario. | 
| custom_scenarios.description | String | the description of the scenario. | 
| custom_scenarios.successCriteria | String | success criteria the scenario. | 
| custom_scenarios.originalScenarioId | String | original scenario id of scenario. | 
| custom_scenarios.actions_list | String | actions list of the scenario. | 
| custom_scenarios.edges_count | String | edges count for the scenario. | 
| custom_scenarios.steps_order | String | the order of steps of the scenario. | 
| custom_scenarios.createdAt | String | the creation datetime of the scenario. | 
| custom_scenarios.updatedAt | String | the last updated time the scenario. | 
| custom_scenarios.custom_data_object_for_rerun_scenario | String | the data which can be used for             rerun-simulation command. | 
| custom_scenarios.custom_data_for_rerun_test | String | the data which can be used for rerun-test command. | 

### safebreach-get-prebuilt-scenarios

***

    This command gets scenarios which are built by safebreach. They will be available by default even in new instance
    of your safebreach instance. They can be modified and saved as custom scenarios or used as it is.
    

#### Base Command

`safebreach-get-prebuilt-scenarios`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| prebuilt_scenarios.id | String | the Id of scenario. | 
| prebuilt_scenarios.name | String | the name of the scenario. | 
| prebuilt_scenarios.description | String | the description of the scenario. | 
| prebuilt_scenarios.createdBy | String | user id of user, who created the scenario. | 
| prebuilt_scenarios.createdAt | String | creation datetime of scenario. | 
| prebuilt_scenarios.updatedAt | String | the update datetime of the scenario. | 
| prebuilt_scenarios.recommended | String | the recommendation status of the scenario. | 
| prebuilt_scenarios.tags_list | String | the tags related to the scenario. | 
| prebuilt_scenarios.categories | String | the category ids of the scenario. | 
| prebuilt_scenarios.steps_order | String | the order of steps involved in the scenario. | 
| prebuilt_scenarios.order | String | the order of execution related to the scenario. | 
| prebuilt_scenarios.minApiVer | String | the minimum version of API required for scenario to be executed. | 

### safebreach-get-schedules

***
This command retrieves schedules from safebreach which user has set and they will display it to user.

#### Base Command

`safebreach-get-schedules`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| deleted | <br/>                      If this field is set to true then deleted schedules will be retrieved too for information, <br/>                      Unless it is required to search old and deleted schedules, keep this selection as false.<br/>                      . Possible values are: true, false. Default is false. | Optional | 
| details | <br/>                      Should details tests be included in result, if this field is not selected to true then only name <br/>                      and id will be retrieved and anything else is ignored, so if we want information on detailed schedule<br/>                      structure and planning , keep this selected to true. else keep this false.<br/>                      . Possible values are: true, false. Default is true. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| schedules.id | String | the Id of the schedule. | 
| schedules.isEnabled | Boolean | if simulation is enabled. | 
| schedules.name | String | the name of the schedule. | 
| schedules.cronString | String | the cron expression the schedule. | 
| schedules.user_schedule | String | the user readable form of the schedule. | 
| schedules.runDate | String | the run date of the schedule. | 
| schedules.cronTimezone | String | the time zone of the schedule. | 
| schedules.taskId | String | the plan ID of the schedule. | 
| schedules.description | String | the description of the schedule. | 
| schedules.matrixId | String | the matrix ID of the schedule. | 
| schedules.createdAt | String | the creation datetime of the schedule. | 
| schedules.updatedAt | String | the updated datetime of the schedule. | 
| schedules.deletedAt | String | the deletion time of the schedule. | 

### safebreach-get-services-status

***

    This command retrieves status of services from safebreach and shows them as table for user, incase they are down then
    from when they are down or when it was last up will also be shown here.
    

#### Base Command

`safebreach-get-services-status`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| services_status.name | String | the name of the service. | 
| services_status.version | String | version of the service. | 
| services_status.connection status | String | connection status of service. | 
| services_status.error | String | error status of service. | 

### safebreach-get-available-simulator-count

***
This command gives all details related to account, we are using this to find assigned simulator quota.

#### Base Command

`safebreach-get-available-simulator-count`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| account_details.id | Number | The account ID which is being used by integration. | 
| account_details.name | String | The Account Name of account being queried. | 
| account_details.contactName | String | Contact name for given account. | 
| account_details.contactEmail | String | Email of the contact person. | 
| account_details.userQuota | String | User Quota for the given account, the max number of users which are allowed for the account. | 
| account_details.nodesQuota | Number | The simulator quota for the given account. the maximum number of simulators                        which are permitted for the account. | 
| account_details.registrationDate | Number | The registration date of given account. | 
| account_details.activationDate | String | The Activation date of given account. | 
| account_details.expirationDate | String | Account expiration date. | 

### safebreach-get-simulator-with-name

***
This command gives simulator with given name.

#### Base Command

`safebreach-get-simulator-with-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| simulator_or_node_name | <br/>                      Name of simulator/node to search with. this is name which will be used to search the list of simulators <br/>                      which will be retrieved and of which whose name matches this input value.<br/>                      . | Required | 
| details | <br/>                      If simulator details are to be retrieved while searching. this should be selected to true if the command is<br/>                      "safebreach-get-simulator-with-name" and if its false then only very small number of fields will be <br/>                      retrieved thus making search with name impossible.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| deleted | if deleted are to be included for search. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| simulator_details_with_name.is_enabled | String | Whether the node is enabled or not. | 
| simulator_details_with_name.simulator_id | String | The Id of given simulator. | 
| simulator_details_with_name.name | String | name for given simulator. | 
| simulator_details_with_name.account_id | String | Account Id of account Hosting given simulator. | 
| simulator_details_with_name.is_critical | String | Whether the simulator is critical. | 
| simulator_details_with_name.is_exfiltration | String | If Simulator is exfiltration target. | 
| simulator_details_with_name.is_infiltration | String | If simulator is infiltration target. | 
| simulator_details_with_name.is_mail_target | String | If simulator is mail target. | 
| simulator_details_with_name.is_mail_attacker | String | If simulator is mail attacker. | 
| simulator_details_with_name.is_pre_executor | String | Whether the node is pre executor. | 
| simulator_details_with_name.is_aws_attacker | String | if the given simulator is aws attacker. | 
| simulator_details_with_name.is_azure_attacker | String | If the given simulator is azure attacker. | 
| simulator_details_with_name.external_ip | String | external ip of given simulator. | 
| simulator_details_with_name.internal_ip | String | internal ip of given simulator. | 
| simulator_details_with_name.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| simulator_details_with_name.preferred_interface | String | Preferred simulator interface. | 
| simulator_details_with_name.preferred_ip | String | Preferred Ip of simulator. | 
| simulator_details_with_name.hostname | String | Hostname of given simulator. | 
| simulator_details_with_name.connection_type | String | connection_type of given simulator. | 
| simulator_details_with_name.simulator_status | String | status of the simulator. | 
| simulator_details_with_name.connection_status | String | connection status of node/simulator. | 
| simulator_details_with_name.simulator_framework_version | String | Framework version of simulator. | 
| simulator_details_with_name.operating_system_type | String | operating system type of given simulator. | 
| simulator_details_with_name.operating_system | String | Operating system of given simulator. | 
| simulator_details_with_name.execution_hostname | String | Execution Hostname of the given node. | 
| simulator_details_with_name.deployments | String | deployments simulator is part of. | 
| simulator_details_with_name.created_at | String | Creation datetime of simulator. | 
| simulator_details_with_name.updated_at | String | Update datetime of given simulator. | 
| simulator_details_with_name.deleted_at | String | deletion datetime of given simulator. | 
| simulator_details_with_name.assets | String | Assets of given simulator. | 
| simulator_details_with_name.simulation_users | String | simulator users list. | 
| simulator_details_with_name.proxies | String | Proxies of simulator. | 
| simulator_details_with_name.advanced_actions | String | Advanced simulator details. | 

### safebreach-get-user-with-matching-name-or-email

***
This command gives all users depending on inputs given.

#### Base Command

`safebreach-get-user-with-matching-name-or-email`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| name | <br/>                      Name of the user to lookup. This will first retrieve all users and show details related to <br/>                      name entered here. this name will be search of if name is part of name given to user and not <br/>                      a perfect match. For example if actual name is 'demisto' but if input is 'dem', even then this<br/>                      will be shown as a valid match to name. This is so that command user need not know exact name of<br/>                      user and just searching first name or last name will work.<br/>                      . | Optional | 
| email | <br/>                      Email of the user to lookup. This will be used to retrieve user with matching email that user entered<br/>                      partial email search doesn't work here.<br/>                      . | Required | 
| should_include_details | <br/>                      This field when selected true will retrieve the details of users like name, email, role, whether the user <br/>                      is active, when the user is created, updated and when user is deleted if deleted and deployments related to<br/>                      user etc. if this field is set to false then we only retrieve name and id of user, thus when chaining <br/>                      commands like delete or update user, please set details to true.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| should_include_deleted | <br/>                      If deleted users are to be included while querying all users. by default this is set to true because<br/>                      there might be cases where its preferable to see deleted users too. this can be set to false to see <br/>                      only users who dont have their credentials deleted.<br/>                      . Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| filtered_users.id | Number | The ID of User retrieved. this can be used to further link this user with user_id field of                        safebreach-update-user or safebreach-delete-user commands. | 
| filtered_users.name | String | The name of User retrieved. | 
| filtered_users.email | String | The email of User retrieved. this can be used for updating user or deleting user                        for input email of commands safebreach-update-user or safebreach-delete-user. | 

### safebreach-get-verification-token

***

    This command retrieves existing verification token needed for verification of the simulators.
    

#### Base Command

`safebreach-get-verification-token`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| verification_token.token | String | the value of new verification token. | 

### safebreach-pause-resume-simulations-tests

***

    This command gets simulations/tests which are in running or queued state and pauses/resumes them based on input selected.
    the state selected will be applied for all running/queued state tasks whether they are simulations or tests.
    

#### Base Command

`safebreach-pause-resume-simulations-tests`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| simulation_or_test_state | State of tests/simulators to set to:<br/>                       1. pause will set all simulations/tests which are in queue/running to paused stated and resume all <br/>                       will be the state of button in running simulations page.<br/>                       2. resume will queue all simulations/tests and will set them to running/queued state depending on priority.<br/>                       Note that this doe not affect the schedules and scheduled tasks unless they are running or active at the<br/>                       moment of execution of the command.<br/>                       . Possible values are: resume, pause. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| simulations_tests_status.status | String | the status of the simulations/tests. | 

### safebreach-rerun-simulation

***
this commands puts given simulation data at a given position, for this command to get test data input,        run safebreach-custom-scenarios-list and copy field 'data for rerun simulation' from table.

#### Base Command

`safebreach-rerun-simulation`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| position | position in queue to put the given simulation data at. | Optional | 
| enable_feedback_loop | this argument is used to enable/disable feedback loop. Possible values are: false, true. Default is true. | Optional | 
| retry_simulation | this argument is used to retry according to retry policy                 mention in retry policy field. Possible values are: , false, true. | Optional | 
| wait_for_retry | this arguments tells flow to retry the adding to queue after the                 current step execution is completed. Possible values are: , false, true. | Optional | 
| priority | the priority of this simulation action. Possible values are: low, high. Default is low. | Optional | 
| simulation_data | simulation data for the given simulation. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| changed_data.id | String | the Id of scenario. | 
| changed_data.name | String | the name of the scenario. | 
| changed_data.description | String | the description of the scenario. | 
| changed_data.successCriteria | String | success criteria the scenario. | 
| changed_data.originalScenarioId | String | original scenario id of scenario. | 
| changed_data.actions_list | String | actions list of the scenario. | 
| changed_data.edges_count | String | edges count for the scenario. | 
| changed_data.steps_order | String | the order of steps of the scenario. | 
| changed_data.createdAt | String | the creation datetime of the scenario. | 
| changed_data.updatedAt | String | the last updated time the scenario. | 

### safebreach-rerun-simulation2

***
this commands puts given simulation data at a given position, for this command to get test data input,        run safebreach-custom-scenarios-list and copy field 'data for rerun simulation' from table.

#### Base Command

`safebreach-rerun-simulation2`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| position | position in queue to put the given simulation data at. | Optional | 
| enable_feedback_loop | this argument is used to enable/disable feedback loop. Possible values are: false, true. Default is true. | Optional | 
| retry_simulation | this argument is used to retry according to retry policy                 mention in retry policy field. Possible values are: , false, true. | Optional | 
| wait_for_retry | this arguments tells flow to retry the adding to queue after the                 current step execution is completed. Possible values are: , false, true. | Optional | 
| priority | the priority of this simulation action. Possible values are: low, high. Default is low. | Optional | 
| simulation_id | simulation id for the given simulation, can be retrieved from running get prebuilt scenarios                       or custom scenarios command and then getting id field from them. | Required | 
| simulation_name | simulation name for the given simulation. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| changed_data.id | String | the Id of scenario. | 
| changed_data.name | String | the name of the scenario. | 
| changed_data.description | String | the description of the scenario. | 
| changed_data.successCriteria | String | success criteria the scenario. | 
| changed_data.originalScenarioId | String | original scenario id of scenario. | 
| changed_data.actions_list | String | actions list of the scenario. | 
| changed_data.edges_count | String | edges count for the scenario. | 
| changed_data.steps_order | String | the order of steps of the scenario. | 
| changed_data.createdAt | String | the creation datetime of the scenario. | 
| changed_data.updatedAt | String | the last updated time the scenario. | 

### safebreach-rerun-test2

***
this commands puts given test data at a given position, for this command to get test data input,        run safebreach-custom-scenarios-list and copy field 'data for rerun test' from table.

#### Base Command

`safebreach-rerun-test2`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| position | position in queue to put the given test data at. | Optional | 
| enable_feedback_loop | this argument is used to enable/disable feedback loop. Possible values are: false, true. Default is true. | Optional | 
| retry_simulation | this argument is used to retry according to retry policy                 mention in retry policy field. Possible values are: , false, true. | Optional | 
| wait_for_retry | this arguments tells flow to retry the adding to queue after the                 current step execution is completed. Possible values are: , false, true. | Optional | 
| priority | the priority of this test action. Possible values are: low, high. Default is low. | Optional | 
| retry_policy | the retry policy of test. | Optional | 
| test_id | test id for the given test,             this is be planRunId field from get-all-tests-summary command. | Required | 
| test_name | test name for the given test. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| changed_data.id | String | the Id of scenario. | 
| changed_data.name | String | the name of the scenario. | 
| changed_data.description | String | the description of the scenario. | 
| changed_data.successCriteria | String | success criteria the scenario. | 
| changed_data.originalScenarioId | String | original scenario id of scenario. | 
| changed_data.actions_list | String | actions list of the scenario. | 
| changed_data.edges_count | String | edges count for the scenario. | 
| changed_data.steps_order | String | the order of steps of the scenario. | 
| changed_data.createdAt | String | the creation datetime of the scenario. | 
| changed_data.updatedAt | String | the last updated time the scenario. | 
| changed_data.planId | String | the plan id of the scenario. | 
| changed_data.ranBy | String | the user id of the user who ran the scenario. | 
| changed_data.ranFrom | String | where the user ran the scenario from. | 
| changed_data.enableFeedbackLoop | String | feedback loop status of the scenario. | 
| changed_data.planRunId | String | plan run id of the scenario. | 
| changed_data.priority | String | priority of the scenario. | 
| changed_data.retrySimulations | String | retry status of the scenario. | 

### safebreach-rotate-verification-token

***

    This command rotates generated verification token meaning it creates a new token which will be used for verification 
    of simulator and adding the simulator.
    

#### Base Command

`safebreach-rotate-verification-token`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| Safebreach Content Management.new_token | String | new Token which has been generated due to the api call. | 

### safebreach-update-deployment

***

    This command updates a deployment with given data. The deployment_id field of this command can  be retrieved from 
    get-all-deployments command. If the user wants to search with deployment ID then they can search it that way or 
    if user just wants to search with name then they can just give name field and the command internally searches the deployment 
    with given name and updates it.
    

#### Base Command

`safebreach-update-deployment`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| deployment_id | <br/>                      ID of the deployment to update. this can be searched with list-deployments command or<br/>                      from UI. this will be taken as id of deployment whose properties we want to update.<br/>                      . | Optional | 
| deployment_name | <br/>                      Name of the deployment to search whose data will be updated. This field is not the field whose<br/>                      data will be used to update name of given to the value instead this field is for searching deployment <br/>                      with the value as name. This field will be used to search the existing deployment names and find a <br/>                      deployment whose name matches this and that will be used as deployment whose data we are updating. <br/>                      . | Required | 
| updated_nodes_for_deployment | <br/>                      Comma separated ID of all nodes the deployment should be part of. These nodes can be<br/>                      retrieved by calling get-all-available-simulator-details command and that command will<br/>                      show the results of the all available simulators and the ids of those nodes can be used as<br/>                      comma separated values in this field for those nodes to act as a group.<br/>                      . | Optional | 
| updated_deployment_name | <br/>                      This fields value will be the name which the deployment name will be updated to. <br/>                      . | Optional | 
| updated_deployment_description | description of the deployment to which value this should be updated to. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_deployment_data.id | Number | The ID of deployment whose values have been updated.                           ID cant be changed so this wont be updated. | 
| updated_deployment_data.accountId | String | The accountId of user who created the deployment. | 
| updated_deployment_data.name | String | The name of deployment which has been updated to the name given in updated_deployment_name.                        this will be the name shown in deployment name field of table in deployments page in safebreach UI. | 
| updated_deployment_data.createdAt | String | The creation date and time of deployment whose data has been updated. | 
| updated_deployment_data.updatedAt | String | The last updated date and time of deployment whose data has been updated.                       This will generally be closer to the update deployment command run time for reference. | 
| updated_deployment_data.description | String | The updated description of deployment which is provided in updated_deployment_description                       field of input . This will now be the description which is shown in description field of deployments                       table of safebreach UI. | 
| updated_deployment_data.nodes | String | The nodes that are part of deployment. unless any nodes are given as input this field wont                       be updated this field doesn't reflect changes if nodes given as input are deleted. | 

### safebreach-update-simulator-with-given-name

***

    This command updates simulator with given name with given details in simulator_or_node_name. then the given inputs for update
    fields will be updated to the selected filed values will be updated to given value.
    

#### Base Command

`safebreach-update-simulator-with-given-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| simulator_or_node_name | <br/>                      Name of simulator/node to search with. this is name which will be used to search the list of simulators <br/>                      which will be retrieved and of which whose name matches this input value.<br/>                      . | Required | 
| details | <br/>                      If simulator details are to be retrieved while searching. this should be selected to true if the command is<br/>                      "safebreach-get-simulator-with-name" and if its false then only very small number of fields will be <br/>                      retrieved thus making search with name impossible.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| deleted | <br/>                      If deleted are to be included for search. Incase the simulator we are searching for is deleted one then<br/>                      set this to true and then search. else keep it as default and set to false.<br/>                      . Possible values are: true, false. Default is true. | Required | 
| connection_url | <br/>                  the given value will be set as connection string, meaning this can be used to connect to<br/>                  this URL.<br/>                  . | Optional | 
| cloud_proxy_url | the given value will be set as cloud proxy url. | Optional | 
| name | <br/>                  the given value will be set as name of simulator. this will be the name of simulator once the command runs.<br/>                  . | Optional | 
| preferred_interface | <br/>                  the given value will be set as preferred interface.<br/>                  . | Optional | 
| preferred_ip | <br/>                  the given value will be set as Preferred IP to connect to the simulator.<br/>                  . | Optional | 
| tunnel | <br/>                  the given value will be set as tunnel.<br/>                  . | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| updated_simulator_details.simulator_id | String | The Id of given simulator. | 
| updated_simulator_details.name | String | name for given simulator. | 
| updated_simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| updated_simulator_details.is_critical | String | Whether the simulator is critical. | 
| updated_simulator_details.is_exfiltration | String | If Simulator is exfiltration target. | 
| updated_simulator_details.is_infiltration | String | If simulator is infiltration target. | 
| updated_simulator_details.is_mail_target | String | If simulator is mail target. | 
| updated_simulator_details.is_mail_attacker | String | If simulator is mail attacker. | 
| updated_simulator_details.is_pre_executor | String | Whether the node is pre executor. | 
| updated_simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| updated_simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| updated_simulator_details.external_ip | String | external ip of given simulator. | 
| updated_simulator_details.internal_ip | String | internal ip of given simulator. | 
| updated_simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| updated_simulator_details.preferred_interface | String | Preferred simulator interface. | 
| updated_simulator_details.preferred_ip | String | Preferred Ip of simulator. | 
| updated_simulator_details.hostname | String | Hostname of given simulator. | 
| updated_simulator_details.connection_type | String | connection_type of given simulator. | 
| updated_simulator_details.simulator_status | String | status of the simulator. | 
| updated_simulator_details.connection_status | String | connection status of node/simulator. | 
| updated_simulator_details.simulator_framework_version | String | Framework version of simulator. | 
| updated_simulator_details.operating_system_type | String | operating system type of given simulator. | 
| updated_simulator_details.operating_system | String | Operating system of given simulator. | 
| updated_simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| updated_simulator_details.deployments | String | deployments simulator is part of. | 
| updated_simulator_details.created_at | String | Creation datetime of simulator. | 
| updated_simulator_details.updated_at | String | Update datetime of given simulator. | 
| updated_simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| updated_simulator_details.assets | String | Assets of given simulator. | 
| updated_simulator_details.simulation_users | String | simulator users list. | 
| updated_simulator_details.proxies | String | Proxies of simulator. | 
| updated_simulator_details.advanced_actions | String | Advanced simulator details. | 

### safebreach-update-user-details

***
This command updates a user with given data.

#### Base Command

`safebreach-update-user-details`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| user_id | user ID of user from safebreach to search. this can be retrieved in 2 ways,<br/>                      1. run get-all-users command and then look for user id of user with matching criteria<br/>                      but to see details its required that details parameter to be set to true,<br/>                      2. if you know user name or email then those can be used in safebreach-get-user-with-given-name-or-email<br/>                      command and then search for user with required details in displayed results for ID.<br/>                      This field is not  required, meaning even if just email is given , we will internally search user<br/>                      id with the matching email and use the user for further process. | Optional | 
| email | Email of the user to Search for updating user details. This is a required field.<br/>                      The user with matching email will be considered as user whose data will be updated. | Required | 
| name | <br/>                      Update the user name to given value of this field, <br/>                      unless this field is left empty, whatever is present here will be updated to user details.<br/>                      user will be selected based on user_id or email fields mentioned above.<br/>                      . | Optional | 
| user_description | <br/>                      Update the user Description to given value in this field. This will be updated description of user<br/>                      unless this field is left empty, whatever is present here will be updated to user details.<br/>                      user will be selected based on user_id or email fields mentioned above.<br/>                      . | Optional | 
| is_active | <br/>                      Update the user Status based on the input, if this is set to false then user will be deactivated.<br/>                      unless this field is left empty, whatever is present here will be updated to user details.<br/>                      user will be selected based on user_id or email fields mentioned above.<br/>                      . Possible values are: true, false, . | Optional | 
| password | <br/>                      Password of user to be updated with. this will be used for changing password for user.<br/>                      unless this field is left empty, whatever is present here will be updated to user details.<br/>                      user will be selected based on user_id or email fields mentioned above.<br/>                      . | Optional | 
| user_role | <br/>                      Role of the user to be changed to. unless you want to change the user role and permissions, <br/>                      dont select anything in this field, user will be selected based on user_id or email fields mentioned above.<br/>                      . Possible values are: viewer, administrator, contentDeveloper, operator. | Optional | 
| deployments | <br/>                        Comma separated ID of all deployments the user should be part of.<br/>                        unless this field is left empty, whatever is present here will be updated to user details.<br/>                        user will be selected based on user_id or email fields mentioned above.<br/>                      . | Optional | 
| should_include_details | <br/>                      This field when selected true will retrieve the details of users like name, email, role, whether the user <br/>                      is active, when the user is created, updated and when user is deleted if deleted and deployments related to<br/>                      user etc. if this field is set to false then we only retrieve name and id of user, thus when chaining <br/>                      commands like delete or update user, please set details to true.<br/>                      . Possible values are: true, false. Default is true. | Optional | 
| should_include_deleted | <br/>                      If deleted users are to be included while querying all users. by default this is set to true because<br/>                      there might be cases where its preferable to see deleted users too. this can be set to false to see <br/>                      only users who dont have their credentials deleted.<br/>                      . Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_user_data.id | Number | The ID of User whose data has been updated. | 
| updated_user_data.name | String | The name of User after running the update command according to safebreach records. | 
| updated_user_data.email | String | the email of the user whose data has been updated by the command. | 
| updated_user_data.createdAt | String | the time at which the user who has been selected has been created. | 
| updated_user_data.updatedAt | String | The last updated time of User selected for update.                        this will be the execution time for the command or close to it. | 
| updated_user_data.deletedAt | String | The Deletion time of User selected to update. Generally this is empty unless                       user chosen to update is a deleted user. | 
| updated_user_data.roles | String | The roles of User updated. these will change if role has been updated during                       updating user details else they will be same as pre update. | 
| updated_user_data.description | String | The description of User after updating user, if description field has been given any                       new value during update then its updated else this will be left unchanged from previous value. | 
| updated_user_data.role | String | The roles and permissions related to user who has been selected for update.unless this field                       has been given a value , this will not be updated and will stay the same as previous value. | 
| updated_user_data.deployments | String | The deployments related to user, this will be comma separated values of deployment IDs. | 
