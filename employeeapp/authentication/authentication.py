from employeeapp.models import Client
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import BaseAuthentication
from employeeapp.authentication.exceptions import NoAuthToken, InvalidAuthToken
from employeeapp.utils.validate_api_key import validate_api_key_with_cache

class ApiKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        try:
            auth_header = request.headers["Authorization"]
        except:
            raise NoAuthToken()

        if "uid" in auth_header:
            client_id = auth_header.rsplit("uid", 1)[1]
            api_key = auth_header.rsplit("uid", 1)[0]

            is_valid = validate_api_key_with_cache(client_id, api_key)

            if is_valid:
                client = Client.objects.get(id=int(client_id))
                client.is_authenticated = True

                return (client, api_key)
            else:
                raise AuthenticationFailed("Invalid API Key")
        else:
            raise InvalidAuthToken()
