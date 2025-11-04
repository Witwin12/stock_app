from django.db import models
from django.contrib.auth.models import AbstractUser

class Employee(AbstractUser):
    """
    เก็บข้อมูลของผู้ใช้งาน (โดยขยายจาก User มาตรฐานของ Django)
    """

    class Role(models.TextChoices):
        ADMIN = 'admin', 'แอดมิน'
        STAFF = 'staff', 'พนักงาน'

    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.STAFF
    )
    
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.username