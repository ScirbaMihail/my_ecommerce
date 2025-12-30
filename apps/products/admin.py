from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.products.models import Product, Category
from django.utils.translation import gettext_lazy as _

# Register your models here.
@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ('name',)



@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'price', 'in_stock')
    readonly_fields = ('in_stock',)
    
    fieldsets = [
        (
            _(''),
            {'fields': ('name', 'description', 'category', 'price', 'amount')}
        )
    ]