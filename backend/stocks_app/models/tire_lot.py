from django.db import models
from django.db.models import Sum
from .tire_product import TireProduct 
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

class TireLot(models.Model):
    """
    ตารางเก็บ 'ล็อต' การรับเข้า (Stock In)
    เชื่อมโยง Product และ ปีผลิต เข้าด้วยกัน
    """
    lot_id = models.AutoField(primary_key=True)
    
    # --- เชื่อมโยงกับ Master Product ---
    product = models.ForeignKey(
        TireProduct, 
        on_delete=models.PROTECT, 
        related_name='lots', 
        verbose_name="สินค้า"
    )
    
    year_manufactured = models.IntegerField(verbose_name="ปีที่ผลิต")
    date_in = models.DateField(verbose_name="วันที่รับเข้า")
    quantity_in = models.IntegerField(default=0, verbose_name="จำนวนรับเข้า")
    
    is_active = models.BooleanField(
        default=True, 
        verbose_name="active",
        db_index=True  
    )
    @property
    def total_out(self):
        """คำนวณยอดเบิกออกทั้งหมดของ 'ล็อตนี้'"""

        from .stock_out_transaction import StockOutTransaction
        
        # self.stock_outs มาจาก related_name ของ StockOutTransaction
        result = self.stock_outs.aggregate(total=Sum('quantity_out'))
        return result['total'] or 0

    @property
    def quantity_remaining(self):
        """คำนวณจำนวนคงเหลือของ 'ล็อตนี้'"""
        return self.quantity_in - self.total_out

    def __str__(self):
        return f"{self.product} (ปี {self.year_manufactured}) - ล็อต {self.date_in}"

    class Meta:
        verbose_name = "ล็อตยาง (Stock In)"
        verbose_name_plural = "ล็อตยาง (Stock In)"

@receiver(post_delete, sender=TireLot)
def update_product_status_after_lot_delete(sender, instance, **kwargs):
    """
    เมื่อ TireLot ถูกลบ -> ตรวจสอบสต็อกใหม่ทั้งหมด
    """
    product = instance.product
    remaining = product.total_stock_on_hand
    product.is_active = remaining > 0
    product.save()


@receiver(post_save, sender=TireLot)
def update_product_status_after_lot_create(sender, instance, created, **kwargs):
    """
    เมื่อ TireLot ถูกสร้างหรืออัปเดต -> ตรวจสอบสต็อกอีกครั้ง
    """
    product = instance.product
    remaining = product.total_stock_on_hand
    if remaining > 0 and not product.is_active:
        product.is_active = True
        product.save()