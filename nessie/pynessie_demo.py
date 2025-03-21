from pynessie import NessieClient
from pynessie.model import Branch, Tag
from pynessie.conf import build_config

# Initialize the Nessie client with configuration
NESSIE_URL = "http://localhost:19120/api/v1"
USERNAME = "admin"  # Replace with your Nessie username
PASSWORD = "admin123"  # Replace with your Nessie password

# Build the configuration
config = build_config(
    {
        "nessie.url": NESSIE_URL,
        "nessie.auth.type": "BASIC",  # Use BASIC authentication
        "nessie.auth.username": USERNAME,
        "nessie.auth.password": PASSWORD,
    }
)

# Initialize the Nessie client
client = NessieClient(config)


def list_references():
    """List all references (branches and tags) in the Nessie catalog."""
    references_response = client.list_references()
    references = references_response.references  # Access the list of references
    print("References:")
    for ref in references:
        print(f"- {ref.name} ({ref})")


def create_branch(branch_name, source_ref="main"):
    source_ref_details = client.get_reference(source_ref)
    try:
        branch = client.create_branch(branch_name, hash_on_ref=source_ref_details.hash_)
        print(f"Branch '{branch_name}' created from '{source_ref}'.")
        return branch
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_tag(tag_name, source_ref):
    source_ref_details = client.get_reference(source_ref)
    try:
        tag = client.create_tag(tag_name, ref=source_ref, hash_on_ref=source_ref_details.hash_)
        print(f"Tag '{tag_name}' created successfully from reference '{source_ref}' at commit '{tag.hash_}'.")
        return tag
    except Exception as e:
        print(f"Error: {e}")
        return None


def create_table(table_name, schema, branch_name="main"):
    try:
        client.create_table(table_name, schema, branch_name)
        print(f"Table '{table_name}' created in branch '{branch_name}'.")
    except Exception as e:
        print(f"Error: {e}")

# Example usage
table_schema = {
    "type": "struct",
    "fields": [
        {"name": "id", "type": "int", "required": True},
        {"name": "name", "type": "string", "required": True},
        {"name": "created_at", "type": "timestamp", "required": False},
    ],
}
create_table("my_table", table_schema)


if __name__ == "__main__":
    list_references()
    create_branch("bugfix-branch")
    create_tag("v4.0.0", source_ref="main")
    list_references()
