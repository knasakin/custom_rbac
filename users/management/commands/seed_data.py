from django.core.management.base import BaseCommand

from access.models import AccessRule, BusinessElement, Role
from users.models import User


class Command(BaseCommand):
    help = 'Создаём бизнес-элементы + пользователей с определёнными ролями. Заполняем БД.'

    def handle(self, *args, **options):
        admin_role, _ = Role.objects.get_or_create(name='admin')
        manager_role, _ = Role.objects.get_or_create(name='manager')
        user_role, _ = Role.objects.get_or_create(name='user')

        products_element, _ = BusinessElement.objects.get_or_create(name='products')
        orders_element, _ = BusinessElement.objects.get_or_create(name='orders')
        access_rules_element, _ = BusinessElement.objects.get_or_create(name='access_rules')

        access_rules_to_create = [
            {
                'role': admin_role,
                'business_element': products_element,
                'can_read': True,
                'can_create': True,
                'can_update': True,
                'can_delete': True,
            },
            {
                'role': admin_role,
                'business_element': orders_element,
                'can_read': True,
                'can_create': True,
                'can_update': True,
                'can_delete': True,
            },
            {
                'role': admin_role,
                'business_element': access_rules_element,
                'can_read': True,
                'can_create': True,
                'can_update': True,
                'can_delete': True,
            },
            {
                'role': manager_role,
                'business_element': products_element,
                'can_read': True,
                'can_create': True,
                'can_update': True,
                'can_delete': False,
            },
            {
                'role': manager_role,
                'business_element': orders_element,
                'can_read': True,
                'can_create': True,
                'can_update': True,
                'can_delete': False,
            },
            {
                'role': manager_role,
                'business_element': access_rules_element,
                'can_read': False,
                'can_create': False,
                'can_update': False,
                'can_delete': False,
            },
            {
                'role': user_role,
                'business_element': products_element,
                'can_read': True,
                'can_create': False,
                'can_update': False,
                'can_delete': False,
            },
            {
                'role': user_role,
                'business_element': orders_element,
                'can_read': True,
                'can_create': False,
                'can_update': False,
                'can_delete': False,
            },
            {
                'role': user_role,
                'business_element': access_rules_element,
                'can_read': False,
                'can_create': False,
                'can_update': False,
                'can_delete': False,
            },
        ]

        for rule_data in access_rules_to_create:
            AccessRule.objects.update_or_create(
                role=rule_data['role'],
                business_element=rule_data['business_element'],
                defaults={
                    'can_read': rule_data['can_read'],
                    'can_create': rule_data['can_create'],
                    'can_update': rule_data['can_update'],
                    'can_delete': rule_data['can_delete'],
                },
            )

        users_to_create = [
            {
                'email': 'admin@admin.com',
                'name': 'Admin',
                'password': '1111',
                'role': admin_role,
                'is_superuser': True,
                'is_staff': True,
            },
            {
                'email': 'manager@manager.com',
                'name': 'Manager',
                'password': '2222',
                'role': manager_role,
                'is_superuser': False,
                'is_staff': True,
            },
            {
                'email': 'user@user.com',
                'name': 'User',
                'password': '3333',
                'role': user_role,
                'is_superuser': False,
                'is_staff': False,
            },
        ]

        for user_data in users_to_create:
            email = user_data.pop('email')
            password = user_data.pop('password')

            user, created = User.objects.get_or_create(email=email, defaults=user_data)
            if created:
                user.set_password(password)
                user.save()

        self.stdout.write(self.style.SUCCESS('Начальные данные успешно созданы'))
