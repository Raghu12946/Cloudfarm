from django.contrib import admin


from django.contrib import admin
from .models import UserRegistration, UserLogin
from .models import Fertilizer


@admin.register(UserRegistration)
class UserRegistrationAdmin(admin.ModelAdmin):
    list_display = ('number', 'email', 'name')
    search_fields = ('number', 'email', 'name')
    list_filter = ('email',)


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('number', 'password')
    search_fields = ('number',)

@admin.register(Fertilizer)
class FertilizerAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
