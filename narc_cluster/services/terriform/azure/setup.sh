az login
export ARM_SUBSCRIPTION_ID
export ARM_TENANT_ID

az ad sp create-for-rbac --role="Contributor" --scopes="/subscriptions/${ARM_SUBSCRIPTION_ID}"

export ARM_CLIENT_ID
export ARM_CLIENT_SECRET

$ az group create --name packer --location "East US"

export AZURE_RESOURCE_GROUP=packer