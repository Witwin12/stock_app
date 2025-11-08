from rest_framework import serializers
from ..models import TireProduct  

class TireProductSerializer(serializers.ModelSerializer):
    
    # --- การดึงค่าจาก @property ---
    total_stock_on_hand = serializers.ReadOnlyField()
    stock_status = serializers.ReadOnlyField()

    class Meta:
        model = TireProduct
        fields = [
            'product_id', 
            'brand', 
            'pattern', 
            'size',
            'total_stock_on_hand',
            'is_active',
            'stock_status'
        ]