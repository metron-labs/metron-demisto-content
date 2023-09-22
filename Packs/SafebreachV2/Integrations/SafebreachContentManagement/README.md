
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
