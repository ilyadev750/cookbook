from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from recepies.models import Quantity, Recepie
from .models import Product
from products.forms import AddProductForm


# Create your views here.
def add_product_to_recipe(request, recepie_id, product_id, weight):
    recepie_id = Recepie.objects.get(pk=recepie_id)
    product_id = Product.objects.get(pk=product_id)
    try:
        product_quantity=Quantity.objects.get(recepie_id=recepie_id, product_id=product_id)
    except ObjectDoesNotExist as exc:
        product_quantity = Quantity()
    product_quantity.recepie_id = recepie_id
    product_quantity.product_id = product_id
    product_quantity.weight = weight
    product_quantity.save()
    return redirect('get_recepie_products', request.user.username, recepie_id.slug)

def delete_product_from_recepie(request, recepie_id, product_id):
    product = Quantity.objects.get(recepie_id=recepie_id, product_id=product_id)
    slug = product.recepie_id.slug
    product.delete()
    return redirect('get_recepie_products', request.user.username, slug)

def get_recepie_products(request, *args, **kwargs):
    try:
        products = Quantity.objects.filter(recepie_id=request.session['recepie_id'])
    except ObjectDoesNotExist as exc:
        products = None
    if request.method == "POST":
        product_form = AddProductForm(request.POST)
        if product_form.is_valid():
            product_name = product_form.cleaned_data['product_name'].lower()
            weight = product_form.cleaned_data['weight']
            recepie_id = request.session['recepie_id']
            try:
                product_id = (Product.objects.get(product_name=product_name)).id
            except ObjectDoesNotExist as exc:
                new_product = Product()
                new_product.product_name = product_name
                new_product.number_of_recepies = 0
                new_product.save()
                product_id = new_product.pk
            return redirect('add_product_to_recipe', recepie_id, product_id, weight)
    else:
        context = {'recepie_name': request.session['recepie_name'], 
                   'recepie_image': request.session['recepie_image'],
                   'recepie_id': request.session['recepie_id'],
                   'products': products,
                   'product_form': AddProductForm()}
        return render(request, 'products/get_recepie_products.html', context)