from rest_framework import serializers
from access.models import AccessRule


class AccessRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRule
        fields = (
            'id',
            'role',
            'business_element',
            'can_read',
            'can_create',
            'can_update',
            'can_delete'
        )
