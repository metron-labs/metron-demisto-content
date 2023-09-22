
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

### safebreach-delete-schedule

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-delete-schedule`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| schedule ID | schedule ID of schedule to delete. | Required | 

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

### safebreach-get-custom-scenarios

***
This command gets simulations which are in running or queued state.

#### Base Command

`safebreach-get-custom-scenarios`

#### Input

| **Argument Name** | **Description** | **Required** |
| --- | --- | --- |
| schedule details | Whether to get details of custom scenarios,            set this to true every time unless you explicitly don't need details. Possible values are: false, true. Default is true. | Optional | 

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
