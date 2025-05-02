from rest_framework import serializers
from employeeapp.models.employee import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id', 'email', 'first_name', 'last_name', 'license_plate']
        read_only_fields = ['id']
