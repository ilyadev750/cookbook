from django import forms

class AddProductForm(forms.Form):

    product_name = forms.CharField(label='Название продукта',max_length=50)
    weight = forms.IntegerField(label='Масса, г')
    
