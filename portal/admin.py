# from integrations.models import IntegrationCategory, Integration, UserIntegration
# from django.contrib import admin
# from .models import *


# @admin.register(IntegrationCategory)
# class IntegrationCategoryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'display_name']


# @admin.register(Integration)
# class IntegrationAdmin(admin.ModelAdmin):
#     list_display = ['name', 'display_name', 'category', 'is_active']
#     list_filter = ['category', 'is_active']


# @admin.register(UserIntegration)
# class UserIntegrationAdmin(admin.ModelAdmin):
#     list_display = ['user', 'integration', 'status', 'last_sync']
#     list_filter = ['status', 'integration__category']
