# unfold
from unfold.admin import ModelAdmin

# django
from django.contrib import admin

# local
from apps.payments.models import Order


# Register your models here.
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "user__email", "cost", "status")
