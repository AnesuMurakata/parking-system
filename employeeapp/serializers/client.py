from rest_framework import serializers
from employeeapp.models.client import Client

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'name']
