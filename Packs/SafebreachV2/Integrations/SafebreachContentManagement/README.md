
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
