This Integration aims to provide easy access to safebreach from XSOAR.        Following are the things that user can get access through XSOAR command integration:         1. User get, create, update and delete.         2. Deployment create, update and delete.         3. Tests get and delete.         4. Nodes get, update, delete. 

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

4. Click **Test** to validate the URLs, token, and connection.

## Commands

You can execute these commands from the Cortex XSOAR CLI, as part of an automation, or in a playbook.
After you successfully execute a command, a DBot message appears in the War Room with the command details.

### safebreach-generate-api-key

***
This command creates a API Key with given data.

#### Base Command

`safebreach-generate-api-key`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Name | Name of the API Key to create. | Required | 
| Description | Description of the API Key to create. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| generated_api_key.name | Number | The Name of API Key created. | 
| generated_api_key.description | String | The Description of API Key created. | 
| generated_api_key.createdBy | String | The User ID of API key creator. | 
| generated_api_key.createdAt | String | The creation time of API key. | 
| generated_api_key.key | String | The API key Value. | 
| generated_api_key.roles | String | The roles allowed for this api key. | 
| generated_api_key.role | String | The role of API Key. | 

### safebreach-create-deployment

***
This command creates a deployment with given data.

#### Base Command

`safebreach-create-deployment`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Name | Name of the deployment to create. | Optional | 
| Description | Description of the deployment to create. | Optional | 
| Nodes | Comma separated ID of all nodes the deployment should be part of. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| created_deployment_data.id | Number | The ID of deployment created. | 
| created_deployment_data.accountId | String | The account of deployment created. | 
| created_deployment_data.name | String | The name of deployment created. | 
| created_deployment_data.createdAt | String | The creation time of deployment created. | 
| created_deployment_data.description | String | The description of deployment created. | 
| created_deployment_data.nodes | String | The nodes that are part of deployment. | 

### safebreach-create-user

***
This command creates a user with given data.

#### Base Command

`safebreach-create-user`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Name | Name of the user to create. | Optional | 
| Email | Email of the user to Create. | Required | 
| Is Active | Whether the user is active upon creation. Possible values are: true, false. Default is false. | Optional | 
| Email Post Creation | Should Email be sent to user on creation. Possible values are: true, false. Default is false. | Optional | 
| Password | Password of user being created. | Required | 
| Admin Name | Name of the Admin creating user. | Optional | 
| Change Password on create | Should user change password on creation. Possible values are: true, false. Default is false. | Optional | 
| User role | Role of the user being Created. Possible values are: viewer, administrator, contentDeveloper, operator. Default is viewer. | Optional | 
| Deployments | Comma separated ID of all deployments the user should be part of. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| created_user_data.id | Number | The ID of User created. | 
| created_user_data.name | String | The name of User created. | 
| created_user_data.email | String | The email of User created. | 
| created_user_data.createdAt | String | The creation time of User created. | 
| created_user_data.deletedAt | String | The Deletion time of User created. | 
| created_user_data.roles | String | The roles of User created. | 
| created_user_data.description | String | The description of User created. | 
| created_user_data.role | String | The role of User created. | 
| created_user_data.deployments | String | The deployments user is part of. | 

### safebreach-delete-api-key

***
This command deletes a API key with given name.

#### Base Command

`safebreach-delete-api-key`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Key Name | Name of the API Key to Delete. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_api_key.name | Number | The Name of API Key deleted. | 
| deleted_api_key.description | String | The Description of API Key deleted. | 
| deleted_api_key.createdBy | String | The User ID of API key creator. | 
| deleted_api_key.createdAt | String | The creation time of API key. | 
| deleted_api_key.deletedAt | String | The deletion time of API key. | 

### safebreach-delete-deployment

***
This command deletes a deployment with given data.

#### Base Command

`safebreach-delete-deployment`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Deployment ID | Name of the deployment to update. | Optional | 
| Deployment Name | Description of the deployment to update. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_deployment_data.id | Number | The ID of deployment created. | 
| deleted_deployment_data.accountId | String | The account of deployment created. | 
| deleted_deployment_data.name | String | The name of deployment created. | 
| deleted_deployment_data.createdAt | String | The creation time of deployment created. | 
| deleted_deployment_data.description | String | The description of deployment created. | 
| deleted_deployment_data.nodes | String | The nodes that are part of deployment. | 

### safebreach-delete-integration-errors

***
This command deleted connector related errors.

#### Base Command

`safebreach-delete-integration-errors`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Connector ID | The connector ID of Integration connector to have its errors deleted. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| errors_cleared.error | Number | Error count after deletion of errors for the given connector. | 
| errors_cleared.result | String | error deletion status whether true or false. | 

### safebreach-delete-simulator-with-name

***
This command deletes simulator with given name.

#### Base Command

`safebreach-delete-simulator-with-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Simulator/Node Name | Name of simulator/node to search with. | Required | 
| Should Force Delete | Should we force delete the simulator. Possible values are: true, false. Default is false. | Required | 
| details | if details are to be included for search. Possible values are: true, false. Default is true. | Optional | 
| deleted | if deleted are to be included for search. Possible values are: true, false. Default is true. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| deleted_simulator_details.simulator_id | String | The Id of given simulator. | 
| deleted_simulator_details.name | String | name for given simulator. | 
| deleted_simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| deleted_simulator_details.is_critical | String | Whether the simulator is critical. | 
| deleted_simulator_details.is_exfiltration | Number | If Simulator is exfiltration target. | 
| deleted_simulator_details.is_infiltration | Number | If simulator is infiltration target. | 
| deleted_simulator_details.is_mail_target | Number | If simulator is mail target. | 
| deleted_simulator_details.is_mail_attacker | Number | If simulator is mail attacker. | 
| deleted_simulator_details.is_pre_executor | Number | Whether the node is pre executor. | 
| deleted_simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| deleted_simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| deleted_simulator_details.external_ip | String | external ip of given simulator. | 
| deleted_simulator_details.internal_ip | String | internal ip of given simulator. | 
| deleted_simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| deleted_simulator_details.preferred_interface | Number | Preferred simulator interface. | 
| deleted_simulator_details.preferred_ip | Number | Preferred Ip of simulator. | 
| deleted_simulator_details.hostname | String | Hostname of given simulator. | 
| deleted_simulator_details.connection_type | String | connection_type of given simulator. | 
| deleted_simulator_details.simulator_status | String | status of the simulator. | 
| deleted_simulator_details.connection_status | Number | connection status of node/simulator. | 
| deleted_simulator_details.simulator_framework_version | Number | Framework version of simulator. | 
| deleted_simulator_details.operating_system_type | String | operating system type of given simulator. | 
| deleted_simulator_details.operating_system | String | Operating system of given simulator. | 
| deleted_simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| deleted_simulator_details.deployments | Number | deployments simulator is part of. | 
| deleted_simulator_details.created_at | Number | Creation datetime of simulator. | 
| deleted_simulator_details.updated_at | String | Update datetime of given simulator. | 
| deleted_simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| deleted_simulator_details.assets | String | Assets of given simulator. | 
| deleted_simulator_details.simulation_users | Number | simulator users list. | 
| deleted_simulator_details.proxies | Number | Proxies of simulator. | 
| deleted_simulator_details.advanced_actions | Number | Advanced simulator details. | 

### safebreach-delete-test-summary-of-given-test

***
This command deletes tests with given plan ID.

#### Base Command

`safebreach-delete-test-summary-of-given-test`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Test ID | number of entries per page to be retrieved. | Optional | 
| Soft Delete | Should archived tests be included in search. Possible values are: true, false. Default is true. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_test_results.planId | String | Plan ID of the simulation. | 
| deleted_test_results.planName | String | Plan Name of the simulation. | 
| deleted_test_results.securityActionPerControl | String | Security Actions of the simulation. | 
| deleted_test_results.planRunId | String | Plan Run ID of the simulation. | 
| deleted_test_results.runId | String | Run ID of the simulation. | 
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
| User ID | user ID of user from safebreach to search. | Optional | 
| Email | Email of the user to Search for updating user details. | Required | 
| Should Include Details | If Details of user are to be included while             querying all users. Possible values are: true, false. Default is true. | Optional | 
| Should Include Deleted | If deleted users are to be included while querying all users. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_user_data.id | Number | The ID of User deleted. | 
| deleted_user_data.name | String | The name of User deleted. | 
| deleted_user_data.email | String | The email of User deleted. | 
| deleted_user_data.createdAt | String | The creation time of User deleted. | 
| deleted_user_data.deletedAt | String | The Deletion time of User deleted. | 
| deleted_user_data.roles | String | The roles of User deleted. | 
| deleted_user_data.description | String | The description of User deleted. | 
| deleted_user_data.role | String | The role of User deleted. | 
| deleted_user_data.deployments | String | The deployments user was part of. | 

### safebreach-get-integration-errors

***
This command gives all connector related errors.

#### Base Command

`safebreach-get-integration-errors`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| integration_errors.connector | Number | The connector ID of Integration connector retrieved. | 
| integration_errors.action | String | The action of Integration connector error. | 
| integration_errors.success | String | status of connector error. | 
| integration_errors.error | String | Error description. | 
| integration_errors.timestamp | String | Time of error. | 

### safebreach-get-available-simulator-details

***
We are using this command to get all available simulators.

#### Base Command

`safebreach-get-available-simulator-details`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| details | if details are to be included for search. Possible values are: true, false. Default is true. | Required | 
| deleted | if deleted are to be included for search. Possible values are: true, false. Default is true. | Required | 
| secret | if secrets are to be included for search. Possible values are: true, false. | Optional | 
| shouldIncludeProxies | if proxies are to be included for search. Possible values are: true, false. | Optional | 
| hostname | if hostname to be included for search. Possible values are: true, false. | Optional | 
| connectionType | if connectionType to be included for search. Possible values are: true, false. | Optional | 
| externalIp | if external IP details to be included for search. | Optional | 
| internalIp | if Internal IP are to be included for search. | Optional | 
| os | if Operating system details to be included for search. Possible values are: true, false. | Optional | 
| sortDirection | direction in which secrets are to be sorted. Possible values are: asc, desc. Default is asc. | Optional | 
| startRow | if there are too many entries then where should we start looking from. | Optional | 
| pageSize | number of entries to search. | Optional | 
| isEnabled | if to search only enabled ones. Possible values are: true, false. | Optional | 
| isConnected | status of connection of nodes to search. Possible values are: true, false. | Optional | 
| isCritical | whether to search only for critical nodes or not. Possible values are: true, false. | Optional | 
| assets | Whether search only for assets and which assets. | Optional | 
| additionalDetails | Whether to show additional details or not. Possible values are: true, false. | Optional | 
| impersonatedUsers | should search only for impersonated user targets or not. Possible values are: true, false. | Optional | 
| isAzureAttacker | Whether to search only for azure attackers. Possible values are: true, false. | Optional | 
| isAwsAttacker | Whether to search only for aws attacker. Possible values are: true, false. | Optional | 
| isPreExecutor | should search only for pre-executors or not. Possible values are: true, false. | Optional | 
| isInfiltrationTarget | Whether to search only for infiltration targets. Possible values are: true, false. | Optional | 
| isMailTarget | Whether to search only for Mail targets. Possible values are: true, false. | Optional | 
| isExfiltrationTarget | should search only for exfiltration targets or not. Possible values are: true, false. | Optional | 
| deployments | deployments list which the search should look. | Optional | 
| advancedActions | advanced actions to search. | Optional | 
| roles | roles to search. | Optional | 
| userids | userids to search. | Optional | 
| versions | versions to filter by. | Optional | 
| proxyIds | proxy ids to search. | Optional | 
| assetIds | asset ids to search. | Optional | 
| status | if simulator status are to be included for search. Possible values are: APPROVED, PENDING, ALL. Default is ALL. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| simulator_details.simulator_id | String | The Id of given simulator. | 
| simulator_details.name | String | name for given simulator. | 
| simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| simulator_details.is_critical | String | Whether the simulator is critical. | 
| simulator_details.is_exfiltration | Number | If Simulator is exfiltration target. | 
| simulator_details.is_infiltration | Number | If simulator is infiltration target. | 
| simulator_details.is_mail_target | Number | If simulator is mail target. | 
| simulator_details.is_mail_attacker | Number | If simulator is mail attacker. | 
| simulator_details.is_pre_executor | Number | Whether the node is pre executor. | 
| simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| simulator_details.external_ip | String | external ip of given simulator. | 
| simulator_details.internal_ip | String | internal ip of given simulator. | 
| simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| simulator_details.preferred_interface | Number | Preferred simulator interface. | 
| simulator_details.preferred_ip | Number | Preferred Ip of simulator. | 
| simulator_details.hostname | String | Hostname of given simulator. | 
| simulator_details.connection_type | String | connection_type of given simulator. | 
| simulator_details.simulator_status | String | status of the simulator. | 
| simulator_details.connection_status | Number | connection status of node/simulator. | 
| simulator_details.simulator_framework_version | Number | Framework version of simulator. | 
| simulator_details.operating_system_type | String | operating system type of given simulator. | 
| simulator_details.operating_system | String | Operating system of given simulator. | 
| simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| simulator_details.deployments | Number | deployments simulator is part of. | 
| simulator_details.created_at | Number | Creation datetime of simulator. | 
| simulator_details.updated_at | String | Update datetime of given simulator. | 
| simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| simulator_details.assets | String | Assets of given simulator. | 
| simulator_details.simulation_users | Number | simulator users list. | 
| simulator_details.proxies | Number | Proxies of simulator. | 
| simulator_details.advanced_actions | Number | Advanced simulator details. | 

### safebreach-get-test-summary

***
This command gets tests with given modifiers.

#### Base Command

`safebreach-get-test-summary`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Include Archived | Should archived tests be included in search. Possible values are: true, false. Default is true. | Optional | 
| Entries per Page | number of entries per page to be retrieved. | Optional | 
| Plan ID | plan Id of test. | Optional | 
| Status | Status of simulation. Possible values are: CANCELED, COMPLETED. Default is CANCELED. | Optional | 
| Simulation ID | Unique ID of the simulation. | Optional | 
| Sort By | sort by option. Possible values are: endTime, startTime, planRunId, stepRunId. Default is endTime. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| test_results.planId | String | Plan ID of the simulation. | 
| test_results.planName | String | Plan Name of the simulation. | 
| test_results.securityActionPerControl | String | Security Actions of the simulation. | 
| test_results.planRunId | String | Plan Run ID of the simulation. | 
| test_results.runId | String | Run ID of the simulation. | 
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
This command gets tests with given plan ID.

#### Base Command

`safebreach-get-test-summary-with-plan-run-id`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Include Archived | Should archived tests be included in search. Possible values are: true, false. Default is true. | Optional | 
| Entries per Page | number of entries per page to be retrieved. | Optional | 
| Plan ID | plan Id of test. | Required | 
| Status | Status of simulation. Possible values are: CANCELED, COMPLETED. | Optional | 
| Simulation ID | Unique ID of the simulation. | Optional | 
| Sort By | sort by option. Possible values are: endTime, startTime, planRunId, stepRunId. Default is endTime. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| test_results.planId | String | Plan ID of the simulation. | 
| test_results.planName | String | Plan Name of the simulation. | 
| test_results.securityActionPerControl | String | Security Actions of the simulation. | 
| test_results.planRunId | String | Plan Run ID of the simulation. | 
| test_results.runId | String | Run ID of the simulation. | 
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
| Should Include Details | If Details of user are to be included while querying all             users. Possible values are: true, false. Default is true. | Optional | 
| Should Include Deleted | If deleted users are to be included while querying all users. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| user_data.id | Number | The ID of User retrieved. | 
| user_data.name | String | The name of User retrieved. | 
| user_data.email | String | The email of User retrieved. | 

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
| account_details.id | Number | The account ID of account. | 
| account_details.name | String | The Account Name of account being queried. | 
| account_details.contactName | String | Contact name for given account. | 
| account_details.contactEmail | String | Email of the contact person. | 
| account_details.userQuota | String | User Quota for the given account, max number of users for this account. | 
| account_details.nodesQuota | Number | The simulator quota for the given account. | 
| account_details.registrationDate | Number | The registration date of given account. | 
| account_details.activationDate | Number | The Activation date of given account. | 
| account_details.expirationDate | Number | Account expiration date. | 

### safebreach-get-simulator-with-name

***
This command gives simulator with given name

#### Base Command

`safebreach-get-simulator-with-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Simulator/Node Name | Name of simulator/node to search with. | Optional | 
| details | if details are to be included for search. Possible values are: true, false. Default is true. | Required | 
| deleted | if deleted are to be included for search. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| simulator_details.simulator_id | String | The Id of given simulator. | 
| simulator_details.name | String | name for given simulator. | 
| simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| simulator_details.is_critical | String | Whether the simulator is critical. | 
| simulator_details.is_exfiltration | Number | If Simulator is exfiltration target. | 
| simulator_details.is_infiltration | Number | If simulator is infiltration target. | 
| simulator_details.is_mail_target | Number | If simulator is mail target. | 
| simulator_details.is_mail_attacker | Number | If simulator is mail attacker. | 
| simulator_details.is_pre_executor | Number | Whether the node is pre executor. | 
| simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| simulator_details.external_ip | String | external ip of given simulator. | 
| simulator_details.internal_ip | String | internal ip of given simulator. | 
| simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| simulator_details.preferred_interface | Number | Preferred simulator interface. | 
| simulator_details.preferred_ip | Number | Preferred Ip of simulator. | 
| simulator_details.hostname | String | Hostname of given simulator. | 
| simulator_details.connection_type | String | connection_type of given simulator. | 
| simulator_details.simulator_status | String | status of the simulator. | 
| simulator_details.connection_status | Number | connection status of node/simulator. | 
| simulator_details.simulator_framework_version | Number | Framework version of simulator. | 
| simulator_details.operating_system_type | String | operating system type of given simulator. | 
| simulator_details.operating_system | String | Operating system of given simulator. | 
| simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| simulator_details.deployments | Number | deployments simulator is part of. | 
| simulator_details.created_at | Number | Creation datetime of simulator. | 
| simulator_details.updated_at | String | Update datetime of given simulator. | 
| simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| simulator_details.assets | String | Assets of given simulator. | 
| simulator_details.simulation_users | Number | simulator users list. | 
| simulator_details.proxies | Number | Proxies of simulator. | 
| simulator_details.advanced_actions | Number | Advanced simulator details. | 

### safebreach-get-user-with-matching-name-or-email

***
This command gives all users depending on inputs given.

#### Base Command

`safebreach-get-user-with-matching-name-or-email`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| name | Name of the user to lookup. | Optional | 
| email | Email of the user to lookup. | Required | 
| Should Include Details | If Details of user are to be included while             querying all users. Possible values are: true. Default is true. | Required | 
| Should Include Deleted | If deleted users are to be included while querying all users. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| filtered_users.id | Number | The ID of User retrieved. | 
| filtered_users.name | String | The name of User retrieved. | 
| filtered_users.email | String | The email of User retrieved. | 

### safebreach-rotate-verification-token

***
This command rotates generated verification token.

#### Base Command

`safebreach-rotate-verification-token`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| Safebreach Content Management.new_token | String | new Token. | 

### safebreach-update-deployment

***
This command updates a deployment with given data.

#### Base Command

`safebreach-update-deployment`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Deployment ID | Name of the deployment to update. | Optional | 
| Deployment Name | Description of the deployment to update. | Optional | 
| Updated Nodes for Deployment | Comma separated ID of all nodes the deployment should be part of. | Optional | 
| Updated Deployment Name | Name of the deployment to update to. | Optional | 
| Updated deployment description. | name of the deployment to update to. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_deployment_data.id | Number | The ID of deployment created. | 
| updated_deployment_data.accountId | String | The account of deployment created. | 
| updated_deployment_data.name | String | The name of deployment created. | 
| updated_deployment_data.createdAt | String | The creation time of deployment created. | 
| updated_deployment_data.description | String | The description of deployment created. | 
| updated_deployment_data.nodes | String | The nodes that are part of deployment. | 

### safebreach-update-simulator-with-given-name

***
This command updates simulator with given name with given details.

#### Base Command

`safebreach-update-simulator-with-given-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Simulator/Node Name | Name of simulator/node to search with. | Required | 
| details | if details are to be included for search. Possible values are: true, false. Default is true. | Optional | 
| deleted | if deleted are to be included for search. Possible values are: true, false. Default is true. | Optional | 
| isEnabled | set true to enable the node. Possible values are: false, true. | Optional | 
| isProxySupported | set true to enable the proxy support. Possible values are: false, true. | Optional | 
| isCritical | set true to make node as critical node. Possible values are: false, true. | Optional | 
| isExfiltration | set true to make the node as exfiltration node. Possible values are: false, true. | Optional | 
| isInfiltration | set true to make the node as infiltration node. Possible values are: false, true. | Optional | 
| isMailTarget | set true to make node as mail target. Possible values are: false, true. | Optional | 
| isMailAttacker | set true to make node as MailAttacker node. Possible values are: false, true. | Optional | 
| isPreExecutor | set true to enable the node as PreExecutor node. Possible values are: false, true. | Optional | 
| isAWSAttacker | set true to make node as AWS attacker target. Possible values are: false, true. | Optional | 
| isAzureAttacker | set true to make node as Azure attacker node. Possible values are: false, true. | Optional | 
| isWebApplicationAttacker | set true to enable the node as web application attacker node. Possible values are: false, true. | Optional | 
| useSystemUser | set true to enable the node get system user access. Possible values are: false, true. | Optional | 
| connectionUrl | the given value will be set as connection string. | Optional | 
| cloudProxyUrl | the given value will be set as cloud proxy url. | Optional | 
| name | the given value will be set as name of simulator. | Optional | 
| preferredInterface | the given value will be set as preferred interface string. | Optional | 
| preferredIp | the given value will be set as Preferred IP. | Optional | 
| tunnel | the given value will be set as tunnel. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_simulator_details.is_enabled | String | Whether the node is enabled or not. | 
| updated_simulator_details.simulator_id | String | The Id of given simulator. | 
| updated_simulator_details.name | String | name for given simulator. | 
| updated_simulator_details.account_id | String | Account Id of account Hosting given simulator. | 
| updated_simulator_details.is_critical | String | Whether the simulator is critical. | 
| updated_simulator_details.is_exfiltration | Number | If Simulator is exfiltration target. | 
| updated_simulator_details.is_infiltration | Number | If simulator is infiltration target. | 
| updated_simulator_details.is_mail_target | Number | If simulator is mail target. | 
| updated_simulator_details.is_mail_attacker | Number | If simulator is mail attacker. | 
| updated_simulator_details.is_pre_executor | Number | Whether the node is pre executor. | 
| updated_simulator_details.is_aws_attacker | String | if the given simulator is aws attacker. | 
| updated_simulator_details.is_azure_attacker | String | If the given simulator is azure attacker. | 
| updated_simulator_details.external_ip | String | external ip of given simulator. | 
| updated_simulator_details.internal_ip | String | internal ip of given simulator. | 
| updated_simulator_details.is_web_application_attacker | String | Whether the simulator is Web application attacker. | 
| updated_simulator_details.preferred_interface | Number | Preferred simulator interface. | 
| updated_simulator_details.preferred_ip | Number | Preferred Ip of simulator. | 
| updated_simulator_details.hostname | String | Hostname of given simulator. | 
| updated_simulator_details.connection_type | String | connection_type of given simulator. | 
| updated_simulator_details.simulator_status | String | status of the simulator. | 
| updated_simulator_details.connection_status | Number | connection status of node/simulator. | 
| updated_simulator_details.simulator_framework_version | Number | Framework version of simulator. | 
| updated_simulator_details.operating_system_type | String | operating system type of given simulator. | 
| updated_simulator_details.operating_system | String | Operating system of given simulator. | 
| updated_simulator_details.execution_hostname | String | Execution Hostname of the given node. | 
| updated_simulator_details.deployments | Number | deployments simulator is part of. | 
| updated_simulator_details.created_at | Number | Creation datetime of simulator. | 
| updated_simulator_details.updated_at | String | Update datetime of given simulator. | 
| updated_simulator_details.deleted_at | String | deletion datetime of given simulator. | 
| updated_simulator_details.assets | String | Assets of given simulator. | 
| updated_simulator_details.simulation_users | Number | simulator users list. | 
| updated_simulator_details.proxies | Number | Proxies of simulator. | 
| updated_simulator_details.advanced_actions | Number | Advanced simulator details. | 

### safebreach-update-user-details

***
This command updates a user with given data.

#### Base Command

`safebreach-update-user-details`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| User ID | user ID of user from safebreach to search. | Optional | 
| Email | Email of the user to Search for updating user details. | Required | 
| Name | Update the user name to given string. | Optional | 
| User Description | Update the user Description to given string. | Optional | 
| Is Active | Update the user Status. Possible values are: true, false, . | Optional | 
| Password | Password of user to be updated with. | Optional | 
| User role | Role of the user to be changed to. Possible values are: viewer, administrator, contentDeveloper, operator. Default is viewer. | Optional | 
| Deployments | Comma separated ID of all deployments the user should be part of. | Optional | 
| Should Include Details | If Details of user are to be included while            querying all users. Possible values are: true, false. Default is true. | Optional | 
| Should Include Deleted | If deleted users are to be included while querying all users. Possible values are: true, false. Default is true. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_user_data.id | Number | The ID of User created. | 
| updated_user_data.name | String | The name of User created. | 
| updated_user_data.email | String | The email of User created. | 
| updated_user_data.createdAt | String | The creation time of User created. | 
| updated_user_data.deletedAt | String | The Deletion time of User created. | 
| updated_user_data.roles | String | The roles of User created. | 
| updated_user_data.description | String | The description of User created. | 
| updated_user_data.role | String | The role of User created. | 
| updated_user_data.deployments | String | The deployments user is part of. | 
