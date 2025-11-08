from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from ..models import TireProduct
from ..serializers import TireProductSerializer
from ..serializers import TireLotSerializer 

class TireProductViewSet(viewsets.ModelViewSet):
    """
    API ViewSet สำหรับจัดการข้อมูลยาง (TireProduct)
    """
    serializer_class = TireProductSerializer

    def get_queryset(self):
        """
        Override เมธอดนี้เพื่อเพิ่ม logic การ search
        """
        
        # Queryset พื้นฐาน (ที่กรอง is_active=True เสมอ)
        queryset = TireProduct.objects.all()
        
        # 4. ดึงค่า search params จาก URL
  
        brand = self.request.query_params.get('brand')
        pattern = self.request.query_params.get('pattern')
        size = self.request.query_params.get('size')
        search = self.request.query_params.get('search')
        
        # --- 5. ใช้ .filter() ต่อเนื่อง ( chaining ) ---
        if brand:
            # __icontains = ค้นหาแบบ "มีคำนี้" (ไม่สนตัวเล็ก/ใหญ่)
            queryset = queryset.filter(brand__icontains=brand)
        
        if pattern:
            queryset = queryset.filter(pattern__icontains=pattern)
        
        if size:
            queryset = queryset.filter(size__icontains=size)

        # 6. การกรองแบบ OR 
        if search:
            # สร้างเงื่อนไข "หรือ"
            queryset = queryset.filter(
                Q(brand__icontains=search) |
                Q(pattern__icontains=search) |
                Q(size__icontains=search)
            )
            
        # 7. เรียงลำดับผลลัพธ์
        return queryset.order_by('-is_active', 'brand', 'pattern')
    
    @action(detail=True, methods=['get'])
    
    def stock_by_year(self, request, pk=None):
        """
        API สำหรับดูสต็อกคงเหลือของยางรุ่นนี้  
        โดยแจกแจงตามล็อตและปีผลิต
        """
        try:
            # 1. ดึงข้อมูลยางเส้นที่ต้องการ 
            product = self.get_object() 
            
            # 2. ตรวจสอบว่ามีการ Filter ปี มาใน Query Param หรือไม่

            year_filter = request.query_params.get('year', None)

            # 3. ดึง "ล็อต" (TireLot) ทั้งหมดที่เกี่ยวข้องกับยางเส้นนี้
            lots_queryset = product.lots.all()

            if year_filter:
                # 4. ถ้ามีการกรองปี ให้ Query เฉพาะปีนั้น
                lots_queryset = lots_queryset.filter(year_manufactured=year_filter)

            # 5. ใช้ TireLotSerializer เพื่อแปลงข้อมูลล็อต (ที่มีค่าคงเหลือ)
            serializer = TireLotSerializer(lots_queryset, many=True)
            
            # 6. ส่งข้อมูลกลับไปเป็น JSON
            return Response(serializer.data)

        except TireProduct.DoesNotExist:
            return Response(
                {"error": "Product not found"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )