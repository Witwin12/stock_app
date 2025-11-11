from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models.employee import Employee 
from .models.stock_out_transaction import StockOutTransaction
from .models.tire_lot import TireLot
from .models.tire_product import TireProduct

class EmployeeAdmin(UserAdmin):
    model = Employee

    # --- ส่วนนี้สำคัญมาก ---
    # ทำให้ field 'role' และ 'name' ของเรา
    # แสดงในหน้า Admin อย่างถูกต้อง

    # 1. แสดงใน "หน้า List" (ตาราง)
    list_display = ('username', 'email', 'name', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')

    # 2. แสดงใน "หน้า Change User" (แบบฟอร์ม)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'name')}),
    )
    
    # 3. แสดงใน "หน้า Add User"
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'name')}),
    )
admin.site.register(Employee,EmployeeAdmin)
admin.site.register(StockOutTransaction)
admin.site.register(TireLot)
admin.site.register(TireProduct)