from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import IntegrityError
from .models import Recepie
from .functions import create_recepie_object
from .forms import CreateRecepieForm, SearchRecepieWithoutProduct
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
                recepie = create_recepie_object(recepie_form=recepie_form, username=request.user.username)
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

def search_recepie_without_product(request):
    search_product_form = SearchRecepieWithoutProduct(request.GET)
    
