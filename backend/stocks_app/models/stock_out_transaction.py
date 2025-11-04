from django.db import models
from django.utils import timezone
from .employee import Employee 
from .tire_lot import TireLot

class StockOutTransaction(models.Model):
    """
    เก็บประวัติการเบิกออก (1 record = 1 ครั้งที่เบิก)
    """
    transaction_id = models.AutoField(primary_key=True)
    
    # --- เชื่อมโยงกับ 'ล็อต' ที่เบิกออกไป ---
    lot = models.ForeignKey(
        TireLot, 
        on_delete=models.CASCADE, 
        related_name='stock_outs', # ทำให้เรียก lot.stock_outs.all() ได้
        verbose_name="ล็อตที่เบิก"
    )
    
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.SET_NULL,
        null=True,
        related_name='stock_out_transactions',
        verbose_name="พนักงาน"
    )
    
    date_out = models.DateField(default=timezone.now, verbose_name="วันที่เบิกออก")
    quantity_out = models.IntegerField(default=0, verbose_name="จำนวนที่เบิก")
    remarks = models.TextField(blank=True, null=True, verbose_name="หมายเหตุ")

    def __str__(self):
        return f"เบิก {self.lot.product} ({self.quantity_out} เส้น) - จากล็อตปี {self.lot.year_manufactured}"

    class Meta:
        verbose_name = "ประวัติการเบิกออก"
        verbose_name_plural = "ประวัติการเบิกออก (Stock Out)"
        ordering = ['-date_out']