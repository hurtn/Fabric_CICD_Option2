# Retrieve parameters
param(
[string]$workspaceName,
[string]$ptenantid,
[string]$pclientid,
[string]$pclientsecret
)

# Debug (Print Only Non-Sensitive Variables)
Write-Host "Workspacename = " $workspaceName ", ClientId =" $pclientid

# Ensure secrets exist
if (-not $workspaceName -or -not $ptenantid -or -not $pclientid) {
    Write-Error "Missing required parameters!"
    exit 1
}

# Authenticate with Azure CLI
Write-Host "Authenticating with Azure using Service Principal..."
az login --service-principal -u $pclientid -p $pclientsecret --tenant $ptenantid

if ($?) {
    Write-Host "Azure CLI authentication successful."
} else {
    Write-Error "Azure CLI authentication failed."
    exit 1
}

# Retrieve access token
$accessToken = az account get-access-token --query accessToken --output tsv

if (-not $accessToken) {
    Write-Error "Failed to retrieve access token."
    exit 1
}

# Function to look up workspace ID
function Get-WorkspaceId {
    param(
        [string]$workspaceName,
        [string]$accessToken
    )

    $fabricApiUrl = "https://api.fabric.microsoft.com/v1/workspaces"
    $headers = @{
        "Authorization" = "Bearer $accessToken"
        "Content-Type" = "application/json"
    }

    $response = Invoke-RestMethod -Uri $fabricApiUrl -Headers $headers -Method Get

    if ($response.StatusCode -eq 200) {
        $workspaces = $response.value
        foreach ($workspace in $workspaces) {
            if ($workspace.displayName -eq $workspaceName) {
                return $workspace.id
            }
        }
        Write-Host "Workspace '$workspaceName' not found."
        return $null
    } else {
        Write-Error "Failed to retrieve workspaces. Status code: $($response.StatusCode)"
        return $null
    }
}

# Look up workspace ID
$workspaceId = Get-WorkspaceId -workspaceName $workspaceName -accessToken $accessToken

if ($workspaceId) {
    Write-Host "Workspace ID for '$workspaceName': $workspaceId"
} else {
    Write-Error "Failed to retrieve workspace ID."
    exit 1
}

# Run Python deployment script
Write-Host "Running Python Deployment Script..."
python "./scripts/deploy/deploy_to_fabric.py" --workspace_name $workspaceId --tenant_id $ptenantid --client_id $pclientid --client_secret $pclientsecret

if ($?) {
    Write-Host "Deployment completed successfully."
} else {
    Write-Error "Deployment failed. Check logs for details."
}