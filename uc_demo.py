import requests


BASE_URL = "http://localhost:8080/api/2.1/unity-catalog"


def make_request(method, endpoint, payload=None):
    url = f"{BASE_URL}{endpoint}"
    headers = {"Content-Type": "application/json"}
    response = requests.request(method, url, json=payload, headers=headers)
    if response.status_code in [200, 201]:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


def create_table(catalog_name, schema_name, table_name, table_type, columns):
    endpoint = "/tables"
    payload = {
        "catalog_name": catalog_name,
        "schema_name": schema_name,
        "name": table_name,
        "table_type": table_type,
        "columns": columns
    }
    return make_request("POST", endpoint, payload)


def create_model(catalog_name, schema_name, model_name, description=""):
    endpoint = "/models"
    payload = {
        "catalog_name": catalog_name,
        "schema_name": schema_name,
        "name": model_name,
        "description": description
    }
    return make_request("POST", endpoint, payload)


def create_function(catalog_name, schema_name, function_name, function_type, input_params, return_params, routine_body):
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


def main():
    print("Creating table...")
    columns = [{"name": "id", "type": "int"}, {"name": "name", "type": "string"}]
    table_response = create_table("my_catalog", "my_schema", "my_table", "EXTERNAL", columns)
    if table_response:
        print("Table created successfully:", table_response)

    print("\nCreating model...")
    model_response = create_model("my_catalog", "my_schema", "my_model", "This is a test model")
    if model_response:
        print("Model created successfully:", model_response)

    print("\nCreating function...")
    input_params = [{"name": "x", "type": "int"}]
    return_params = [{"name": "result", "type": "int"}]
    routine_body = "x + 1"
    function_response = create_function("my_catalog", "my_schema", "my_function", "SCALAR", input_params, return_params, routine_body)
    if function_response:
        print("Function created successfully:", function_response)


if __name__ == "__main__":
    main()
