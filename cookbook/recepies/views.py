from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.db import IntegrityError
from .models import Recepie, Quantity
from products.models import Product
from .functions import create_recepie_object
from .forms import CreateRecepieForm, SearchRecepieWithoutProduct


def get_all_recepies(request):
    recepies = Recepie.objects.all().select_related('username_id')
    context = {'recepies': recepies}
    return render(request, 'recepies/all_recepies.html', context)


def get_user_recepies(request, username):
    user_recepies = (Recepie.objects.select_related('username_id')
                     .filter(username_id__username=username))
    delete_recepie_url = reverse('delete_recepie')
    context = {'user_recepies': user_recepies,
               'username': username,
               'delete_recepie_url': delete_recepie_url}
    return render(request, 'recepies/user_recepies.html', context)


def create_recepie(request):
    if request.method == 'POST':
        recepie_form = CreateRecepieForm(request.POST, request.FILES)
        if recepie_form.is_valid():
            try:
                recepie = create_recepie_object(recepie_form=recepie_form,
                                                username=request.user.username)
                recepie.save()
                return redirect('get_recepie_products',
                                recepie.slug)
            except IntegrityError:
                recepie_form = CreateRecepieForm()
                context = {'recepie_form': recepie_form,
                           'error': 'Рецепт с таким названием существует!'}
                return render(request,
                              "recepies/create_new_recepie.html",
                              context)
        else:
            recepie_form = CreateRecepieForm()
            context = {'message_error': 'Пожалуйста, введите данные \
                        по новому рецепту!',
                       'recepie_form': recepie_form}
            return render(request, "recepies/create_new_recepie.html", context)
    else:
        recepie_form = CreateRecepieForm()
        context = {'recepie_form': recepie_form}
        return render(request, "recepies/create_new_recepie.html", context)


def delete_recepie(request):
    recepie_id = int(request.GET.get('recepie_id'))
    recepie = Recepie.objects.get(pk=recepie_id)
    recepie.delete()
    return redirect('get_user_recepies', request.user.username)


def search_recepie_view(request):
    search_product_form = SearchRecepieWithoutProduct(request.GET)
    if search_product_form.is_valid():
        product_name = search_product_form.cleaned_data['product_name']
        try:
            product_id = Product.objects.get(product_name=product_name).pk
            base_url = reverse('show_recepies_without_product')
            url_args = f'?product_id={product_id}'
            return redirect(base_url + url_args)
        except ObjectDoesNotExist:
            search_product_form = SearchRecepieWithoutProduct()
            context = {'form': search_product_form,
                       'error': 'Продукта с таким названием не существует'}
            return render(request, 'recepies/search_recepies.html', context)
    else:
        search_product_form = SearchRecepieWithoutProduct()
        context = {'form': search_product_form,
                   'error': ''}
        return render(request, 'recepies/search_recepies.html', context)


def show_recepies_without_product(request):
    product_id = int(request.GET.get('product_id'))
    recepie_values = (Quantity.objects.filter(product_id__id=product_id)
                      .filter(weight__gt=15)
                      .values('recepie_id'))
    recepie_values_list = [value['recepie_id'] for value in recepie_values]
    recepies = Recepie.objects.exclude(pk__in=recepie_values_list)
    context = {'recepies': recepies}
    return render(request, 'recepies/show_recepies_without_product.html',
                  context)
