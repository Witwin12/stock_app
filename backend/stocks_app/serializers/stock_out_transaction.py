from rest_framework import serializers
from ..models import StockOutTransaction, Employee
from .tire_product import TireProductSerializer


class StockOutTransactionSerializer(serializers.ModelSerializer):
    """Serializer สำหรับการเบิกยางออกจากสต็อก"""

    # --- แสดงค่า ForeignKey ให้อ่านง่าย ---
    lot_display = serializers.StringRelatedField(source='lot', read_only=True)
    employee = serializers.SlugRelatedField(
        slug_field='username',
        queryset=Employee.objects.all()
    )
    product = TireProductSerializer(source='lot.product', read_only=True)
    lot_remaining_before_txn = serializers.ReadOnlyField(source='lot.quantity_remaining')

    class Meta:
        model = StockOutTransaction
        read_only_fields = ['transaction_id']
        fields = [
            'transaction_id',
            'lot',
            'employee',
            'date_out',
            'quantity_out',
            'remarks',
            'product',
            'lot_display',
            'lot_remaining_before_txn',
        ]

    # --- Validation ---
    def validate_quantity_out(self, value):
        if value <= 0:
            raise serializers.ValidationError("จำนวนที่เบิกออกต้องมากกว่า 0")
        return value

    def validate(self, data):
        lot = data.get('lot')
        qty_out = data.get('quantity_out')

        if not lot or not qty_out:
            return data

        remaining = lot.quantity_remaining
        if qty_out > remaining:
            raise serializers.ValidationError(
                f"เบิกออก {qty_out} เส้น เกินจำนวนคงเหลือ {remaining} เส้น ของล็อตนี้"
            )
        return data

    # --- Create Logic ---
    def create(self, validated_data):
        transaction = super().create(validated_data)
        product = validated_data['lot'].product

        # ถ้าสต็อกสินค้าหมดให้ปิดการใช้งานสินค้า
        if product.total_stock_on_hand == 0:
            product.is_active = False
            product.save(update_fields=['is_active'])

        return transaction
