from django.forms import ModelForm, TextInput, NumberInput
from .models import Address

class AddressForm(ModelForm):
    class Meta:
        model = Address
        fields = ['logradouro','complemento','numero','cep','cidade','estado']
        widgets= {
            'logradouro': TextInput(attrs={"class": "form-control"}),
            'complemento':TextInput(attrs={"class": "form-control"}),
            'numero':NumberInput(attrs={"class": "form-control"}),
            'cep': NumberInput(attrs={"class": "form-control"}),
            'cidade':TextInput(attrs={"class": "form-control"}),
            'estado':TextInput(attrs={"class": "form-control"}) 
        }
