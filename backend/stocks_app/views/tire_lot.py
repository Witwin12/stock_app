from rest_framework import generics ,viewsets
from ..models import TireLot
from ..serializers import TireLotSerializer

class TireLotInAPIView(generics.CreateAPIView):
    """
    API Endpoint สำหรับการรับยางเข้าสต็อก (Stock In)
    
    ส่ง JSON ที่มี brand, pattern, size, year_manufactured, 
    date_in, และ quantity_in
    
    ระบบจะสร้าง TireProduct (หากยังไม่มี) และ TireLot ให้อัตโนมัติ
    """
    queryset = TireLot.objects.all()
    serializer_class = TireLotSerializer

class TireLotViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API ViewSet สำหรับ 'ดึงข้อมูล' ล็อต (TireLot)
    - GET /api/tire-lots/ (ดูทุกล็อต)
    - GET /api/tire-lots/{id}/ (ดูรายละเอียดล็อตเดียว)
    """
    queryset = TireLot.objects.all().order_by('-date_in')
    serializer_class = TireLotSerializer