RESOURCE_GROUP_NAME=consul_resource_group
REGION=useast

az group create --name ${RESOURCE_GROUP_NAME} --location ${REGION} #use this command when you need to create a new resource group for your deployment
az group deployment create --resource-group ${RESOURCE_GROUP_NAME} --template-uri https://raw.githubusercontent.com/Azure/azure-quickstart-templates/master/application-workloads/consul/consul-on-ubuntu/azuredeploy.json