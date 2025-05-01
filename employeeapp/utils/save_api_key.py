from google.cloud import secretmanager
from google.api_core.exceptions import AlreadyExists, NotFound, PermissionDenied, InvalidArgument

def save_api_key(client_id, api_key):
    """
    Stores the API key in Secret Manager, using the client_id as the Secret ID.
    Returns:
        tuple: (secret_name, version_name) or (None, None) on failure.
    """

    # --- Validate Client ID as Secret ID ---
    secret_id = f"client-{client_id}" 

    # --- Prepare Payload ---
    # The API key is the payload, needs to be bytes
    payload_bytes = api_key.encode('utf-8')

    # --- Interact with Secret Manager ---
    try:
        client = secretmanager.SecretManagerServiceClient()
    except Exception as e:
        print(f"Error: Failed to create Secret Manager client. Is authentication configured? {e}")
        return None, None

    parent = "projects/crack-flight-443718-k3"
    secret_path = f"{parent}/secrets/{secret_id}"

    try:
        # 1. Create the Secret container (if it doesn't exist)
        print(f"Checking/Creating secret: {secret_path}")
        secret_request = {
            "parent": parent,
            "secret_id": secret_id,
            "secret": {
                # Define replication policy, automatic is common
                "replication": {"automatic": {}},
                # Optional: Add labels for organization
                "labels": {
                    "created-by": "django-command",
                    # Add other relevant labels like environment, client-type etc.
                }
            },
        }
        try:
            secret = client.create_secret(request=secret_request)
            print(f"Created new secret: {secret.name}")
        except AlreadyExists:
            print(f"Secret '{secret_id}' already exists. Will add version to existing secret.")
            # Fetch the existing secret object if needed later (e.g., to check labels)
            secret = client.get_secret(request={"name": secret_path})
        except PermissionDenied:
             print(f"Error: Permission denied to create/get secret '{secret_id}'. Check IAM roles (Secret Manager Admin?).")
             return None, None
        except InvalidArgument as e:
             print(f"Error: Invalid argument creating secret '{secret_id}'. Is the ID format correct? {e}")
             return None, None
        except Exception as e:
             print(f"An unexpected error occurred creating/getting secret '{secret_id}': {e}")
             return None, None

        # 2. Add the Secret Version (the API key)
        version_payload = {"data": payload_bytes}
        print(f"Adding secret version to: {secret.name}")
        version = client.add_secret_version(
            request={"parent": secret.name, "payload": version_payload}
        )
        print(f"Added secret version: {version.name}")
        return secret.name, version.name

    except PermissionDenied:
        print(f"Error: Permission denied to add version to secret '{secret_id}'. Check IAM roles (Secret Manager Secret Version Adder?).")
        return None, None
    except InvalidArgument as e:
        print(f"Error: Invalid argument adding version to secret '{secret_id}'. Payload issue? {e}")
        return None, None
    except Exception as e:
        print(f"An unexpected error occurred adding secret version for '{secret_id}': {e}")
        return None, None
