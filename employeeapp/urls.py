from django.urls import path
from employeeapp.views.client import ClientAPIView
from employeeapp.views.employee import EmployeeAPIView

urlpatterns = [
    path('client', ClientAPIView.as_view()),
    path('employee', EmployeeAPIView.as_view()),
]