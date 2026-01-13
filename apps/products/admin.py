# django
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# unfold
from unfold.admin import ModelAdmin

# local
from apps.products.models import Product, Category


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

    conditional_fields = {"description": "has_description"}
