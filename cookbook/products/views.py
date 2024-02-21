from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from recepies.models import Quantity, Recepie
from .models import Product
from .functions import get_recepie_id, get_products, create_product_object
from products.forms import AddProductForm


def add_product_to_recipe(request, recepie_slug):
    recepie_id = int(request.GET.get('recepie_id'))
    product_id = int(request.GET.get('product_id'))
    weight = int(request.GET.get('weight'))
    try:
        product_quantity = (Quantity.objects.select_related('recepie_id')
                            .select_related('product_id')
                            .get(recepie_id__pk=recepie_id, 
                                 product_id__pk=product_id))
        product_quantity.weight = weight
        product_quantity.save()
    except ObjectDoesNotExist:
        product_quantity = Quantity()
        product_quantity.recepie_id = Recepie.objects.get(pk=recepie_id)
        product_quantity.product_id = Product.objects.get(pk=product_id)
        product_quantity.weight = weight
        product_quantity.save()
    return redirect('get_recepie_products', recepie_slug)


def delete_product_from_recepie(request, recepie_slug):
    recepie_id = int(request.GET.get('recepie_id'))
    product_id = int(request.GET.get('product_id'))
    product = Quantity.objects.get(recepie_id=recepie_id,
                                   product_id=product_id)
    product.delete()
    return redirect('get_recepie_products', recepie_slug)


def cook_recepie(request, recepie_slug):
    recepie_id = int(request.GET.get('recepie_id'))
    products = Quantity.objects.filter(recepie_id=recepie_id)
    for product in products:
        product.product_id.number_of_recepies += 1
        product.product_id.save()
    return redirect('get_user_recepies', request.user.username)


def get_recepie_products(request, recepie_slug):
    recepie_id = get_recepie_id(recepie_slug=recepie_slug)
    products = (Quantity.objects.select_related('product_id')
                .filter(recepie_id__slug=recepie_slug)
                .values("product_id__pk","product_id__product_name", "weight"))
    if request.method == "POST":
        product_form = AddProductForm(request.POST)
        if product_form.is_valid():
            product_name = product_form.cleaned_data['product_name'].lower()
            weight = product_form.cleaned_data['weight']
            recepie_id = recepie_id.pk
            try:
                product_id = ((Product.objects
                               .get(product_name=product_name)).id)
            except ObjectDoesNotExist:
                new_product = create_product_object(product_name=product_name)
                new_product.save()
                product_id = new_product.pk
            url_base = reverse('add_product_to_recipe',
                               args=[recepie_slug])
            url_args = (f'?recepie_id={recepie_id}'
                        f'&product_id={product_id}'
                        f'&weight={weight}')
            return redirect(url_base + url_args)
    else:
        context = {
                    'recepie': recepie_id,
                    'delete_product_url': reverse('delete_product_from_recepie',
                                                  args=[
                                                      recepie_slug
                                                      ]
                                                  ),
                    'cook_recepie': reverse('cook_recepie',
                                            args=[
                                                recepie_slug
                                                ]
                                            ),
                    'products': products,
                    'product_form': AddProductForm()
                    }
        return render(request, 'products/get_recepie_products.html', context)
