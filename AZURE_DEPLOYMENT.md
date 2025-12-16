# Azure Deployment Setup Guide

## Prerequisites
- Azure CLI installed (`az`)
- GitHub repository set up
- Azure subscription

## Step 1: Create Azure Resources

Run these commands in your terminal (or Azure Cloud Shell):

```bash
# Login to Azure

az login --tenant hasprot.onmicrosoft.com --use-device-code
# az login

# Set variables (customize these)
RESOURCE_GROUP="blog2026-rg"
LOCATION="eastus"
ACR_NAME="blog2026acr"
APP_NAME="blog2026"
APP_PLAN="blog2026-plan"

# Create Resource Group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Azure Container Registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic --admin-enabled true

# Create App Service Plan (Linux, B1 Basic tier - ~$13/month, 1 core, 1.75GB RAM)
az appservice plan create --name $APP_PLAN --resource-group $RESOURCE_GROUP --is-linux --sku B1

# Create Web App for Containers
az webapp create --resource-group $RESOURCE_GROUP --plan $APP_PLAN --name $APP_NAME --deployment-container-image-name $ACR_NAME.azurecr.io/blog2026:latest

# Configure Web App to use ACR
az webapp config container set --name $APP_NAME --resource-group $RESOURCE_GROUP --docker-custom-image-name $ACR_NAME.azurecr.io/blog2026:latest --docker-registry-server-url https://$ACR_NAME.azurecr.io
```

## Step 2: Get Credentials for GitHub Secrets

### Get ACR Credentials
```bash
# Get ACR username and password
az acr credential show --name $ACR_NAME
```
Save these as GitHub secrets:
- `ACR_USERNAME` - the username from the output
- `ACR_PASSWORD` - the password from the output

### Create Azure Service Principal
```bash
# Create service principal and get credentials
az ad sp create-for-rbac --name "blog2026-github" --role contributor --scopes /subscriptions/<SUBSCRIPTION_ID>/resourceGroups/$RESOURCE_GROUP --sdk-auth
```
Save the entire JSON output as GitHub secret:
- `AZURE_CREDENTIALS` - the full JSON object

## Step 3: Add GitHub Secrets

1. Go to your GitHub repository
2. Navigate to Settings → Secrets and variables → Actions
3. Add these secrets:
   - `ACR_USERNAME` - Azure Container Registry username
   - `ACR_PASSWORD` - Azure Container Registry password
   - `AZURE_CREDENTIALS` - Full JSON from service principal creation

## Step 4: Update Workflow Configuration

Edit `.github/workflows/deploy.yml` and update these values:
- `AZURE_WEBAPP_NAME` - Your Azure Web App name
- `ACR_NAME` - Your Azure Container Registry name

## Step 5: Deploy

Push to the `main` branch to trigger the deployment:
```bash
git add .
git commit -m "Add Azure deployment pipeline"
git push origin main
```

## Your Website URL

After deployment, your site will be available at:
```
https://<APP_NAME>.azurewebsites.net
```

## Local Testing with Docker

Test the Docker image locally before deploying:
```bash
# Build the image
docker build -t blog2026 .

# Run the container
docker run -p 8000:8000 blog2026

# Visit http://localhost:8000
```

## Estimated Monthly Cost

- App Service B1: ~$13/month
- Container Registry Basic: ~$5/month
- **Total: ~$18/month**

For lower costs, consider using the Free (F1) tier for App Service (limited to 60 CPU minutes/day).
