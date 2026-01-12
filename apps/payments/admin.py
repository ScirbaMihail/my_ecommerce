from unfold.admin import ModelAdmin
from django.contrib import admin
from rest_framework.mixins import DestroyModelMixin

from apps.core.mixins import ReadOnlyMixin
from apps.payments.models import Order

# Register your models here.
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ('id', 'user__email', 'cost', 'status')