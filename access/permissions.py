from rest_framework.permissions import BasePermission
from access.models import AccessRule


class HasAccessPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        business_element = getattr(view, 'business_element', None)

        if not business_element:
            return False

        try:
            access_rule = AccessRule.objects.get(role=user.role, business_element__name=business_element)
        except AccessRule.DoesNotExist:
            return False

        method_permission_map = {
            'GET': access_rule.can_read,
            'POST': access_rule.can_create,
            'PATCH': access_rule.can_update,
            'PUT': access_rule.can_update,
            'DELETE': access_rule.can_delete,
        }

        return method_permission_map.get(request.method, False)

