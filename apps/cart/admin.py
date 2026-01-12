# django
from django.contrib import admin

# unfold
from unfold.admin import ModelAdmin, TabularInline

# local
from apps.cart.models import Cart, CartProduct


# Register your models here.
class CartProductInline(TabularInline):
    model = CartProduct
    extra = 1
    autocomplete_fields = ["product"]


@admin.register(Cart)
class CartAdmin(ModelAdmin):

    list_display = ("id", "user__email", "cost")
    exclude = ("cost",)
    inlines = [CartProductInline]
