from django.db import models
from django.db.models import Sum
from .tire_product import TireProduct 

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