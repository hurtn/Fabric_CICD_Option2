# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

"""
Example demonstrating:  
1. Access variable group values from Python. Note for sensitive variables ensure the variable group is linked to key vault. See https://learn.microsoft.com/en-us/azure/devops/pipelines/library/link-variable-groups-to-key-vaults?view=azure-devops
2. Use of Service Principal Name (SPN) with a Secret credential flow, leveraging the ClientSecretCredential class. 
3. Use the Fabric reset APIs to lookup the workspace ID based on workspace name
4. Using debug log level
"""
# START-EXAMPLE

# argparse is required to gracefully deal with the arguments
import os,argparse, requests, ast
from concurrent.futures import ThreadPoolExecutor, as_completed
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items,change_log_level
from azure.identity import ClientSecretCredential

# function to return the workspace ID
def get_workspace_id(p_ws_name, p_token):
    url = "https://api.fabric.microsoft.com/v1/workspaces"
    headers = {
        "Authorization": f"Bearer {p_token.token}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    ws_id =''
    if response.status_code == 200:
        workspaces = response.json()["value"]
        for workspace in workspaces:
            if workspace["displayName"] == p_ws_name:
                ws_id = workspace["id"] 
                return workspace["id"]
        if ws_id == '':
            return f"Error: Workspace {p_ws_name} could not found."
    else:
        return f"Error: {response.status_code}, {response.text}"

# set log level
change_log_level("DEBUG")

# parse arguments from yaml pipeline. These are typically secrets from a variable group linked to an Azure Key Vault
parser = argparse.ArgumentParser(description='Process Azure Pipeline arguments.')
parser.add_argument('--aztenantid',type=str, help= 'tenant ID')
parser.add_argument('--azclientid',type=str, help= 'SP client ID')
parser.add_argument('--azspsecret',type=str, help= 'SP secret')
parser.add_argument('--target_env',type=str, help= 'target environment')

parser.add_argument('--items_in_scope',type=str, help= 'Defines the item types to be deployed')
args = parser.parse_args()
item_types_in_scope = args.items_in_scope

#get the token#
print('Obtaining token...')
token_credential = ClientSecretCredential(client_id=args.azclientid, client_secret=args.azspsecret, tenant_id=args.aztenantid)

# get target environment name
tgtenv = args.target_env
print(f'Target environment set to {tgtenv}')

# determine the target workspace using the variable group which stores the target workspace name in a variable with the naming convention "[tgtenv]WorkspaceName"
ws_name = f'{tgtenv}WorkspaceName'
print(f'Variable group to determine workspace is set to {ws_name}')

# define workspace name to be deployed to based on value in variable group based on target environment name. This variable group is not linked to a Key Vault hence the values can be access through os.environ 
workspace_name = os.environ[ws_name.upper()]
print(f'Obtaining GUID for {workspace_name}')

# generating the token used to call the Fabric REST API
resource = 'https://api.fabric.microsoft.com/'
scope = f'{resource}.default'
print(f'scope set to {scope}')
token = token_credential.get_token(scope)

def lookup_and_initialize_workspace(workspace_name, token, tgtenv, token_credential, item_types, repository_directory):
    response = get_workspace_id(workspace_name, token)
    if response.startswith("Error"):
        errmsg = f"{response}. Perhaps workspace name is set incorrectly in the variable group or does not map to environment name + 'WorkspaceName'"
        raise ValueError(errmsg)
    
    wks_id = response
    print(f"Workspace ID for {workspace_name} set to {wks_id}")

    # Initialize the FabricWorkspace
    target_workspace = FabricWorkspace(
        workspace_id=wks_id,
        environment=tgtenv,
        repository_directory=repository_directory,
        item_type_in_scope=item_types,
        token_credential=token_credential,
    )

    # Publish items to the workspace
    print(f'Publish branch to workspace...')
    publish_all_items(target_workspace)

    # Unpublish orphaned items from the workspace
    unpublish_all_orphan_items(target_workspace)

    return workspace

# Setup shared variables
repository_directory = os.environ["GITDIRECTORY"]
item_types = args.items_in_scope.strip("[]").split(",")

workspace_env_pairs = [
    {"name": "cicd_scale_dev_option1", "env": "dev"},
    {"name": "cicd_scale_dev_option2", "env": "test"},
    {"name": "cicd_scale_dev_option3", "env": "prod"},
    {"name": "cicd_scale_dev_option4", "env": "dev"},
    {"name": "cicd_scale_dev_option5", "env": "test"},
    {"name": "cicd_scale_dev_option6", "env": "prod"},
    {"name": "cicd_scale_dev_option7", "env": "dev"},
    {"name": "cicd_scale_dev_option8", "env": "test"},
    {"name": "cicd_scale_dev_option9", "env": "prod"},
    {"name": "cicd_scale_dev_option10", "env": "dev"},
    {"name": "cicd_scale_dev_option11", "env": "test"},
    {"name": "cicd_scale_dev_option12", "env": "prod"},
    {"name": "cicd_scale_dev_option13", "env": "dev"},
    {"name": "cicd_scale_dev_option14", "env": "test"},
    {"name": "cicd_scale_dev_option15", "env": "prod"},
    {"name": "cicd_scale_dev_option16", "env": "dev"},
    {"name": "cicd_scale_dev_option17", "env": "test"},
    {"name": "cicd_scale_dev_option18", "env": "prod"},
    {"name": "cicd_scale_dev_option19", "env": "dev"},
    {"name": "cicd_scale_dev_option20", "env": "test"},
    {"name": "cicd_scale_dev_option21", "env": "prod"},
    {"name": "cicd_scale_dev_option22", "env": "dev"},
    {"name": "cicd_scale_dev_option23", "env": "test"},
    {"name": "cicd_scale_dev_option24", "env": "prod"},
    {"name": "cicd_scale_dev_option25", "env": "dev"},
    {"name": "cicd_scale_dev_option26", "env": "test"},
    {"name": "cicd_scale_dev_option27", "env": "prod"},
    {"name": "cicd_scale_dev_option28", "env": "dev"},
    {"name": "cicd_scale_dev_option29", "env": "test"},
    {"name": "cicd_scale_dev_option30", "env": "prod"},
    {"name": "cicd_scale_dev_option31", "env": "dev"},
    {"name": "cicd_scale_dev_option32", "env": "test"},
    {"name": "cicd_scale_dev_option33", "env": "prod"},
    {"name": "cicd_scale_dev_option34", "env": "dev"},
    {"name": "cicd_scale_dev_option35", "env": "test"},
    {"name": "cicd_scale_dev_option36", "env": "prod"},
    {"name": "cicd_scale_dev_option37", "env": "dev"},
    {"name": "cicd_scale_dev_option38", "env": "test"},
    {"name": "cicd_scale_dev_option39", "env": "prod"},
    {"name": "cicd_scale_dev_option40", "env": "dev"},
    {"name": "cicd_scale_dev_option41", "env": "test"},
    {"name": "cicd_scale_dev_option42", "env": "prod"},
    {"name": "cicd_scale_dev_option43", "env": "dev"},
    {"name": "cicd_scale_dev_option44", "env": "test"},
    {"name": "cicd_scale_dev_option45", "env": "prod"},
    {"name": "cicd_scale_dev_option46", "env": "dev"},
    {"name": "cicd_scale_dev_option47", "env": "test"},
    {"name": "cicd_scale_dev_option48", "env": "prod"},
    {"name": "cicd_scale_dev_option49", "env": "dev"},
    {"name": "cicd_scale_dev_option50", "env": "test"}
]



# Use ThreadPoolExecutor to run lookups and initializations concurrently
with ThreadPoolExecutor() as executor:
    futures = []
    for pair in workspace_env_pairs:
        future = executor.submit(
            lookup_and_initialize_workspace,
            pair["name"],
            token,
            pair["env"],
            token_credential,
            item_types,
            repository_directory
        )
        futures.append(future)

    # Collect results
    for future in as_completed(futures):
        try:
            workspace = future.result()
            print(f"Successfully initialized workspace: {workspace.workspace_id}")
        except Exception as e:
            print(f"Failed to initialize workspace: {e}")

