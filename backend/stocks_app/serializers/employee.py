from rest_framework import serializers
from ..models import Employee  

class EmployeeSerializer(serializers.ModelSerializer):  # (2) ใช้ชื่อแบบ CapWords
    
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