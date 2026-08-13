import os
import sys

from azure.cosmos import CosmosClient

DATABASE_NAME = os.environ.get("COSMOS_DATABASE_NAME", "")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER_NAME", "")
QUERY = os.environ.get("COSMOS_QUERY", "SELECT * FROM c")


def main():
    connection_string = os.environ.get("COSMOS_CONNECTION_STRING")
    if not connection_string:
        print("COSMOS_CONNECTION_STRING is not set", file=sys.stderr)
        sys.exit(1)
    if not DATABASE_NAME or not CONTAINER_NAME:
        print("COSMOS_DATABASE_NAME and COSMOS_CONTAINER_NAME must be set", file=sys.stderr)
        sys.exit(1)

    client = CosmosClient.from_connection_string(connection_string)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    items = list(container.query_items(query=QUERY, enable_cross_partition_query=True))
    print(f"Fetched {len(items)} item(s) from {DATABASE_NAME}/{CONTAINER_NAME}")
    for item in items:
        print(item)


if __name__ == "__main__":
    main()
