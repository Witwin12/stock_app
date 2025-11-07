from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.tire_product import TireProductViewSet
from .views.tire_lot import TireLotInAPIView ,TireLotViewSet
from .views.lot_out import StockOutCreateAPIView

# 1. สร้าง Router
router = DefaultRouter()

# 2. ลงทะเบียน ViewSet กับ Router
# router.register(r'ชื่อ-url', ViewSet, basename='ชื่อ-อ้างอิง')
router.register(r'tire-products', TireProductViewSet, basename='tireproduct')
router.register(r'tire-lots', TireLotViewSet, basename='tirelot')
# 3. ให้ urlpatterns ใช้งาน Router
urlpatterns = [
    path('', include(router.urls)),
    path('stock-in/', TireLotInAPIView.as_view(), name='api-stock-in'),
    path('stock-out/',StockOutCreateAPIView.as_view(), name='api-stock-out' )

]