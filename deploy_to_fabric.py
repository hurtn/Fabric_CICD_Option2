import os
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items

# Get the environment variable
branch = os.getenv("BUILD_SOURCEBRANCH")
print('Branch: {branch}')
# Define branch-to-environment mapping
if branch == "dev":
    workspace_id = "e489926a-747f-444d-88f7-353222a68892"
elif branch == "test":
    workspace_id = "15f88951-a30a-4b7a-9e54-067654c41e03"
elif branch == "prod":
    workspace_id = "5678abcd-1234-efgh-5678-abcd12345678"
else:
    raise ValueError("Invalid branch for deployment: {branch}")

# Define the directory containing items to deploy and their types
repository_directory = "/path/to/repository"
directory_to_in_scope = {"Notebook": []}

print("Repository directory structure:")
for root, dirs, files in os.walk(repository_directory):
    print(f"Directory: {root}")
    for file in files:
        print(f"File: {file}")

print("\nCurrent working directory:")
print(os.getcwd())

# Walk through the repository with the specified configuration
for root, dirs, files in os.walk(repository_directory):
    if root.startswith(repository_directory):
        for file in files:
            if file.endswith(".ipynb"):
                directory_to_in_scope["Notebook"].append(os.path.join(root, file))



# Sample values for FabricWorkspace parameters
environment = branch
repository_directory = "/CICDWS"
item_type_in_scope = ["Notebook", "DataPipeline", "Lakehouse"]

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=environment,
    repository_directory=repository_directory,
    item_type_in_scope=item_type_in_scope,
)


# Publish items to the workspace
workspace = FabricioWorkspace(workspace_id)
publish_all_items(workspace, directory_to_in_scope)

# Unpublish orphaned items from the workspace
unpublish_all_orphan_items(workspace)
