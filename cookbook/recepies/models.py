from django.db import models
from products.models import Product

# Create your models here.
class Recepie(models.Model):
    recepie_name = models.CharField(max_length=50, unique=True)
    recepie_image = models.ImageField(upload_to='media/')
    slug = models.SlugField(max_length=50, unique=True)

class Quantity(models.Model):
    recepie_id = models.ForeignKey(Recepie, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    weight = models.IntegerField()