from rest_framework import generics
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