targetScope = 'subscription'

@description('Name of the application/workload.')
@minLength(3)
@maxLength(12)
param workloadName string = 'expense'

@description('Deployment environment.')
@allowed([
  'dev'
  'tst'
  'prd'
])
param environment string = 'dev'

@description('Azure region where resources will be deployed.')
param location string = 'eastus'

@description('Name of the Resource Group.')
param resourceGroupName string = 'rg-${workloadName}-${environment}'

@description('MySQL administrator username.')
param mysqlAdminUsername string = 'expenseadmin'

@description('MySQL administrator password.')
@secure()
param mysqlAdminPassword string

@description('Name of the MySQL database.')
param mysqlDatabaseName string = 'expense_tracker'

@description('Tags applied to Azure resources.')
param tags object = {
  workload: workloadName
  environment: environment
  managedBy: 'bicep'
  project: 'expense-tracker'
}

var namePrefix = '${workloadName}-${environment}'

// Create Resource Group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2025-04-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

// Deploy application resources inside the Resource Group
module resources './resources.bicep' = {
  name: '${namePrefix}-resources'
  scope: resourceGroup
  params: {
    location: location
    namePrefix: namePrefix
    mysqlAdminUsername: mysqlAdminUsername
    mysqlAdminPassword: mysqlAdminPassword
    mysqlDatabaseName: mysqlDatabaseName
    tags: tags
  }
}

output resourceGroupName string = resourceGroup.name
output appServicePlanName string = resources.outputs.appServicePlanName
output webAppName string = resources.outputs.webAppName
output webAppUrl string = resources.outputs.webAppUrl
output mysqlServerName string = resources.outputs.mysqlServerName
output mysqlDatabaseName string = resources.outputs.mysqlDatabaseName
