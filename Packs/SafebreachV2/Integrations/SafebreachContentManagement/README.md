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
