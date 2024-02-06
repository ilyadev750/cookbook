from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
from pytils.translit import slugify
from .models import Recepie, Quantity
from products.models import Product
from .forms import CreateRecepieForm
from products.forms import AddProductForm
from django.contrib.auth.models import User

# Create your views here.

def get_all_recepies(request):
    recepies = Recepie.objects.all()
    context = {'recepies': recepies}
    return render(request, 'recepies/all_recepies.html', context)

def get_user_recepies(request, *args, **kwargs):
    user_id = (User.objects.get(username=request.user.username)).id
    user_recepies = Recepie.objects.filter(username_id=user_id)
    context = {'user_recepies': user_recepies, 'username': request.user.username}
    return render(request, 'recepies/user_recepies.html', context)

def create_recepie(request,  *args, **kwargs):
    if request.method == 'POST':
        recepie_form = CreateRecepieForm(request.POST, request.FILES)
        if recepie_form.is_valid():
            try:
                recepie = Recepie()
                recepie.recepie_name = recepie_form.cleaned_data["recepie_name"]
                recepie.recepie_image = recepie_form.cleaned_data["image"]
                recepie.slug = slugify(recepie.recepie_name)
                recepie.username_id = User.objects.get(username=request.user.username)
                recepie.save()
                request.session['recepie_name'] = recepie.recepie_name
                request.session['recepie_image'] = recepie.recepie_image.url
                request.session['recepie_id'] = recepie.pk
                return redirect('get_recepie_products', request.user.username, recepie.slug)
            except IntegrityError as exception:
                recepie_form = CreateRecepieForm()
                context = {'recepie_form': recepie_form, 'error': 'Рецепт с таким названием существует!' }
                return render(request, "recepies/create_new_recepie.html", context)
        else:
            recepie_form = CreateRecepieForm()
            context = {'message_error': 'Пожалуйста, введите данные по новому рецепту!', 'recepie_form': recepie_form }
            return render(request, "recepies/create_new_recepie.html", context)
    else:
        recepie_form = CreateRecepieForm()
        context = {'recepie_form': recepie_form}
        return render(request, "recepies/create_new_recepie.html", context)

def cook_recepie(request,  *args, **kwargs):
    recepie_id = request.session['recepie_id']
    products = Quantity.objects.filter(recepie_id=recepie_id)
    for product in products:
        product.product_id.number_of_recepies += 1
        product.product_id.save()
    return redirect('get_user_recepies', request.user.username)