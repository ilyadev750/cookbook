from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from recepies.models import Quantity, Recepie
from .models import Product
from products.forms import AddProductForm


# Create your views here.

def get_recepie_products(request, *args, **kwargs):
    if request.method == "POST":
        if 'add_product' in request.POST:
            product_form = AddProductForm(request.POST)
            if product_form.is_valid():
                product_name = product_form.cleaned_data['product_name']
                try:
                    product_id = (Product.objects.get(product_name=product_name)).id
                except ObjectDoesNotExist as exc:
                    new_product = Product()
                    new_product.product_name = product_form.cleaned_data['product_name']
                    new_product.number_of_recepies = 0
                    new_product.save()
                    product_id = new_product.pk
                recepie_id = request.session['recepie_id']
                weight = product_form.cleaned_data['weight']
                product_quantity = Quantity()
                product_quantity.recepie_id = Recepie.objects.get(pk=recepie_id)
                product_quantity.product_id = Product.objects.get(pk=product_id)
                product_quantity.weight = weight
                product_quantity.save()
                context = {'recepie_name': request.session['recepie_name'], 
                           'recepie_image': request.session['recepie_image'], 
                           'product_form': AddProductForm()}
                return render(request, 'products/get_recepie_products.html', context)
    else:
        context = {'recepie_name': request.session['recepie_name'], 
                   'recepie_image': request.session['recepie_image'], 
                   'product_form': AddProductForm()}
        return render(request, 'products/get_recepie_products.html', context)