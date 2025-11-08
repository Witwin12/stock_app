from rest_framework import generics ,viewsets, status
from rest_framework.response import Response 
from ..models import TireLot
from ..serializers import TireLotSerializer
from ..serializers import StockInSerializer

class TireLotInAPIView(generics.CreateAPIView):
    """
    API Endpoint สำหรับการรับยางเข้าสต็อก (Stock In)
    
    ส่ง JSON ที่มี brand, pattern, size, year_manufactured, 
    date_in, และ quantity_in
    
    ระบบจะสร้าง TireProduct (หากยังไม่มี) และ TireLot ให้อัตโนมัติ
    """
    queryset = TireLot.objects.all()
    serializer_class = StockInSerializer

class TireLotViewSet(viewsets.ModelViewSet):
    """
    API ViewSet สำหรับ 'ดึงข้อมูล' ล็อต (TireLot)
    - GET /api/tire-lots/ (ดูทุกล็อต)
    - GET /api/tire-lots/{id}/ (ดูรายละเอียดล็อตเดียว)
    """
    queryset = TireLot.objects.filter(is_active = True).order_by('-date_in')
    serializer_class = TireLotSerializer

    def destroy(self, request, *args, **kwargs):
        #ดึงล็อตที่จะลบ
        lot = self.get_object() 

        product = lot.product
        #ตรวจสอบเงื่อนไข
        if lot.total_out > 0:
            #ถ้ามีประวัติเบิก -> ห้ามลบ
            return Response(
                {'error': 'ลบไม่ได้: ล็อตนี้มีประวัติการเบิกออกไปแล้ว'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        #ถ้าไม่มีประวัติ (total_out == 0) -> ลบได้
        return super().destroy(request, *args, **kwargs)
    
        if response.status_code == status.HTTP_204_NO_CONTENT:

            if product.total_stock_on_hand == 0:
                product.is_active = False
                product.save()