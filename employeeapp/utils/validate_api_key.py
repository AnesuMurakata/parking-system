from django.core.cache import cache
from google.cloud import secretmanager
from google.api_core.exceptions import NotFound, PermissionDenied, GoogleAPICallError
import logging

logger = logging.getLogger(__name__)

def validate_api_key_with_cache(client_id: str, provided_api_key: str) -> bool:
    if not client_id or not provided_api_key:
        return False

    cache_key = f"key_{client_id}"

    # Check Cache
    cached_api_key = cache.get(cache_key)

    if cached_api_key is not None:
        
        return cached_api_key == provided_api_key.split(" ")[1]
    else:
        # Cache Miss - Fetch from Secrets Manager
        try:
            client = secretmanager.SecretManagerServiceClient()
            # Use 'latest' to always get the current active version
            secret_version_name = f"projects/crack-flight-443718-k3/secrets/key_{client_id}/versions/latest"

            response = client.access_secret_version(request={"name": secret_version_name})
            actual_api_key = response.payload.data.decode("UTF-8")

            # Compare Fetched Key
            is_valid = actual_api_key == provided_api_key.split(" ")[1]

            if is_valid:
                # Store in Cache on successful validation
                cache_ttl = 60 * 60 * 24 # Default 1 day
                cache.set(cache_key, actual_api_key, timeout=cache_ttl)

            return is_valid

        except NotFound:
            logger.warning(f"Secret not found in Secret Manager for client_id: {client_id}")
            return False 
        except PermissionDenied:
            logger.error(f"Permission denied accessing secret for client_id: {client_id}")
            return False
        except GoogleAPICallError as e:
             logger.error(f"Google API error accessing secret for client_id {client_id}: {e}")
             return False
        except Exception as e:
            logger.exception(f"Unexpected error validating key for client_id {client_id}: {e}")
            return False