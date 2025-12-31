from django.contrib import admin
from django.contrib.auth import get_user_model
from unfold.admin import ModelAdmin

User = get_user_model()
# Register your models here.
@admin.register(User)
class UserAdmin(ModelAdmin):
    list_display = ('id', 'email', 'balance')