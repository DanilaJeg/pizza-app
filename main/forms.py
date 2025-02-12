from django import forms
from .models import Pizza, Topping, Address, Payment

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ['size', 'crust', 'topping', 'base', 'cheese']

    topping = forms.ModelMultipleChoiceField(
        queryset = Topping.objects.all(),
        widget = forms.CheckboxSelectMultiple,
        required = False
    )

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['cardHolder', 'cardNumber', 'expiration_month', 'expiration_year', 'cvv']
        labels = {
            'cardHolder': 'Full Name',
            'cardNumber': 'Card Number',
            'expiration_month': 'Expiry Month',
            'expiration_year': 'Expiry Year',
            'cvv': 'CVV',

        }
        widgets = {
            'cardNumber': forms.TextInput(attrs={'pattern': '[0-9]{16}', 'title': '16 digits required'}),
            'expiration_month': forms.TextInput(attrs={'pattern': '[0-9]{2}', 'title': '2 digits required'}),
            'expiration_year': forms.TextInput(attrs={'pattern': '[0-9]{4}', 'title': '4 digits required'}),
            'cvv': forms.TextInput(attrs={'pattern': '[0-9]{3}', 'title': '3 digits required'})
        }

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['name', 'address1', 'address2', 'county', 'town', 'eircode']