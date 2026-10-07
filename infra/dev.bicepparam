using './main.bicep'

param workloadName = 'expense'

param environment = 'dev'

param location = readEnvironmentVariable('LOCATION', 'eastus')

param mysqlAdminUsername = 'expenseadmin'

param mysqlAdminPassword = readEnvironmentVariable('MYSQL_ADMIN_PASSWORD')

param mysqlDatabaseName = 'expense_tracker'

param tags = {
  workload: 'expense'
  environment: 'dev'
  managedBy: 'bicep'
  project: 'expense-tracker'
}
