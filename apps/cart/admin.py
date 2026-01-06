from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from apps.cart.models import Cart, CartProduct

# Register your models here.
class CartProductInline(TabularInline):
    model = CartProduct
    extra = 1
    autocomplete_fields = ['product']

@admin.register(Cart)
class CartAdmin(ModelAdmin):

    list_display = ('id', 'user__email', 'cost')
    exclude = ('cost',)
    inlines = [CartProductInline]