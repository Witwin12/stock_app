from rest_framework import serializers
from ..models import StockOutTransaction

class StockOutTransactionSerializer(serializers.ModelSerializer):
    
    # --- การแสดงผล ForeignKey ให้อ่านง่าย ---
    
    # ดึงค่า __str__ จาก `TireLot`
    lot_display = serializers.StringRelatedField(source='lot', read_only=True)
    
    # ดึงค่า 'username' จาก `Employee` ที่เชื่อมโยงอยู่
    employee_username = serializers.ReadOnlyField(source='employee.username')

    class Meta:
        model = StockOutTransaction
        fields = [
            'transaction_id',
            'lot',                # ฟิลด์นี้สำหรับรับ/แสดง "ID" ของ Lot
            'lot_display',        # ฟิลด์นี้สำหรับแสดง "รายละเอียด" ของ Lot
            'employee',           # ฟิลด์นี้สำหรับรับ/แสดง "ID" ของ Employee
            'employee_username',  # ฟิลด์นี้สำหรับแสดง "Username"
            'date_out',
            'quantity_out',
            'remarks'
        ]