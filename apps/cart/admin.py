# django
from django.contrib import admin

# unfold
from unfold.admin import ModelAdmin, TabularInline
from unfold.sections import TableSection

# local
from apps.cart.models import Cart, CartProduct


# Register your models here.
class ProductTableSection(TableSection):
    verbose_name = "Products"
    height = 400
    related_name = "products"
    fields = ("name", "description", "price")


class CartProductInline(TabularInline):
    model = CartProduct
    extra = 1
    autocomplete_fields = ["product"]


@admin.register(Cart)
class CartAdmin(ModelAdmin):

    list_display = ("id", "user__email", "cost")
    list_display_links = ("id", "user__email", "cost")
    list_sections = (ProductTableSection,)
    exclude = ("cost",)
    inlines = [CartProductInline]
    actions = None
