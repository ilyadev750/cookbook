from .models import Recepie
from django.contrib.auth.models import User
from pytils.translit import slugify

def create_recepie_object(recepie_form, username):
    recepie = Recepie()
    recepie.recepie_name = recepie_form.cleaned_data["recepie_name"]
    recepie.recepie_image = recepie_form.cleaned_data["image"]
    recepie.slug = slugify(recepie.recepie_name)
    recepie.username_id = User.objects.get(username=username)
    return recepie


