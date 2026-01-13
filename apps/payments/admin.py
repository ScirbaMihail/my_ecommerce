# unfold
from unfold.admin import ModelAdmin
from unfold.sections import TableSection
from unfold.decorators import display

# django
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

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
    list_display = ("id", "user__email", "cost", "status", "mark_paid")
    list_display_links = ("id", "user__email", "cost", "status")
    list_sections = (ProductTableSection,)
    actions = None

    @display(description="Mark as paid")
    def mark_paid(self, obj):
        if obj.status != Order.Statuses.PENDING:
            return '-'
        url = reverse("orders-mark-paid", args=[obj.pk])
        button = f'<a href="{url}" id="mark-paid-btn">Mark paid</a>'
        return format_html(button, args=[])

    class Media:
        css = {"all": ("admin/payments/css/style.css",)}



@admin.register(Transaction)
class TransactionAdmin(ReadOnlyMixin, ModelAdmin):
    list_display = ("id", "order__user__email", "amount", "status")
    list_display_links = ("id", "order__user__email", "amount", "status")
