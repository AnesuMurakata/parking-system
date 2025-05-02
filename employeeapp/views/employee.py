import pandas as pd
from io import TextIOWrapper
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from employeeapp.models import Employee
from django.core.exceptions import ValidationError 
from employeeapp.serializers.employee import EmployeeSerializer
from employeeapp.authentication.authentication import ApiKeyAuthentication

class EmployeeAPIView(APIView):
    authentication_classes = [ApiKeyAuthentication]

    def get(self, request):
        client = request.user
        employees = Employee.objects.filter(client=client)
        serializer = EmployeeSerializer(employees, many=True)
        
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        client = request.user
        file_obj = request.FILES.get("file")

        if not file_obj:
            return Response({"detail": "No file uploaded."}, status=status.HTTP_400_BAD_REQUEST)

        # Determine file type
        file_name = file_obj.name.lower()
        try:
            if file_name.endswith('.csv'):
                df = pd.read_csv(TextIOWrapper(file_obj, encoding='utf-8'))
            elif file_name.endswith('.xlsx'):
                df = pd.read_excel(file_obj, engine='openpyxl')
            else:
                return Response({"detail": "Unsupported file type. Upload CSV or Excel."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": f"Error reading file: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate expected columns
        expected_cols = {"email", "first name", "last name", "license plate"}
        if not expected_cols.issubset(df.columns.str.lower()):
            return Response(
                {"detail": f"File must contain columns: {expected_cols}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Normalize column names in case of casing mismatch
        df.columns = df.columns.str.lower()

        # Create Employee instances
        employees = []
        for _, row in df.iterrows():
            employee = Employee(
                email=row["email"],
                first_name=row["first name"],
                last_name=row["last name"],
                license_plate=row["license plate"],
                client=client
            )
            employees.append(employee)

        try:
            Employee.objects.bulk_create(employees, ignore_conflicts=True)
        except ValidationError as e:
            return Response({"detail": f"Validation error: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": f"Successfully uploaded {len(employees)} employees."}, status=status.HTTP_201_CREATED)

    def delete(self, request):
        client = request.user
        email = request.data.get("email")

        if not email:
            return Response({"detail": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # check client as well to ensure clients can only delete their employees
            employee = Employee.objects.get(email=email, client=client)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)

        employee.delete()
        return Response({"data": f"Employee with email {email} has been deleted."}, status=status.HTTP_204_NO_CONTENT)
