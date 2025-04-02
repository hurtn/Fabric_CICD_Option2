import os
from fabric_cicd import FabricioWorkspace, publish_all_items, unpublish_all_orphan_items

# Get the environment variable
branch = os.getenv("BUILD_SOURCEBRANCH")

# Define branch-to-environment mapping
if branch == "dev":
    workspace_id = "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
elif branch == "qa":
    workspace_id = "0987fedc-ba65-4321-8765-cba987654321"
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
            if file ends with ".ipynb":
                directory_to_in_scope["Notebook"].append(os.path.join(root, file))

# Publish items to the workspace
workspace = FabricioWorkspace(workspace_id)
publish_all_items(workspace, directory_to_in_scope)

# Unpublish orphaned items from the workspace
unpublish_all_orphan_items(workspace)
