from rest_framework import serializers
from ..models import TireLot
from .tire_product import TireProductSerializer
from ..models import TireProduct
class TireLotSerializer(serializers.ModelSerializer):

   # --- 1. Fields สำหรับ Input (รับค่า brand, pattern, size) ---
    brand = serializers.CharField(max_length=50, write_only=True, label="ยี่ห้อ")
    pattern = serializers.CharField(max_length=50, write_only=True, label="ลายดอกยาง")
    size = serializers.CharField(max_length=50, write_only=True, label="ขนาด") 
    # --- 2. Field สำหรับ Output (แสดงข้อมูล Product ที่เชื่อมโยง) ---
    product = TireProductSerializer(read_only=True)

    # --- การดึงค่าจาก @property ---
    total_out = serializers.ReadOnlyField()
    quantity_remaining = serializers.ReadOnlyField()
    

    class Meta:
        model = TireLot
        fields = [
            'lot_id',
            'product',            # (Output) Nested Object
            
            'brand',              # (Input)
            'pattern',            # (Input)
            'size',               # (Input)
            
            'year_manufactured',  # (Input/Output)
            'date_in',            # (Input/Output)
            'quantity_in',        # (Input/Output)
            
            'total_out',          # (Output)
            'quantity_remaining'  # (Output)
        ]
        read_only_fields = ['lot_id']

    def validate_quantity_in(self, value):
        """
        ตรวจสอบว่าจำนวนที่รับเข้าต้องมากกว่า 0
        """
        if value <= 0:
            raise serializers.ValidationError("จำนวนที่รับเข้าต้องเป็นค่าบวก")
        return value
    
    def create(self, validated_data):
        """
        Override เมธอด create เพื่อจัดการ logic การสร้าง 2 models
        """
        
        # 1. ดึงข้อมูลของ Product ออกมาจาก validated_data
        product_data = {
            'brand': validated_data.pop('brand'),
            'pattern': validated_data.pop('pattern'),
            'size': validated_data.pop('size')
        }
        
        # 2. ค้นหา หรือ สร้าง TireProduct
        #    ใช้ get_or_create() ซึ่งจะจัดการ unique_together ให้อัตโนมัติ
        product, created = TireProduct.objects.get_or_create(**product_data)
        
        # 3. สร้าง TireLot
        #    - 'validated_data' ตอนนี้จะเหลือแค่ field ของ TireLot
        #    - เราส่ง 'product' (object) ที่เราเพิ่งค้นหา/สร้างเสร็จเข้าไป
        lot = TireLot.objects.create(product=product, **validated_data)
        
        return lot