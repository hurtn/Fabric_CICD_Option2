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
import os,argparse, requests
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items,change_log_level
from azure.identity import ClientSecretCredential

# function to return the workspace ID
def get_workspace_id(workspace_name, token_credential):
    url = "https://api.fabric.microsoft.com/v1/workspaces"
    headers = {
        "Authorization": f"Bearer {token_credential}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        workspaces = response.json().get("value", [])
        for workspace in workspaces:
            if workspace.get("displayName") == workspace_name:
                return workspace.get("id")
            else:
                return "Error: Workspace not found"
    else:
        return f"Error: {response.status_code}, {response.text}"

# set log level
change_log_level("DEBUG")

# parse arguments from yaml pipeline
parser = argparse.ArgumentParser(description='Process Azure Pipeline arguments.')
parser.add_argument('--items_in_scope',type=str, help= 'Defines the item types to be deployed')
args = parser.parse_args()
item_types_in_scope = args.items_in_scope

#get the token
cid=os.environ('azclientid')
print(f'Extracted client id from variable group {cid}')
sec=os.environ('azspsecret')
tid=os.environ('aztenantid')
token_credential = ClientSecretCredential(client_id=cid, client_secret=sec, tenant_id=tid)

# get branch name from build
branch = os.getenv("BUILD_SOURCEBRANCH").replace("refs/heads/","")

# define workspace name to be deployed to based on value in variable group based on branch name
workspace_name = os.environ.get(f'{branch}WorkspaceName')
print(f'Obtaining GUID for {workspace_name}')
lookup_response = get_workspace_id(workspace_name, token_credential)
if lookup_response.startswith("Error"):
    raise ValueError("Invalid workspace name specified or does not map to branch name + 'WorkspaceName'")
else:
    workspace_id = lookup_response
    print(f"Workspace ID for {workspace_name} set to {workspace_id}")

# set repo folder
repository_directory = os.environ('gitFolder')

item_type_in_scope = ["Notebook", "DataPipeline", "Lakehouse","SemanticModel","Report"]

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=args.workspace_id,
    environment=branch,
    repository_directory=repository_directory,
    item_type_in_scope=item_types_in_scope,
    token_credential=token_credential,
)

# Publish items to the workspace
print(f'Deploying to workspace...')

publish_all_items(target_workspace)

# Unpublish orphaned items from the workspace
unpublish_all_orphan_items(target_workspace)
