from rest_framework import serializers
from ..models import StockOutTransaction
from .tire_product import TireProductSerializer

class StockOutTransactionSerializer(serializers.ModelSerializer):
    
    # --- การแสดงผล ForeignKey ให้อ่านง่าย ---
    
    # ดึงค่า __str__ จาก `TireLot`
    lot_display = serializers.StringRelatedField(source='lot', read_only=True)
    
    # ดึงค่า 'username' จาก `Employee` ที่เชื่อมโยงอยู่
    employee_username = serializers.ReadOnlyField(source='employee.username')

    product = TireProductSerializer(source = 'lot.product',read_only=True)
    #แสดงยอดคงเหลือของล็อต (ณ ก่อนเบิก) เพื่อให้ Response ชัดเจน
    lot_remaining_before_txn = serializers.ReadOnlyField(source='lot.quantity_remaining')

    class Meta:
        model = StockOutTransaction
        fields = [
            'transaction_id',
            
            # --- 2. Fields สำหรับ Input (Write) ---
            'lot',                # นี่คือ Input: User ต้องส่ง 'lot_id' ที่จะเบิก
            'employee',           # นี่คือ Input: User ต้องส่ง 'employee_id'
            'date_out',
            'quantity_out',
            'remarks',
            
            # --- 3. Fields สำหรับ Output (Read-only) ---
            'product',            # (แสดงผล)
            'lot_display',        # (แสดงผล)
            'employee_username',  # (แสดงผล)
            'lot_remaining_before_txn' # (แสดงผล)
            ]
        read_only_fields = ['transaction_id']

    def validate_quantity_out(self, value):
        """
        ตรวจสอบว่า 'จำนวนที่เบิก' ต้องมากกว่า 0
        """
        if value <= 0:
            raise serializers.ValidationError("จำนวนที่เบิกออกต้องมากกว่า 0")
        return value

    def validate(self, data):
        """
        ตรวจสอบ Logic โดยรวม:
        - จำนวนที่เบิก (quantity_out) ต้องไม่เกินยอดคงเหลือ (quantity_remaining) 
        - ของ 'lot' ที่ระบุมา
        """
        
        lot_object = data.get('lot')
        quantity_to_stock_out = data.get('quantity_out')

        if lot_object and quantity_to_stock_out:
            
            # 1. ดึงยอดคงเหลือจาก @property ของ Model
            remaining_stock = lot_object.quantity_remaining
            
            # 2. ตรวจสอบ
            if quantity_to_stock_out > remaining_stock:
                raise serializers.ValidationError(
                    f"เบิกออก ({quantity_to_stock_out} เส้น) เกินจำนวนคงเหลือ ({remaining_stock} เส้น) ของล็อตนี้"
                )
                
        return data
    
    def create(self, validated_data):
        """
        Override เมธอด create
        เพื่อเพิ่ม Logic ตรวจสอบสต็อกหลังเบิกออก
        """
        
        # 1. สร้าง Transaction (เบิกออก) ตามปกติ
        #    (บันทึกลง DB)
        transaction = super().create(validated_data)
        
        # 2. ดึง Product ที่เกี่ยวข้อง
        #    validated_data['lot'] คือ <TireLot object>
        product = validated_data['lot'].product 

        # 3. ตรวจสอบสต็อกคงเหลือ *หลังจาก* บันทึก transaction นี้

        if product.total_stock_on_hand == 0:
            
            # 4. ถ้าสต็อกเป็น 0 ให้ตั้งค่า is_active = False
            product.is_active = False
            product.save()
            
        # 5. ส่ง transaction กลับไป
        return transaction
