from rest_framework import serializers
from ..models import Employee  
from dj_rest_auth.serializers import UserDetailsSerializer

class EmployeeSerializer(serializers.ModelSerializer): 
    
    class Meta:
        model = Employee
        
        fields = [
            'id', 
            'username', 
            'email', 
            'name', 
            'role', 
            'first_name', 
            'last_name',  
        ]

class CustomUserDetailsSerializer(UserDetailsSerializer):
    class Meta(UserDetailsSerializer.Meta):
        model = Employee
        fields = ('id', 'username', 'email', 'name', 'role')