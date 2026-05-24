from django.contrib import admin
from access.models import Role, BusinessElement, AccessRule


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    pass


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    pass


@admin.register(AccessRule)
class AccessRuleAdmin(admin.ModelAdmin):
    pass
