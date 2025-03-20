import requests
import json

from requests.auth import HTTPBasicAuth

NESSIE_URL = "http://localhost:19120/api/v1"
USERNAME = "admin"
PASSWORD = "admin123"


def check_nessie_status():
    """Check if the Nessie server is running."""
    response = requests.get(f"{NESSIE_URL}/config")
    print("Server Status:", response.json())


def list_branches():
    """List all branches."""
    response = requests.get(f"{NESSIE_URL}/trees")
    print("Branches:", response.json())


def create_nessie_branch(branch_name, source_ref="main", auth=None):
    url = f"{NESSIE_URL}/tree/{branch_name}"
    headers = {"Content-Type": "application/json"}
    payload = {"sourceRefName": source_ref}

    try:
        if auth:
            response = requests.put(url, headers=headers, data=json.dumps(payload), auth=auth)
        else:
            response = requests.put(url, headers=headers, data=json.dumps(payload))

        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error creating branch: {e}")
        if response is not None:
          try:
            print(f"Server response: {response.json()}")
          except:
            print(f"Server response code: {response.status_code}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        return None




def list_tables(branch_name="main"):
    """List all tables in a branch."""
    response = requests.get(f"{NESSIE_URL}/contents", params={"ref": branch_name})
    print(f"Tables in branch '{branch_name}':", response.json())

def get_table_details(table_name, branch_name="main"):
    """Get details of a specific table."""
    response = requests.get(f"{NESSIE_URL}/contents/{table_name}", params={"ref": branch_name})
    print(f"Table '{table_name}' details:", response.json())

def create_tag(tag_name, hash_ref="LATEST"):
    """Create a new tag."""
    data = {"name": tag_name, "hash": hash_ref}
    response = requests.post(f"{NESSIE_URL}/trees/tag", json=data)
    print(f"Tag '{tag_name}' created:", response.json())

def make_commit(table_name, branch_name="main", metadata_location="s3://my-bucket/path/to/metadata.json"):
    """Make a commit (modify a table)."""
    data = {
        "type": "ICEBERG_TABLE",
        "reference": branch_name,
        "message": "Updating table schema",
        "contents": {"metadataLocation": metadata_location}
    }
    response = requests.post(f"{NESSIE_URL}/contents/{table_name}", json=data)
    print(f"Commit made on '{table_name}':", response.json())

def merge_branch(from_branch, to_branch="main"):
    """Merge a branch into main."""
    data = {"fromRefName": from_branch, "toRefName": to_branch, "hash": "LATEST"}
    response = requests.post(f"{NESSIE_URL}/trees/merge", json=data)
    print(f"Branch '{from_branch}' merged into '{to_branch}':", response.json())

def delete_branch(branch_name):
    """Delete a branch."""
    response = requests.delete(f"{NESSIE_URL}/trees/branch/{branch_name}")
    print(f"Branch '{branch_name}' deleted:", response.json())

# Example Usage:
if __name__ == "__main__":
    # check_nessie_status()
    list_branches()
    create_nessie_branch("my-feature-branch")
    # list_tables("my-feature-branch")
    # list_tables("main")
    # get_table_details("my_table", "my-feature-branch")
    # create_tag("v1.0")
    # make_commit("my_table", "my-feature-branch")
    # merge_branch("my-feature-branch", "main")
    # delete_branch("my-feature-branch")
