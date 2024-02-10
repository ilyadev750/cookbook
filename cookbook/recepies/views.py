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
    username_id = User.objects.get(username=request.user.username)
    user_recepies = Recepie.objects.filter(username_id=username_id)
    delete_recepie_url = reverse('delete_recepie', args=[request.user.username])
    context = {'user_recepies': user_recepies, 'username': request.user.username, 'delete_recepie_url': delete_recepie_url}
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

def delete_recepie(request, username):
    recepie_id = int(request.GET.get('recepie_id'))
    recepie = Recepie.objects.get(pk=recepie_id)
    recepie.delete()
    return redirect('get_user_recepies', username)
