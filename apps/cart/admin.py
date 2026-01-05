from django.contrib import admin
from unfold.admin import ModelAdmin
from apps.cart.models import Cart

# Register your models here.
@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('user__email',)