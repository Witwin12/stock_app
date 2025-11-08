from rest_framework import serializers
from ..models import TireLot, TireProduct

class StockInSerializer(serializers.ModelSerializer):
    """
    Serializer สำหรับ 'รับเข้าสต็อก' (WriteOnly)
    """
    # --- 1. Fields สำหรับ Input (รับค่า brand, pattern, size) ---
    brand = serializers.CharField(max_length=50, write_only=True, label="ยี่ห้อ")
    pattern = serializers.CharField(max_length=50, write_only=True, label="ลายดอกยาง")
    size = serializers.CharField(max_length=50, write_only=True, label="ขนาด") 

    class Meta:
        model = TireLot
        fields = [
            'lot_id',
            'brand',              # (Input)
            'pattern',            # (Input)
            'size',               # (Input)
            'year_manufactured',  # (Input)
            'date_in',            # (Input)
            'quantity_in',        # (Input)
            'is_active',          # (Input - optional)
        ]
        read_only_fields = ['lot_id']
        
    def validate_quantity_in(self, value):
        if value <= 0:
            raise serializers.ValidationError("จำนวนที่รับเข้าต้องเป็นค่าบวก")
        return value
    
    def create(self, validated_data):
        product_data = {
            'brand': validated_data.pop('brand'),
            'pattern': validated_data.pop('pattern'),
            'size': validated_data.pop('size')
        }
        product, created = TireProduct.objects.get_or_create(**product_data)
        
        # (เพิ่ม) ถ้าสร้าง Product ใหม่ ให้ Active
        if not product.is_active:
             product.is_active = True
             product.save()

        lot = TireLot.objects.create(product=product, **validated_data)
        return lot