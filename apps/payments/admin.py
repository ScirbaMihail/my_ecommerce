# unfold
from unfold.admin import ModelAdmin

# django
from django.contrib import admin

# local
from apps.payments.models import Order, Transaction
from apps.core.mixins import ReadOnlyMixin


# Register your models here.
@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "user__email", "cost", "status")


@admin.register(Transaction)
class TransactionAdmin(ReadOnlyMixin, ModelAdmin):
    list_display = ("id", "order__user__email", "amount", "status")
