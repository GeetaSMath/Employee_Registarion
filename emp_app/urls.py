from django.contrib import admin
from django.urls import path, include
from .views import EmployeeCreateAPIView, EmployeeUpdateAPIView, EmployeeDeleteAPIView, EmployeeRetrieveAPIView

urlpatterns = [
    path('create_employee', EmployeeCreateAPIView.as_view(), name='create_employee'),
    path('update/<int:regid>/', EmployeeUpdateAPIView.as_view(), name='employee-update'),
    path('delete/', EmployeeDeleteAPIView.as_view(), name='employee-delete'),
    path('get/', EmployeeRetrieveAPIView.as_view(), name='employee-get'),
]