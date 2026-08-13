import json
import os
import sys

from azure.cosmos import CosmosClient

DATABASE_NAME = os.environ.get("COSMOS_DATABASE_NAME", "")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER_NAME", "")
QUERY = os.environ.get("COSMOS_QUERY", "SELECT * FROM c")
OUTPUT_PATH = os.environ.get("COSMOS_OUTPUT_PATH", "cosmos_data.json")


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

    output_dir = os.path.dirname(OUTPUT_PATH)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, default=str)
    print(f"Wrote {len(items)} item(s) to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
