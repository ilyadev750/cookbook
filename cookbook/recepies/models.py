from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Recepie(models.Model):
    recepie_name = models.CharField(max_length=50, unique=True,
                                    verbose_name='Название рецепта')
    recepie_image = models.ImageField(upload_to='recepie_images',
                                      verbose_name='Изображение рецепта')
    username_id = models.ForeignKey(User, on_delete=models.CASCADE,
                                    verbose_name='Пользователь')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='URL')
    product = models.ManyToManyField(Product, through='Quantity')

    class Meta:
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.recepie_name}'


class Quantity(models.Model):
    recepie_id = models.ForeignKey(Recepie, on_delete=models.CASCADE,
                                   verbose_name='Рецепт')
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE,
                                   verbose_name='Продукт')
    weight = models.IntegerField(verbose_name='Вес продукта')

    class Meta:
        verbose_name = 'вес продукта'
        verbose_name_plural = 'вес продуктов'

    def __str__(self) -> str:
        recepie_name = self.recepie_id.recepie_name
        product_name = self.product_id.product_name
        return f'{recepie_name} - {product_name}'
