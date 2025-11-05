from rest_framework import serializers
from ..models import TireLot

class TireLotSerializer(serializers.ModelSerializer):
    
    # --- การดึงค่าจาก @property ---
    total_out = serializers.ReadOnlyField()
    quantity_remaining = serializers.ReadOnlyField()
    

    product_display = serializers.StringRelatedField(source='product', read_only=True)

    class Meta:
        model = TireLot
        fields = [
            'lot_id',
            'product',            # ฟิลด์นี้จะรับ/แสดงเป็น "ID" (สำหรับการ POST/PUT)
            'product_display',    # ฟิลด์นี้จะแสดงเป็น "ชื่อ" (สำหรับการ GET)
            'year_manufactured',
            'date_in',
            'quantity_in',
            'total_out',          # ยอดเบิกออก 
            'quantity_remaining'  # ยอดคงเหลือ 
        ]