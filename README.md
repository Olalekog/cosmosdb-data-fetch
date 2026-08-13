# cosmosdb-data-fetch

Azure DevOps pipeline that fetches data from Azure Cosmos DB, run on a self-hosted Azure VM agent.

## How it works

- `azure-pipelines.yml` runs on the `cosmos-vm-pool` agent pool (the Azure VM registered as a self-hosted DevOps agent).
- The pipeline pulls the Cosmos DB connection string from Azure Key Vault via the `AzureKeyVault@2` task and passes it to `fetch_cosmos_data.py` as an environment variable.
- `fetch_cosmos_data.py` queries the configured database/container and prints the results to the pipeline log.

## One-time setup

1. **Register the VM as a self-hosted agent**
   - In Azure DevOps: Project Settings > Agent pools > New pool, name it `cosmos-vm-pool` (or update the `pool` value in `azure-pipelines.yml`).
   - On the VM, download and configure the agent per [Microsoft's self-hosted agent docs](https://learn.microsoft.com/azure/devops/pipelines/agents/agents), targeting that pool. Ensure Python 3.11+ is installed on the VM.

2. **Store the Cosmos DB connection string in Key Vault**
   - `az keyvault secret set --vault-name Cosmos-DB-KV --name COSMODB-CONNECTION-STRING --value "<connection-string>"`

3. **Create an Azure service connection** in Azure DevOps (Project Settings > Service connections) with permission to read the Key Vault.

4. **Create a Pipeline Library variable group** named `cosmosdb-fetch-vars` (Pipelines > Library). If you use a different name, update the `group:` value in `azure-pipelines.yml` to match.

### Key Vault secrets

| Secret name | Description |
| --- | --- |
| `COSMODB-CONNECTION-STRING` | Cosmos DB account connection string used by `fetch_cosmos_data.py` |

### Library variable group (`cosmosdb-fetch-vars`)

| Variable | Secret? | Description |
| --- | --- | --- |
| `azureServiceConnection` | No | Name of the Azure service connection (step 3) used to authorize Key Vault access |
| `keyVaultName` | No | `Cosmos-DB-KV` — name of the Key Vault holding `COSMODB-CONNECTION-STRING` |
| `COSMOS_DATABASE_NAME` | No | Cosmos DB database name to query |
| `COSMOS_CONTAINER_NAME` | No | Cosmos DB container name to query |
| `COSMOS_QUERY` | No | Query to run (defaults to `SELECT * FROM c` if omitted) |

## Local testing

```bash
pip install -r requirements.txt
export COSMOS_CONNECTION_STRING="..."
export COSMOS_DATABASE_NAME="..."
export COSMOS_CONTAINER_NAME="..."
python fetch_cosmos_data.py
```
