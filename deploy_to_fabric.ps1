# Retrieve secrets from environment variables
$AppId = $env:AZURE_APP_ID
$Secret = $env:AZURE_SECRET
$TenantId = $env:AZURE_TENANT_ID

# Debug (Print Only Non-Sensitive Variables)
Write-Host "AppId = " $AppId ", TenantId =" $TenantId

# Ensure secrets exist
if (-not $AppId -or -not $Secret -or -not $TenantId) {
    Write-Error "Missing required environment variables!"
    exit 1
}

# Authenticate with Azure CLI
Write-Host "Authenticating with Azure using Service Principal..."
az login --service-principal -u $AppId -p $Secret --tenant $TenantId

if ($?) {
    Write-Host "Azure CLI authentication successful."
} else {
    Write-Error "Azure CLI authentication failed."
    exit 1
}

# Run Python deployment script
Write-Host "Running Python Deployment Script..."
python ./scripts/deploy/deploy_to_fabric.py

if ($?) {
    Write-Host "Deployment completed successfully."
} else {
    Write-Error "Deployment failed. Check logs for details."
}