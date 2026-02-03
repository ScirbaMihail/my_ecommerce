# django
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# unfold
from unfold.admin import ModelAdmin

# local
from apps.products.models import Product, Category


class StockFilter(admin.SimpleListFilter):
    title = _("stock status")
    parameter_name = "stock_filter"

    def lookups(self, request, model_admin):
        return (
            ("in_stock", _("In stock")),
            ("missing", _("Missing")),
        )

    def queryset(self, request, queryset):
        if self.value() == "in_stock":
            return queryset.filter(in_stock=True)
        if self.value() == "missing":
            return queryset.filter(in_stock=False)
        return queryset


# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ("name",)


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ("id", "name", "category", "price", "in_stock")
    list_display_links = ("id", "name", "category", "price", "in_stock")
    exclude = ("in_stock",)
    search_fields = ("name",)
    list_filter = (StockFilter,)

    conditional_fields = {"description": "has_description"}
