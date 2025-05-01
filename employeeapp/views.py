from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from employeeapp.models import Client
from django.db import transaction
from employeeapp.utils.generate_api_key import generate_api_key
from employeeapp.utils.save_api_key import save_api_key

class ClientAPIView(APIView):
    def post(self, request):
        try:
            with transaction.atomic():
                name = request.data["name"]

                client_object = Client(name=name)

                client_object.save()
                client_id = client_object.id 

                api_key = generate_api_key()
                secret_name, version_name = save_api_key(client_id, api_key)

                return Response({"status": "success", "data": {"message": "Client registered successfully.", "client_id": client_id, "api_key": api_key}}, status=status.HTTP_200_OK)

        except Exception as e:
            print('debug exception ', e)
            return Response({"status": "error", "data": {"message": "Failed to register client.", "error": e}}, status=status.HTTP_400_BAD_REQUEST)
