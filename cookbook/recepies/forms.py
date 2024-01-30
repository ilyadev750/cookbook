from django import forms

class CreateRecepieForm(forms.Form):
    recepie_name = forms.CharField(label='Название рецепта',max_length=50)
    image = forms.ImageField(label='Изображение рецепта')

