import secrets

def generate_api_key(length=18):
    # Generates a secure URL-safe API key
    return secrets.token_urlsafe(length)
