import requests


BASE_URL = "http://localhost:8080/api/2.1/unity-catalog"

function_info = {
    "catalog_name": "my_catalog",
    "schema_name": "my_schema",
    "name": "my_function",
    "function_type": "SCALAR",
    "input_params": [{"name": "x", "type": "int"}],
    "return_params": [{"name": "result", "type": "int"}],
    "routine_body": "x + 1"
}


def make_request(method, endpoint, payload=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.request(method, url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def create_catalog(name, comment=""):
    endpoint = "/catalogs"
    payload = {"name": name, "comment": comment}
    return make_request("POST", endpoint, payload)


def list_catalogs():
    endpoint = "/catalogs"
    return make_request("GET", endpoint)


def get_catalog(name):
    endpoint = f"/catalogs/{name}"
    return make_request("GET", endpoint)


def update_catalog(name, updates):
    endpoint = f"/catalogs/{name}"
    return make_request("PATCH", endpoint, updates)


def delete_catalog(name):
    endpoint = f"/catalogs/{name}"
    return make_request("DELETE", endpoint)


def create_schema(catalog_name, schema_name, comment=""):
    endpoint = "/schemas"
    payload = {
        "catalog_name": catalog_name,
        "name": schema_name,
        "comment": comment
    }
    return make_request("POST", endpoint, payload)


def list_schemas(catalog_name):
    endpoint = f"/schemas?catalog_name={catalog_name}"
    return make_request("GET", endpoint)


def get_schema(full_name):
    endpoint = f"/schemas/{full_name}"
    return make_request("GET", endpoint)


def update_schema(full_name, updates):
    endpoint = f"/schemas/{full_name}"
    return make_request("PATCH", endpoint, updates)


def delete_schema(full_name):
    endpoint = f"/schemas/{full_name}"
    return make_request("DELETE", endpoint)


def create_table(catalog_name, schema_name, table_name, table_type, columns):
    for column in columns:
        if "name" not in column or "type" not in column:
            raise ValueError("Each column must have 'name' and 'type' fields.")
        if not isinstance(column["type"], str) or not column["type"]:
            raise ValueError("Column 'type' must be a non-empty string.")

    endpoint = "/tables"
    payload = {
        "catalog_name": catalog_name,
        "schema_name": schema_name,
        "name": table_name,
        "table_type": table_type,
        "columns": columns
    }
    return make_request("POST", endpoint, payload)


def list_tables(catalog_name, schema_name):
    endpoint = f"/tables?catalog_name={catalog_name}&schema_name={schema_name}"
    return make_request("GET", endpoint)


def get_table(full_name):
    endpoint = f"/tables/{full_name}"
    return make_request("GET", endpoint)


def delete_table(full_name):
    endpoint = f"/tables/{full_name}"
    return make_request("DELETE", endpoint)


def create_volume(catalog_name, schema_name, volume_name, volume_type, storage_location):
    endpoint = "/volumes"
    payload = {
        "catalog_name": catalog_name,
        "schema_name": schema_name,
        "name": volume_name,
        "volume_type": volume_type,
        "storage_location": storage_location
    }
    return make_request("POST", endpoint, payload)


def list_volumes(catalog_name, schema_name):
    endpoint = f"/volumes?catalog_name={catalog_name}&schema_name={schema_name}"
    return make_request("GET", endpoint)


def get_volume(full_name):
    endpoint = f"/volumes/{full_name}"
    return make_request("GET", endpoint)


def update_volume(full_name, updates):
    endpoint = f"/volumes/{full_name}"
    return make_request("PATCH", endpoint, updates)

def delete_volume(full_name):
    endpoint = f"/volumes/{full_name}"
    return make_request("DELETE", endpoint)


def create_function(catalog_name, schema_name, function_name, function_type, input_params, return_params, routine_body):
    for param in input_params:
        if "name" not in param or "type" not in param:
            raise ValueError("Each input parameter must have 'name' and 'type' fields.")
        if not isinstance(param["type"], str) or not param["type"]:
            raise ValueError("Input parameter 'type' must be a non-empty string.")

    # Validate return parameters
    for param in return_params:
        if "name" not in param or "type" not in param:
            raise ValueError("Each return parameter must have 'name' and 'type' fields.")
        if not isinstance(param["type"], str) or not param["type"]:
            raise ValueError("Return parameter 'type' must be a non-empty string.")

    # Validate routine body
    if not isinstance(routine_body, str) or not routine_body:
        raise ValueError("Routine body must be a non-empty string.")

    endpoint = "/functions"
    payload = {
        "catalog_name": catalog_name,
        "schema_name": schema_name,
        "name": function_name,
        "function_type": function_type,
        "input_params": input_params,
        "return_params": return_params,
        "routine_body": routine_body
    }
    return make_request("POST", endpoint, payload)


def list_functions(catalog_name, schema_name):
    endpoint = f"/functions?catalog_name={catalog_name}&schema_name={schema_name}"
    return make_request("GET", endpoint)


def get_function(full_name):
    endpoint = f"/functions/{full_name}"
    return make_request("GET", endpoint)


def delete_function(full_name):
    endpoint = f"/functions/{full_name}"
    return make_request("DELETE", endpoint)


def main(catalog_name):
    # Create a catalog
    print("Creating catalog...")
    create_catalog(catalog_name, "This is a test catalog")

    # List catalogs
    print("\nListing catalogs...")
    catalogs = list_catalogs()
    print("Catalogs:", catalogs)

    # Create a schema
    print("\nCreating schema...")
    create_schema(catalog_name, "my_schema", "This is a test schema")

    # List schemas
    print("\nListing schemas...")
    schemas = list_schemas(catalog_name)
    print("Schemas:", schemas)

    # Create a table
    print("\nCreating table...")
    columns = [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]
    create_table(catalog_name, "my_schema", "my_table", "EXTERNAL", columns)

    # List tables
    print("\nListing tables...")
    tables = list_tables(catalog_name, "my_schema")
    print("Tables:", tables)

    # Create a volume
    print("\nCreating volume...")
    create_volume(catalog_name, "my_schema", "my_volume", "EXTERNAL", "s3://my-bucket/volume")

    # List volumes
    print("\nListing volumes...")
    volumes = list_volumes(catalog_name, "my_schema")
    print("Volumes:", volumes)

    def create_model(catalog_name, schema_name, model_name, description=""):
        endpoint = "/models"
        payload = {
            "catalog_name": catalog_name,
            "schema_name": schema_name,
            "name": model_name,
            "description": description
        }
        return make_request("POST", endpoint, payload)

    # Create a function
    print("\nCreating function...")
    input_params = [{"name": "x", "type": "int"}]
    return_params = [{"name": "result", "type": "int"}]
    routine_body = "x + 1"
    create_function(catalog_name, "my_schema", "my_function", "SCALAR", input_params, return_params, routine_body)

    # List functions
    print("\nListing functions...")
    functions = list_functions(catalog_name, "my_schema")
    print("Functions:", functions)

    print("\nCreating model...")
    model_response = create_model(catalog_name, "my_schema", "my_model", "This is a test model")
    if model_response:
        print("Model created successfully:", model_response)


if __name__ == "__main__":
    main("test_catalog")
