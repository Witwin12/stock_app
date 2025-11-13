from rest_framework import serializers
from ..models import TireLot, TireProduct


class StockInSerializer(serializers.ModelSerializer):
    """Serializer สำหรับการรับยางเข้าสต็อก"""

    # --- ข้อมูลของสินค้า (WriteOnly) ---
    brand = serializers.CharField(max_length=50, write_only=True, label="ยี่ห้อ")
    pattern = serializers.CharField(max_length=50, write_only=True, label="ลายดอกยาง")
    size = serializers.CharField(max_length=50, write_only=True, label="ขนาด")

    class Meta:
        model = TireLot
        read_only_fields = ['lot_id']
        fields = [
            'lot_id',
            'brand',
            'pattern',
            'size',
            'year_manufactured',
            'date_in',
            'quantity_in',
            'is_active',
        ]

    def validate_quantity_in(self, value):
        if value <= 0:
            raise serializers.ValidationError("จำนวนที่รับเข้าต้องเป็นค่าบวก")
        return value

    def create(self, validated_data):
        product_data = {
            field: validated_data.pop(field)
            for field in ('brand', 'pattern', 'size')
        }
        product, _ = TireProduct.objects.get_or_create(**product_data)

        # เปิดการใช้งานสินค้าถ้ายังไม่ active
        if not product.is_active:
            product.is_active = True
            product.save(update_fields=['is_active'])

        return TireLot.objects.create(product=product, **validated_data)
