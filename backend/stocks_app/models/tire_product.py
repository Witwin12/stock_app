from django.db import models
from django.db.models import Sum

class TireProduct(models.Model):
    """
    ตารางเก็บข้อมูลหลักของยาง (Product Master)
    เช่น Michelin Pilot Sport 4 (225/45R17)
    """
    product_id = models.AutoField(primary_key=True)
    brand = models.CharField(max_length=50, verbose_name="ยี่ห้อ")
    pattern = models.CharField(max_length=50, verbose_name="ลายดอกยาง")
    size = models.CharField(max_length=50, verbose_name="ขนาด")
    is_active = models.BooleanField(
        default=True, 
        verbose_name="active",
        db_index=True  
    )

    @property
    def total_stock_on_hand(self):
        """
        คำนวณสต็อกคงเหลือ 'ทั้งหมด' ของยางรุ่นนี้ (รวมทุกปีผลิต)
        """

        from .stock_out_transaction import StockOutTransaction
        
        # หายอดรวมเข้าทั้งหมด (จากล็อตที่อ้างอิงถึง product นี้)
        total_in = self.lots.aggregate(total=Sum('quantity_in'))['total'] or 0
        
        # หายอดเบิกออกทั้งหมด (จาก transaction ที่อ้างอิงผ่าน lot กลับมายัง product นี้)
        total_out = StockOutTransaction.objects.filter(
            lot__product=self
        ).aggregate(total=Sum('quantity_out'))['total'] or 0
        
        return total_in - total_out
    
    def get_stock_by_year(self, year):
        """
        คำนวณสต็อกคงเหลือ โดยระบุปีผลิต
        """
        from .stock_out_transaction import StockOutTransaction
        
        # หาล็อตของปีที่ระบุ
        lots_in_year = self.lots.filter(year_manufactured=year)
        
        # ยอดรับเข้าของปีนั้น
        total_in = lots_in_year.aggregate(total=Sum('quantity_in'))['total'] or 0
        
        # ยอดเบิกออกของปีนั้น
        total_out = StockOutTransaction.objects.filter(
            lot__product=self, 
            lot__year_manufactured=year
        ).aggregate(total=Sum('quantity_out'))['total'] or 0
        
        return total_in - total_out

    def __str__(self):
        return f"{self.brand} {self.pattern} ({self.size})"

    class Meta:
        verbose_name = "ข้อมูลยาง (Master)"
        verbose_name_plural = "ข้อมูลยาง (Master)"
        unique_together = ('brand', 'pattern', 'size')