from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from recepies.models import Quantity, Recepie
from .models import Product
from products.forms import AddProductForm


# Create your views here.

def add_product_to_recipe(request, username, recepie_slug):
    recepie_id = Recepie.objects.get(pk=int(request.GET.get('recepie_id')))
    product_id = Product.objects.get(pk=int(request.GET.get('product_id')))
    weight = int(request.GET.get('weight'))
    try:
        product_quantity=Quantity.objects.get(recepie_id=recepie_id, product_id=product_id)
    except ObjectDoesNotExist as exc:
        product_quantity = Quantity()
    product_quantity.recepie_id = recepie_id
    product_quantity.product_id = product_id
    product_quantity.weight = weight
    product_quantity.save()
    return redirect('get_recepie_products', username, recepie_slug)

def delete_product_from_recepie(request, username, recepie_slug):
    recepie_id = int(request.GET.get('recepie_id'))
    product_id = int(request.GET.get('product_id'))
    product = Quantity.objects.get(recepie_id=recepie_id, product_id=product_id)
    product.delete()
    return redirect('get_recepie_products', username, recepie_slug)

def cook_recepie(request, username, recepie_slug):
    recepie_id = int(request.GET.get('recepie_id'))
    products = Quantity.objects.filter(recepie_id=recepie_id)
    for product in products:
        product.product_id.number_of_recepies += 1
        product.product_id.save()
    return redirect('get_user_recepies', username)

def get_recepie_products(request, username, recepie_slug):
    try:
        recepie_id = Recepie.objects.get(slug=recepie_slug)
    except ObjectDoesNotExist as exc:
        recepie_id = None
    try:
        products = Quantity.objects.filter(recepie_id=recepie_id)
    except ObjectDoesNotExist as exc:
        products = None
    if request.method == "POST":
        product_form = AddProductForm(request.POST)
        if product_form.is_valid():
            product_name = product_form.cleaned_data['product_name'].lower()
            weight = product_form.cleaned_data['weight']
            recepie_id = recepie_id.pk
            try:
                product_id = (Product.objects.get(product_name=product_name)).id
            except ObjectDoesNotExist as exc:
                new_product = Product()
                new_product.product_name = product_name
                new_product.number_of_recepies = 0
                new_product.save()
                product_id = new_product.pk
            url_base = reverse('add_product_to_recipe', args=[username, recepie_slug])
            url_args = f'?recepie_id={recepie_id}&product_id={product_id}&weight={weight}'
            return redirect(url_base + url_args)
    else:
        context = {
                    'recepie': recepie_id,
                    'delete_product_url': reverse('delete_product_from_recepie', args=[username, recepie_slug]),
                    'cook_recepie': reverse('cook_recepie', args=[username, recepie_slug]),
                    'products': products,
                    'product_form': AddProductForm()
                    }
        return render(request, 'products/get_recepie_products.html', context)