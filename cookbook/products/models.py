from django.db import models


class Product(models.Model):
    product_name = models.CharField(
        max_length=50, unique=True, verbose_name='Продукт')
    number_of_recepies = models.IntegerField(
        verbose_name='Количество рецептов')

    class Meta:
        verbose_name = 'продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return f'{self.product_name}'
