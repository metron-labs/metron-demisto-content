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
