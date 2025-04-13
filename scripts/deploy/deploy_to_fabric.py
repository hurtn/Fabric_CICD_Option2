import os,argparse
from fabric_cicd import FabricWorkspace, publish_all_items, unpublish_all_orphan_items,change_log_level

parser = argparse.ArgumentParser(description='Process Azure Pipeline arguments.')
parser.add_argument('--workspace_id', type=str)

args = parser.parse_args()

change_log_level("DEBUG")
# Get the environment variable
branch = os.getenv("BUILD_SOURCEBRANCH").replace("refs/heads/","")
print(f'Deploying to workspace {branch}')

# Sample values for FabricWorkspace parameters
environment = branch
repository_directory = "CICDWS"
item_type_in_scope = ["Notebook", "DataPipeline", "Lakehouse","SemanticModel","Report"]

# Initialize the FabricWorkspace object with the required parameters
target_workspace = FabricWorkspace(
    workspace_id=args.workspace_id,
    environment=environment,
    repository_directory=repository_directory,
    item_type_in_scope=item_type_in_scope,
)

# Publish items to the workspace
#workspace = FabricioWorkspace(workspace_id)
publish_all_items(target_workspace)

# Unpublish orphaned items from the workspace
unpublish_all_orphan_items(target_workspace)
