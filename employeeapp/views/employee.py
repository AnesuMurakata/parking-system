import pandas as pd
from io import TextIOWrapper
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from employeeapp.models import Employee
from django.core.exceptions import ValidationError 
from employeeapp.authentication.authentication import ApiKeyAuthentication

class EmployeeAPIView(APIView):
    authentication_classes = [ApiKeyAuthentication]

    def get(self, request):
        client = request.user
        employees = Employee.objects.filter(client=client)

        return Response({"data": employees}, status=status.HTTP_200_OK)

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
        expected_cols = {"email", "first_name", "last_name", "license_plate"}
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
                first_name=row["first_name"]
                last_name=row["last_name"],
                license_plate=row["license_plate"]
                client=client
            )
            employees.append(employee)

        try:
            Employee.objects.bulk_create(employees, ignore_conflicts=True)
        except ValidationError as e:
            return Response({"detail": f"Validation error: {e}"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"data": f"Successfully uploaded {len(employees)} employees."}, status=status.HTTP_201_CREATED)

