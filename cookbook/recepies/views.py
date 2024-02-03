from django.shortcuts import render
from pytils.translit import slugify
from .models import Recepie
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
        recepie_form = CreateRecepieForm(request.POST)
        if recepie_form.is_valid():
            recepie = Recepie()
            recepie.recepie_name = recepie_form.cleaned_data["recepie_name"]
            recepie.recepie_image = recepie_form.cleaned_data["image"]
            recepie.slug = slugify(recepie.recepie_name)
            recepie.username_id = (User.objects.get(username=request.user.username)).id
            recepie.save() 
            product_form = AddProductForm()
            context = {'recepie_name': recepie.recepie_name, 'recepie_image': recepie.recepie_image, 'product_form': product_form}
            return render(request, "products/add_product.html", context)
        else:
            recepie_form = CreateRecepieForm()
            context = {'message_error': 'Пожалуйста, введите данные по новому рецепту!', 'recepie_form': recepie_form }
            return render(request, "recepies/create_new_recepie.html", context)
    else:
        recepie_form = CreateRecepieForm()
        context = {'recepie_form': recepie_form}
        return render(request, "recepies/create_new_recepie.html", context)

