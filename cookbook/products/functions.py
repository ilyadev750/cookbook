from recepies.models import Quantity, Recepie
from .models import Product
from django.core.exceptions import ObjectDoesNotExist


def get_recepie_id(recepie_slug):
    try:
        recepie_id = Recepie.objects.get(slug=recepie_slug)
    except ObjectDoesNotExist:
        recepie_id = None
    return recepie_id


def get_products(recepie_id):
    try:
        products = Quantity.objects.filter(recepie_id=recepie_id)
    except ObjectDoesNotExist:
        products = None
    return products


def create_product_object(product_name):
    new_product = Product()
    new_product.product_name = product_name
    new_product.number_of_recepies = 0
    return new_product
