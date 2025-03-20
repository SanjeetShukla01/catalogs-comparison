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
    if not source_ref_details:
        raise ValueError(f"Source reference '{source_ref}' does not exist.")
    client.create_branch(branch_name, hash_on_ref=source_ref_details.hash_)
    print(f"Branch '{branch_name}' created from '{source_ref}'.")


def create_tag(tag_name, source_ref):
    source_ref_details = client.get_reference(source_ref)
    try:
        tag = client.create_tag(tag_name, ref=source_ref, hash_on_ref=source_ref_details.hash_)
        print(f"Tag '{tag_name}' created successfully from reference '{source_ref}' at commit '{tag.hash_}'.")
        return tag
    except Exception as e:
        print(f"Error: {e}")
        return None


# def create_tag(tag_name, source_ref="main"):
#     """Create a new tag in the Nessie catalog."""
#     source_ref_details = client.get_reference(source_ref)
#     tag = Tag(name=tag_name, hash_=source_ref_details.hash_)
#     client.create_tag(tag_name, source_ref)
#     print(f"Tag '{tag_name}' created from '{source_ref}'.")


# Example usage
if __name__ == "__main__":
    # List all references
    list_references()
    # create_branch("dev-branch")
    # create_tag("v1.0.0", source_ref="main", commit_hash="abc123def456")
    create_tag("v1.0.0", source_ref="main")
