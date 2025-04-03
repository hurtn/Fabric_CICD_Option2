import os
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items
change_log_level("DEBUG")
# Get the environment variable
branch = os.getenv("BUILD_SOURCEBRANCH").replace("refs/heads/","")
print(f'Branch: {branch}')

# Define branch-to-environment mapping
if branch == "dev":
    workspace_id = "e489926a-747f-444d-88f7-353222a68892"
elif branch == "test":
    workspace_id = "15f88951-a30a-4b7a-9e54-067654c41e03"
elif branch == "prod":
    workspace_id = "0c3ab123-5aae-4a03-bafe-0fe00f46e213"
else:
    raise ValueError("Invalid branch for deployment: {branch}")

# Sample values for FabricWorkspace parameters
environment = branch
repository_directory = "CICDWS"
item_type_in_scope = ["Notebook", "DataPipeline", "Lakehouse"]

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=environment,
    repository_directory=repository_directory,
    item_type_in_scope=item_type_in_scope,
)

# Publish items to the workspace
#workspace = FabricioWorkspace(workspace_id)
publish_all_items(target_workspace)

# Unpublish orphaned items from the workspace
unpublish_all_orphan_items(target_workspace)
