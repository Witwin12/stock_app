from rest_framework import serializers
from ..models import TireLot
from .tire_product import TireProductSerializer


class TireLotSerializer(serializers.ModelSerializer):
    """
    Serializer สำหรับ 'อ่าน' ข้อมูล Lot (ReadOnly)
    """
    # --- 1. Field สำหรับ Output (แสดงข้อมูล Product ที่เชื่อมโยง) ---
    product = TireProductSerializer(read_only=True)

    # --- 2. การดึงค่าจาก @property ---
    total_out = serializers.ReadOnlyField()
    quantity_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = TireLot
        fields = [
            'lot_id',
            'product',            # (Output) Nested Object
            'year_manufactured',
            'date_in',
            'quantity_in',
            'total_out',          # (Output)
            'quantity_remaining', # (Output)
            'is_active'
        ]
        read_only_fields = ['lot_id']