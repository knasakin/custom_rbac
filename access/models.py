from django.db import models


class Role(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название роли', unique=True)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'

    def __str__(self):
        return self.name


class BusinessElement(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название бизнес элемента', unique=True)

    class Meta:
        verbose_name = 'Бизнес элемент'
        verbose_name_plural = 'Бизнес элементы'

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    role = models.ForeignKey(to=Role, on_delete=models.CASCADE, related_name='access_rules')
    business_element = models.ForeignKey(to=BusinessElement, on_delete=models.CASCADE, related_name='access_rules')

    can_read = models.BooleanField(verbose_name='Может читать', default=False)
    can_create = models.BooleanField(verbose_name='Может создавать', default=False)
    can_update = models.BooleanField(verbose_name='Может обновлять', default=False)
    can_delete = models.BooleanField(verbose_name='Может удалять', default=False)

    class Meta:
        verbose_name = 'Доступ'
        verbose_name_plural = 'Доступы'
        constraints = [
            models.UniqueConstraint(
                fields=['role', 'business_element'],
                name='unique_role_business_element',
            ),
        ]

    def __str__(self):
        return f'{self.role} - {self.business_element}'
