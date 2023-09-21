
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
| Name | Name of the deployment to create. | Required | 
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
| Deployment ID | ID of the deployment to delete. | Optional | 
| Deployment Name | Name of the deployment to delete. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_deployment_data.id | Number | The ID of deployment to be deleted. | 
| deleted_deployment_data.accountId | String | The account of deployment to be deleted. | 
| deleted_deployment_data.name | String | The name of deployment to be deleted. | 
| deleted_deployment_data.createdAt | String | The creation time of deployment to be deleted. | 
| deleted_deployment_data.description | String | The description of deployment to be deleted. | 
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

### safebreach-delete-schedule

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-delete-schedule`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| schedule ID | schedule ID. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| deleted_Schedule.id | String | the Id of the schedule. | 
| deleted_Schedule.isEnabled | Boolean | if simulation is enabled. | 
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
| active_simulations.status | String | the status of the simulation. | 
| active_simulations.timestamp | String | the time of the simulation. | 
| active_simulations.numOfTasks | String | the number of steps involved in the simulation. | 
| active_simulations.planRunId | String | the planRunId of the simulation. | 
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
| active_tests.originalScenarioId | String | Original scenario ID of the running test | 
| active_tests.actions count | String | number of actions | 
| active_tests.edges count | String | number of edges. | 
| active_tests.createdAt | String | details related to when test is created. | 
| active_tests.updatedAt | String | details related to when test is last updated/changed | 
| active_tests.steps count | String | number of steps in simulator. | 
| active_tests.planId | String | planId of the test. | 
| active_tests.originalPlan ID | String | original plan ID for reference. | 
| active_tests.ranBy | String | User who ran the plan. | 
| active_tests.ranFrom | String | Where the test ran from. | 
| active_tests.enableFeedbackLoop | String | Should feedback loop be enabled. | 
| active_tests.planRunId | String | plan run id. | 
| active_tests.priority | String | priority of tests. | 
| active_tests.retrySimulations | String | Should simulations be retried | 
| active_tests.flowControl | String | Flow control of tests | 
| active_tests.slot position | String | position in queue. | 
| active_tests.slot status | Boolean | is the test paused. | 
| active_tests.pauseDuration | String | is the test paused and if so till when | 
| active_tests.totalJobs | String | Total number of jobs for this test | 
| active_tests.pausedDate | String | when the test is paused | 
| active_tests.expectedSimulationsAmount | String | number of simulations expected | 
| active_tests.dispatchedSimulationsAmount | String | the number of simulations dispatched | 
| active_tests.blockedSimulationsAmount | String | The number of simulations blocked | 
| active_tests.unblockedSimulationsAmount | String | The number of simulations unblocked | 
| active_tests.skippedSimulationsAmount | String | The number of simulations skipped | 
| active_tests.failedSimulationsAmount | String | The number of simulations failed | 
| active_tests.isPrepared | String | Total number of simulations that have been prepared | 

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
| hostname | if hostname to be included for search. | Optional | 
| connectionType | if connectionType to be included for search. | Optional | 
| externalIp | if external IP details to be included for search. | Optional | 
| internalIp | if Internal IP are to be included for search. | Optional | 
| os | if Operating system details to be included for search. Possible values are: true, false. | Optional | 
| sortDirection | direction in which secrets are to be sorted. Possible values are: asc, desc. Default is asc. | Optional | 
| pageSize | number of entries to search. | Optional | 
| isEnabled | if to search only enabled ones. Possible values are: true, false. | Optional | 
| isConnected | status of connection of nodes to search. Possible values are: true, false. | Optional | 
| isCritical | whether to search only for critical nodes or not. Possible values are: true, false. | Optional | 
| additionalDetails | Whether to show additional details or not. Possible values are: true, false. | Optional | 
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

### safebreach-get-custom-scenarios

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-get-custom-scenarios`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| schedule details | Whether to get details of custom scenarios,                set this to true every time unless you explicitly dont need details. Possible values are: false, true. Default is true. | Optional | 

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
This command gets simulations which are in running or queued state.

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
| prebuilt_scenarios.tags_list | String | the tags of the scenario. | 
| prebuilt_scenarios.categories | String | the category ids of the scenario. | 
| prebuilt_scenarios.steps_order | String | the order of steps involved in the scenario. | 
| prebuilt_scenarios.order | String | the order of the scenario. | 
| prebuilt_scenarios.minApiVer | String | the minimum version of API required for scenario to be executed | 

### safebreach-get-schedules

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-get-schedules`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| deleted | should deleted be retrieved. Possible values are: true, false. Default is true. | Optional | 
| details | Should details tests be included in result. Possible values are: true, false. Default is true. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| schedules.id | String | the Id of the schedule. | 
| schedules.isEnabled | Boolean | if simulation is enabled. | 
| schedules.name | String | the name of the schedule. | 
| schedules.cronString | String | the cron expression the schedule. | 
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
This command gets simulations which are in running or queued state.

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
| account_details.id | Number | The account ID of account. | 
| account_details.name | String | The Account Name of account being queried. | 
| account_details.contactName | String | Contact name for given account. | 
| account_details.contactEmail | String | Email of the contact person. | 
| account_details.userQuota | String | User Quota for the given account, max number of users for this account. | 
| account_details.nodesQuota | Number | The simulator quota for the given account. | 
| account_details.registrationDate | Number | The registration date of given account. | 
| account_details.activationDate | String | The Activation date of given account. | 
| account_details.expirationDate | String | Account expiration date. | 

### safebreach-get-simulator-with-name

***
This command gives simulator with given name

#### Base Command

`safebreach-get-simulator-with-name`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Simulator/Node Name | Name of simulator/node to search with. | Required | 
| details | if details are to be included for search. Possible values are: true, false. Default is true. | Required | 
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

### safebreach-get-verification-token

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-get-verification-token`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| verification_token.token | String | the value of new verification token. | 

### safebreach-play-pause-simulations-tests

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-play-pause-simulations-tests`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| Simulation/Test State | State of tests/simulators to set to. Possible values are: resume, pause. | Required | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| simulations_tests_status.status | String | the status of the simulations/tests. | 

### safebreach-rerun-scenario

***
this commands puts given simulation data at a given position, for this command to get test data input,        run safebreach-custom-scenarios-list and copy field 'data for rerun simulation' from table 

#### Base Command

`safebreach-rerun-scenario`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| position | position in queue to put the given simulation data at. | Optional | 
| enable feedback loop | this argument is used to enable/disable feedback loop. Possible values are: false, true. Default is true. | Optional | 
| retry simulation | this argument is used to retry according to retry policy                 mention in retry policy field. Possible values are: , false, true. | Optional | 
| wait for retry | this arguments tells flow to retry the adding to queue after the                 current step execution is completed. Possible values are: , false, true. | Optional | 
| priority | the priority of this simulation action. Possible values are: low, high. Default is low. | Optional | 
| simulation data | simulation data for the given simulation. | Required | 

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

### safebreach-rerun-test

***
this commands puts given test data at a given position, for this command to get test data input,        run safebreach-custom-scenarios-list and copy field 'data for rerun test' from table 

#### Base Command

`safebreach-rerun-test`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| position | position in queue to put the given test data at. | Optional | 
| enable feedback loop | this argument is used to enable/disable feedback loop. Possible values are: false, true. Default is true. | Optional | 
| retry simulation | this argument is used to retry according to retry policy                 mention in retry policy field. Possible values are: , false, true. | Optional | 
| wait for retry | this arguments tells flow to retry the adding to queue after the                 current step execution is completed. Possible values are: , false, true. | Optional | 
| priority | the priority of this test action. Possible values are: low, high. Default is low. | Optional | 
| test data | test data for the given test. | Required | 

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
| Deployment ID | ID of the deployment to update. | Optional | 
| Deployment Name | Name of the deployment to update. | Required | 
| Updated Nodes for Deployment | Comma separated ID of all nodes the deployment should be part of. | Optional | 
| Updated Deployment Name | Name of the deployment to update to. | Optional | 
| Updated deployment description. | name of the deployment to update to. | Optional | 

#### Context Output

| **Path** | **Type** | **Description** |
| --- | --- | --- |
| updated_deployment_data.id | Number | The ID of deployment to update. | 
| updated_deployment_data.accountId | String | The account of deployment to update. | 
| updated_deployment_data.name | String | The name of deployment to update. | 
| updated_deployment_data.createdAt | String | The creation time of deployment to update. | 
| updated_deployment_data.description | String | The description of deployment to update. | 
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
| updated_user_data.id | Number | The ID of User updated. | 
| updated_user_data.name | String | The name of User updated. | 
| updated_user_data.email | String | The email of User updated. | 
| updated_user_data.createdAt | String | The creation time of User updated. | 
| updated_user_data.deletedAt | String | The Deletion time of User updated. | 
| updated_user_data.roles | String | The roles of User updated. | 
| updated_user_data.description | String | The description of User updated. | 
| updated_user_data.role | String | The role of User updated. | 
| updated_user_data.deployments | String | The deployments user is part of. | 
