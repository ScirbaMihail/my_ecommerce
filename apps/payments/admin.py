# unfold
from unfold.admin import ModelAdmin
from unfold.sections import TableSection

# django
from django.contrib import admin

# local
from apps.payments.models import Order, Transaction
from apps.core.mixins import ReadOnlyMixin


# Register your models here.
class ProductTableSection(TableSection):
    verbose_name = "Products"
    height = 400
    related_name = "products"
    fields = ("name", "description", "price")


@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ("id", "user__email", "cost", "status")
    list_sections = (
        ProductTableSection,
    )


@admin.register(Transaction)
class TransactionAdmin(ReadOnlyMixin, ModelAdmin):
    list_display = ("id", "order__user__email", "amount", "status")
