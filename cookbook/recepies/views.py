from django.shortcuts import render
from pytils.translit import slugify
from models import Recepie
from .forms import CreateRecepieForm
from products.forms import AddProductForm

# Create your views here.

def create_recepie(request):
    if request.method == 'POST':
        recepie_form = CreateRecepieForm(request.POST)
        if recepie_form.is_valid():
            recepie = Recepie()
            recepie.recepie_name = recepie_form.cleaned_data["recepie_name"]
            recepie.recepie_image = recepie_form.cleaned_data["image"]
            recepie.slug = slugify(recepie.recepie_name)
            recepie.username = request.user.username
            recepie.save() 
            product_form = AddProductForm()
            context = {'recepie_name': recepie.recepie_name, 'recepie_image': recepie.recepie_image, 'product_form': product_form}
            return render(request, "products/add_product.html", context)
        else:
            recepie_form = CreateRecepieForm()
            context = {'message_error': 'Пожалуйста, введите данные по новому рецепту!' }
            return render(request, "recepies/create_recepie.html", context)
    else:
        recepie_form = CreateRecepieForm()
        context = {}
        return render(request, "recepies/create_recepie.html", context)

