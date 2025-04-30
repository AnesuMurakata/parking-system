from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from employeeapp.models import Client

# Create your views here.
class ClientAPIView(APIView):
    def post(self, request):
        try:
            name = request.data["name"]
            email = request.data["email"]

            client_object = Client(name=name, email=email)

            client_object.save()

            return Response({"status": "success", "data": "Client registered successfully."}, status=status.HTTP_200_OK)

        except Exception as e:
            print('debug exception ', e)
            return Response({"status": "error", "data": {"message": "Failed to register client.", "error": e}}, status=status.HTTP_400_BAD_REQUEST)
