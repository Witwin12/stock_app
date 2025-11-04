from django.contrib import admin
from .models.employee import Employee 
from .models.stock_out_transaction import StockOutTransaction
from .models.tire_lot import TireLot
from .models.tire_product import TireProduct

admin.site.register(Employee)
admin.site.register(StockOutTransaction)
admin.site.register(TireLot)
admin.site.register(TireProduct)